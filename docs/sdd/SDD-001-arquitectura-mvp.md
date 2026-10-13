# SDD-001 — Arquitectura del MVP y plan de fases F0–F6

| Campo | Valor |
|---|---|
| Issue | [#6](https://github.com/Gunz-cop/ComentarioBiblico/issues/6) |
| Estado | **Borrador v0.1 — propuesta pendiente de auditoría y de aprobación del propietario**. No autoriza implementar ni desplegar. |
| Alcance | MVP Génesis 1–5, 138 versículos (DEC-001). No amplía alcance. |
| Base | `main` en `676ec3a` (tras fusionar PR #5) |
| Autor | Claude Code · 2026-10-13 |
| Investigaciones relacionadas | INV-001 [#7](https://github.com/Gunz-cop/ComentarioBiblico/issues/7) · UX-001 [#8](https://github.com/Gunz-cop/ComentarioBiblico/issues/8) / PR [#10](https://github.com/Gunz-cop/ComentarioBiblico/pull/10) · INFRA-001 [#9](https://github.com/Gunz-cop/ComentarioBiblico/issues/9) |

> **Jerarquía.** Esta SDD está subordinada a las decisiones del propietario, a `docs/decisiones/registro.md` y a `docs/requisitos.md` (AGENTS.md §2). No modifica requisitos. Donde los requisitos dejan un hueco o admiten dos lecturas, la SDD lo marca como **[Q-nn]** (pregunta al propietario) y no lo da por resuelto.
>
> **Investigaciones abiertas.** Esta SDD **no anticipa** los resultados de #7, #8 ni #9. Define contratos que funcionan con cualquier resultado razonable de esas investigaciones, y marca con **⟂ INV-001**, **⟂ UX-001** o **⟂ INFRA-001** cada punto que queda abierto hasta su resolución.

---

## 0. Resumen

- **Producto:** sitio Astro estático (DEC-011) con contenido versionado en Git, validación tipada y cero JavaScript obligatorio.
- **Arquitectura en capas:** canon → textos → original → léxico → comentario → fuentes → referencias → presentación (requisitos §7.1). Cada capa tiene un esquema Zod versionado y un directorio propio.
- **Una sola función decide qué se publica** (`esPublicable`). La consumen las rutas, el sitemap, el JSON-LD, el JSON para agentes y `llms.txt`. Así, un borrador no puede filtrarse por un camino distinto.
- **Un solo artefacto `dist/`** se construye una vez, se prueba, se despliega y se entrega a SDI.
- **Siete fases (F0–F6).** F0 y F1a no dependen de ninguna investigación abierta y pueden empezar en cuanto se apruebe esta SDD. F1b y F2 esperan a INV-001; F3 espera a UX-001; F5 espera a INFRA-001 y a la autorización de recursos en Cloudflare.
- **Paralelismo:** carriles con propiedad de directorios explícita, y contratos que se congelan antes de que dependan de ellos otros carriles (§9).

---

## 1. Insumos y trazabilidad

| Fuente | Qué aporta a esta SDD |
|---|---|
| `AGENTS.md` | Flujo SDD → auditoría → aprobación → implementación; reglas de ingeniería y editoriales |
| `docs/requisitos.md` (v0.1) | RF/RNF/RE/RL/RD, PEND-01…10, CA-01…15. Ver **[Q-01]** sobre su estado |
| `docs/decisiones/registro.md` | DEC-001…012; PROP-002 y PROP-004 siguen como propuestas |
| ADR-001 (#2) | Stack aprobado; vistas previas no indexables; estado SDI en rama dedicada; JSON por capítulo a especificar aquí |
| Repositorio [Gunz-cop/SDI](https://github.com/Gunz-cop/SDI) | Contrato de `sdi-cli@0.1.0`: `output: "static"`, mismo `dist/`, `baseline --confirm`, `run`, persistencia de `.sdi/state.json`, entrypoint directo |
| `docs/arquitectura-y-referencias.md` | Notas no vinculantes |

### 1.1 Versiones verificadas (npm, 2026-10-13)

| Paquete | Versión actual | Uso propuesto | Nota |
|---|---|---|---|
| `astro` | 7.3.8 (`latest`) | `~7.3` fijado por lockfile | La 7.4 está en beta: no usarla |
| `typescript` | 7.0.2 (`latest`) / 6.0.3 | **6.0.x** | `@astrojs/check` 0.9.10 declara `typescript: ^5 \|\| ^6` |
| `@astrojs/check` | 0.9.10 | `astro check` en CI | |
| `zod` | 4.6.7 | Vía `astro/zod` (sin dependencia directa) | Evita dos copias de Zod |
| `tailwindcss`, `@tailwindcss/vite` | 4.3.3 | Layout y componentes (DEC-011) | |
| `@astrojs/sitemap` | 3.7.4 | Sitemap filtrado | Genera `sitemap-0.xml`, el nombre que espera SDI |
| `vitest` | 5.0.4 | Pruebas unitarias y de integración | |
| `@playwright/test` / `@axe-core/playwright` | 1.64.0 / 4.13.0 | E2E, JS desactivado, axe | |
| `wrangler` | 4.150.0 | Despliegue (F5) | ⟂ INFRA-001 |
| `sdi-cli` | 0.1.0 | Paso posterior al despliegue (F5) | Entrypoint `node node_modules/sdi-cli/dist/cli.js` |
| Node | 24 LTS | `.nvmrc` + `engines` | Astro exige `>=22.12` |

**Regla:** en F0 se fijan las versiones exactas en `package-lock.json`. Cada cambio de versión mayor va en su propio PR (política de ADR-001). Esta tabla es evidencia de factibilidad, no una orden de fijar esos parches.

---

## 2. Arquitectura

### 2.1 Vista general

```
           data/ (importado, editorial)          content/ (editorial)
                   │                                    │
                   ▼                                    ▼
      scripts/importar (offline, determinista) ─► data/**/normalizado
                   │
                   ▼
    src/content.config.ts  (Content Layer: file()/glob() + esquemas Zod)
                   │
                   ▼
    src/dominio/  ── osis · canon · publicacion (esPublicable) · derivacion
                   │       (morfología→es, transliteración, guía)
                   ▼
    src/validacion/  (integridad referencial, RE-011, RE-030, RE-051/052)
                   │
       ┌───────────┼────────────────┬────────────────────┐
       ▼           ▼                ▼                    ▼
   páginas HTML  JSON-LD      /datos/v1/*.json      sitemap · llms.txt
   (src/pages)                (agent-native)        · robots · build.json
                   │
                   ▼
                 dist/  ──►  pruebas sobre dist  ──►  despliegue  ──►  SDI
```

### 2.2 Principios técnicos de esta SDD

1. **Derivar, no duplicar.** Lo derivado (morfología en español, transliteración, guía de lectura, referencias inversas) se calcula al compilar y nunca se guarda a mano (requisitos §6.2, RD-014).
2. **El build es determinista.** No hay fechas de compilación, aleatoriedad ni orden dependiente del sistema de archivos en el HTML. SDI compara huellas: un HTML no determinista provoca notificaciones falsas.
3. **Un único punto de decisión de publicación.** `esPublicable(entrada, modo)` en `src/dominio/publicacion.ts`. Ninguna página, endpoint o integración filtra por su cuenta.
4. **La compilación falla ante cualquier dato inválido** (RD-013, RF-042, RE-011). Las advertencias no bastan para reglas DEBE.
5. **Sin dependencias por anticipación.** Cada dependencia nueva se justifica en el PR que la introduce (AGENTS.md §8).

### 2.3 Estructura del repositorio (contrato CT-02)

```
/
├── astro.config.ts           # output: "static", trailingSlash: "always", site por entorno
├── package.json · package-lock.json · .nvmrc · tsconfig.json (strict)
├── wrangler.jsonc            # F5, ⟂ INFRA-001
├── sdi.config.mjs            # F5, ⟂ INFRA-001
├── data/                     # RNF-040: datos
│   ├── canon/                # libros.json (66 libros), versificacion/ ⟂ Q-06
│   ├── ediciones/<id>/       # meta.json + texto normalizado por libro ⟂ INV-001 (PEND-05)
│   ├── original/<corpus>/    # origen/ (intacto, RD-003) · parches/ · normalizado/  ⟂ INV-001
│   ├── morfologia/<sistema>/ # tabla etiqueta→español (RF-042) ⟂ INV-001
│   ├── lexico/               # glosas por lema y sentido (RD-020)
│   ├── fuentes/              # registro de fuentes (RD-021, RE-021)
│   └── referencias/          # referencias cruzadas directas (RD-014)
├── content/                  # RNF-040: contenido editorial
│   └── comentarios/genesis/  # libro · capitulos · pericopas · versiculos
├── scripts/                  # importar/, verificar/ (Node, sin red en CI salvo indicación)
├── src/
│   ├── contratos/            # esquemas Zod y tipos exportados (CT-03…CT-09)
│   ├── dominio/              # osis, canon, publicacion, derivacion/, referencias
│   ├── validacion/           # reglas de integridad y editoriales
│   ├── content.config.ts
│   ├── pages/ · layouts/ · components/   # F3 ⟂ UX-001
│   └── styles/               # tokens + CSS editorial + Tailwind (F3) ⟂ UX-001
├── public/                   # fuentes tipográficas, robots, clave IndexNow (F5)
├── tests/
│   ├── unit/ · integracion/ · dist/ · e2e/
│   └── fixtures/             # Anexos A y B como fixtures de prueba, nunca contenido publicable
└── docs/sdd/
```

**Separación (RNF-040):** `data/` (importado y léxico), `content/` (redacción editorial) y `src/` (código y presentación) no se mezclan. Las fixtures de prueba viven en `tests/fixtures/` y el build de producción no las carga.

### 2.4 Modos de compilación (contrato CT-14)

| Variable | Valores | Efecto |
|---|---|---|
| `SITIO_MODO` | `produccion` (por defecto) · `preview` · `test` | Decide qué estados se renderizan, la indexabilidad y el sitemap |
| `SITIO_URL` | URL absoluta | `site` de Astro, canónicas y `siteUrl` de SDI ⟂ PEND-10 |

| Comportamiento | `produccion` | `preview` | `test` |
|---|---|---|---|
| Estados renderizados | solo `publicado` | **[Q-02]** propuesta: `publicado` + `aprobado` + `borrador`, con banda «No publicado» | fixtures |
| `<meta name="robots" content="noindex">` y `X-Robots-Tag` | **prohibido** (prueba CI) | obligatorio | n/a |
| Sitemap y `llms.txt` | sí | no | sí |
| `/datos/v1/` | solo publicado | igual que el HTML de preview | sí |
| SDI | sí (F5) | **nunca** | nunca |

---

## 3. Contratos compartidos

Los contratos son los puntos de encuentro entre carriles (§9). Cada uno tiene un **propietario de carril**, un archivo fuente de verdad y un criterio de congelación. Un contrato congelado solo cambia mediante un PR propio etiquetado `contrato`, que incrementa `versionEsquema` cuando el cambio no es compatible.

| ID | Contrato | Fuente de verdad | Carril dueño | Se congela en | Abierto por |
|---|---|---|---|---|---|
| CT-01 | Identificadores OSIS y rangos | `src/dominio/osis.ts` | B | F1a | — |
| CT-02 | Estructura del repositorio | §2.3 | A | F0 | — |
| CT-03 | Canon (66 libros, slugs) | `src/contratos/canon.ts` + `data/canon/` | B | F1a | Q-06 (versificación) |
| CT-04 | Edición y texto bíblico | `src/contratos/texto.ts` | B | F1b | ⟂ INV-001 (PEND-05) |
| CT-05 | Interlineal: token y segmento | `src/contratos/interlineal.ts` | B | F1b | ⟂ INV-001 (PEND-01, -02) |
| CT-06 | Comentario y afirmaciones | `src/contratos/comentario.ts` | B | F1a | Q-04 |
| CT-07 | Fuentes, léxico y referencias cruzadas | `src/contratos/{fuentes,lexico,referencias}.ts` | B | F1a | — |
| CT-08 | Estados editoriales y `esPublicable` | `src/dominio/publicacion.ts` | B | F1a | Q-02 |
| CT-09 | Huella de revisión (RE-051/052) | `src/dominio/huella.ts` | B | F1a | Q-09 |
| CT-10 | Rutas y slugs | §3.10 | D | F1a (tabla) / F3 (páginas) | — |
| CT-11 | JSON para agentes `/datos/v1/` | `src/contratos/datos-v1.ts` + JSON Schema publicado | E | F4 | Q-08 |
| CT-12 | JSON-LD | `src/contratos/jsonld.ts` | E | F4 | — |
| CT-13 | `llms.txt` | §3.13 | E | F4 | — |
| CT-14 | Modos de compilación | §2.4 | A | F0 | Q-02 |
| CT-15 | Artefacto y manifiesto de build | §3.14 | A | F0 | — |
| CT-16 | Nombres de checks de CI | §6.2 | A | F0 | — |
| CT-17 | Integración SDI y rama de estado | §7.3 | F | F5 | ⟂ INFRA-001 |

### 3.1 CT-01 — OSIS

- Formatos admitidos: `Libro`, `Libro.C`, `Libro.C.V` y rangos `A-B` del mismo nivel (`Gen.1.1-Gen.2.3`). Los rangos que cruzan libros quedan fuera del MVP.
- API: `parsearOsis`, `formatearOsis`, `compararOsis`, `expandirRango(rango, canon)`, `contiene(rango, ref)`, `aSlug(ref, canon)` y `aUrl(ref, canon, publicados)`.
- La API valida contra el canon: un libro desconocido o un versículo fuera de rango es un error de compilación (RD-013).
- Pruebas: tabla dorada con casos límite (`Gen.1.31`, `Gen.2.4` en ambas mitades de un rango, `Gen.5.32`).

### 3.2 CT-03 — Canon

- `libros.json`: los 66 libros con `osis`, `slug` (RF-010), `nombre`, `nombreOriginal`, `testamento`, `seccion`, `orden` y `capitulos`. RD-016 exige los 66 desde el MVP.
- Recuento de versículos por capítulo: **obligatorio** para Gn 1–5 (CA-01). Para el resto de libros depende de **[Q-06]**: sin esa tabla, RD-013 no puede validar destinos de referencias cruzadas como Jn 1:1 o Sal 33:6.
- `deuterocanonico: false` previsto en el esquema, para no cambiar URLs al añadirlos (RD-016).

### 3.3 CT-04 — Edición y texto ⟂ INV-001

```ts
Edicion = {
  id: string                 // p. ej. "rv1909"
  nombre: string
  esquemaVersificacion: string        // RD-015; en el MVP solo se declara
  procedencia: Procedencia            // RL-001 completo
  politicaOrtografica: string         // ⟂ PEND-05: la valida INV-001, no esta SDD
  politicaNormalizacion: string       // ⟂ INV-001 (RNF-005)
  cotejo?: { referencia: string; fecha: string; alcance: string }   // RL-003, CA-12
}
VersiculoTexto = { osis: OsisVersiculo; texto: string }
Procedencia = { nombre, version, url, licencia, fechaObtencion, atribucion }  // RL-001
```

- Invariante: cada edición cubre exactamente el conjunto de versículos que declara, y el recuento coincide con el canon (CA-01).
- RL-006: cambiar de traducción por defecto = añadir una edición + cambiar `edicionPorDefecto` en la configuración. Ningún componente nombra «rv1909».

### 3.4 CT-05 — Interlineal ⟂ INV-001

El esquema refleja el modelo conceptual de los requisitos (§6.1–6.3), **sin suponer ningún corpus concreto**:

```ts
Token = {
  id: string                  // id interno estable, derivado de osis + posición
  idOrigen: string            // RD-001
  osis: OsisVersiculo
  posicion: number            // orden lógico (RNF-004)
  superficie: string          // hebreo con niqud, tal como resulte de la política de normalización
  unidoPorMaqaf: boolean      // Anexo B: maqaf entre tokens
  segmentos: Segmento[]
}
Segmento = {
  idOrigen: string            // RD-001
  superficie: string
  lema: IdLema                // RD-013: debe resolverse en el léxico
  etiqueta: { sistema: string; valor: string }   // importada tal cual
  glosa: Glosa                // editorial
  origen: { superficie: "importado", lema: "importado", etiqueta: "importado", glosa: "editorial" } // RD-002
}
Glosa = ({
    tipo: "traduccion"; texto: string; sentido: IdSentido; desvio?: { motivo: string }  // RD-020
  } | {
    tipo: "funcion"; texto: string; sentido: IdSentido   // Anexo A, token 4 (אֵת)
  }) & { estado: EstadoEditorial }                        // CA-02: «glosa aprobada»
```

- **Campos derivados** (no se almacenan): `analisisEs` (RF-042), `transliteracion` (⟂ PEND-02) y `guiaLectura` (⟂ PEND-03). Son funciones puras sobre los campos importados, con casos dorados para Gn 1:1 y 1:3 **cuando INV-001 fije las convenciones**. Hasta entonces, sus pruebas solo comprueban la forma, no el valor.
- **Parches (RD-003):** `data/original/<corpus>/parches/*.yaml` con `{ idOrigen, campo, valorAnterior, valorNuevo, motivo, fuente }`. El importador falla si `valorAnterior` no coincide con el origen, lo que detecta parches obsoletos.
- La forma exacta del importador y del mapeo de etiquetas depende del corpus. Por eso CT-05 **se congela en F1b**, después de que INV-001 se resuelva.

### 3.5 CT-06 — Comentario y afirmaciones

Requisitos: RD-010…012, RE-010…013, RE-030, RE-032. **Propuesta [Q-04]:** comentarios en **YAML estructurado**, sin MDX (en ADR-001, Claude Code y ChatGPT coinciden en evitar MDX), para que Zod valide cada afirmación sin analizar prosa libre.

```yaml
# content/comentarios/genesis/1/versiculos/1.yaml
tipo: versiculo            # libro | capitulo | pericopa | versiculo  (RD-011)
ancla: Gen.1.1             # rango OSIS
estado: borrador           # CT-08
asistidoPorIA: true        # RE-032
revisadoPor: null
fechaRevision: null
huellaRevisada: null       # CT-09
versionEsquema: 1
fuentes: [bdb, gesenius-gkc]          # RD-012: unión calculada y verificada
secciones:
  explicacion:
    - texto: "…"           # sintaxis en línea restringida (abajo)
      tipo: literaria      # linguistica | historica | literaria | interpretativa (RE-010)
      refs: [Gen.1.1, Gen.2.1]
  notasLinguisticas:
    - texto: "En Qal, [[tr:bārāʾ]] …"
      tipo: linguistica
      fuentes: [{ id: bdb, localizador: "s.v. ברא" }]   # RE-022
  otrasLecturas:
    - texto: "…"
      tipo: interpretativa
      atribucion: "la tradición rabínica (Rashi)"      # RE-013
      fuentes: [{ id: rashi-gen }]
```

- **Sintaxis en línea restringida**, con analizador propio y probado, sin HTML crudo: `*cursiva*`, `[[he:…]]` (→ `<span lang="he" dir="rtl">`, RNF-001), `[[tr:…]]` (→ `lang="he-Latn"`) y `[[ref:Gen.1.1]]` (→ enlace según RF-014). Cualquier otro marcado es un error. Así se evita la inyección de HTML y se cumple RNF-001 de forma verificable.
- **Validaciones (todas bloqueantes):**
  - RE-011: `linguistica`, `historica` e `interpretativa` sin `fuentes` → error. `literaria` exige `refs` o `fuentes`.
  - RE-013: `interpretativa` exige `atribucion`, y una lista de fórmulas prohibidas («algunos dicen», «se dice», «hay quienes»…) hace fallar la validación. La lista es configurable.
  - RD-010: heurística de incrustación. Se comprueba que el `texto` no contenga una secuencia de ≥ N palabras consecutivas del versículo de la edición (N propuesto: 8). Es una heurística: un falso positivo se resuelve ajustando el texto, no desactivando la regla.
  - RE-021: todo `id` de fuente existe en el registro.
  - RE-030 (1–3): `esSustancial(c)` = `explicacion` propia no vacía ∧ (`notasLinguisticas` ≥ 1 ∨ una afirmación de contexto específica) ∧ `estado = publicado`. El punto 4 es revisión humana.

### 3.6 CT-07 — Fuentes, léxico y referencias cruzadas

- **Fuente:** `{ id, tipo (RD-021), autor, titulo, edicion, anio, editorial?, url?, licencia?, verificadaPor, fechaVerificacion }`. RE-021: `verificadaPor` es obligatorio para que una fuente pueda citarse en contenido `aprobado` o `publicado`.
- **Léxico (RD-020):** `{ lema: IdLema, forma, sentidos: [{ id, glosa, notas?, fuentes }], estado }`. El `IdLema` depende del corpus ⟂ INV-001; el contrato solo exige que sea estable y que se resuelva.
- **Referencia cruzada (RD-014):** `{ origen: Osis, destino: Osis, tipo: cita|alusion|paralelo|tematica, procedencia: editorial|importada, fuentes? }`. Las referencias inversas se calculan en `src/dominio/referencias.ts` y nunca se escriben (CA-07).
- **[Q-05]** Destinos fuera del MVP (Jn 1:1): propuesta, mostrarlos como referencia en texto sin enlace, igual que los libros «próximamente» (RF-022). Así se cumple RF-014 («nunca a una URL inexistente»).

### 3.7 CT-08 — Estados y publicación

```ts
esPublicable(c: Comentario, modo: Modo): boolean
tieneRutaPropia(v: Versiculo, modo): boolean     // RF-029 + RE-030
```

- `produccion`: solo `publicado` (RE-050, RNF-022). `aprobado` no se renderiza en ningún sitio.
- `preview`: ⟂ **[Q-02]**.
- Transición: `aprobado → publicado` se hace en el PR de publicación revisado por el propietario. El despliegue posterior a la fusión materializa el estado.

### 3.8 CT-09 — Huella de revisión (RE-051, RE-052)

RE-051 exige que un cambio sustancial devuelva el contenido a `borrador`. La propuesta es hacerlo verificable sin un sistema de permisos:

- `huella(c)` = SHA-256 de la forma canónica de los campos **sustanciales** (secciones, anclas, fuentes y referencias). Se excluyen los metadatos y el espaciado. Las normalizaciones tipográficas (comillas, espacios) se definen en código.
- En `aprobado` o `publicado`, CI exige `huella(c) == huellaRevisada`. Si alguien cambia el contenido sin volver a `borrador` y sin una nueva revisión, la compilación falla.
- Para aprobar, el propietario (o el agente, **en el PR que el propietario revisa**) actualiza `estado`, `revisadoPor`, `fechaRevision` y `huellaRevisada` con `npm run editorial:aprobar -- <archivo>`.
- **[Q-09]** La garantía real depende de que la fusión exija la revisión del propietario: `CODEOWNERS` sobre `content/` y `data/` + protección de rama en `main`. Es una configuración del repositorio que solo puede hacer el propietario.

### 3.9 Inventario de reglas de validación (RNF-041)

Todas se ejecutan en `npm run validar` y en CI, y bloquean la fusión.

| Regla | Requisito | Fase |
|---|---|---|
| Esquemas Zod de todas las colecciones | RD-012, §7 | F1a/F1b |
| Resolución de OSIS, fuentes y lemas | RD-013, CA-04 | F1a |
| 138 versículos de texto = canon | CA-01 | F2 |
| Interlineal completo y glosa aprobada | CA-02 | F2 (forma) / F6 (glosas aprobadas) |
| Etiquetas con traducción al español | RF-042, CA-03 | F2 |
| Afirmaciones con fuente y atribución | RE-011, RE-013, CA-06 | F1a |
| No incrustar texto bíblico (heurística) | RD-010 | F1a |
| Coherencia de referencias inversas | RD-014, CA-07 | F1a |
| Huella de revisión y metadatos completos | RE-051, RE-052, CA-13 | F1a |
| Desvío de glosa marcado y justificado | RD-020 | F2 |
| Parches de corpus vigentes | RD-003 | F2 |
| Determinismo de la importación (`--check`) | §6.2 | F2 |

### 3.10 CT-10 — Rutas

Tabla de requisitos §4.2, generada con `getStaticPaths` **solo** a partir del canon, de las ediciones y de `esPublicable`. Ninguna ruta se escribe a mano (RF-002).

| Página | Ruta | Existe si |
|---|---|---|
| Home | `/` | siempre |
| Testamento | `/antiguo-testamento/`, `/nuevo-testamento/` | siempre (contenido del NT ⟂ PEND-07) |
| Libro | `/{slug}/` | el libro tiene al menos un capítulo con texto cargado |
| Capítulo | `/{slug}/{c}/` | la edición por defecto tiene el capítulo |
| Versículo | `/{slug}/{c}/{v}/` | `tieneRutaPropia` (RF-029) |
| Institucionales | `/metodologia/`, `/fuentes/`, `/acerca-de/` | siempre |
| Glosario gramatical | `/glosario/` (RF-044, PUEDE) | se propone en F3 |
| 404 | `/404.html` | siempre |

`trailingSlash: "always"` en Astro, igual que `normalization.trailingSlash` en SDI y que el manejo de barras de Workers ⟂ INFRA-001.

### 3.11 CT-11 — JSON para agentes `/datos/v1/` **[Q-08]**

ADR-001 lo deja para que la SDD lo especifique. Propuesta: incluirlo en el MVP, pero que su ausencia no bloquee el lanzamiento (puede salir de F4 sin afectar a nada más).

- Rutas: `/datos/v1/indice.json`, `/datos/v1/{slug}/{c}.json`, y un JSON Schema publicado en `/datos/v1/esquema.json`.
- Contenido por capítulo: `{ version: "1", osis, url, edicion: {id, procedencia}, versiculos: [{ osis, numero, url, texto, interlineal, comentario? }], pericopas, fuentes, procedencia }`. Solo incluye contenido que `esPublicable` acepta.
- **Sin fecha de compilación ni SHA** dentro del JSON (determinismo). El SHA vive en `build.json` (CT-15).
- Se genera desde las **mismas** funciones que alimentan el HTML. Una prueba compara HTML y JSON en Gn 1:1 y 1:3: texto, glosas, lemas y fuentes.
- **Riesgo de licencia:** redistribuir el interlineal en JSON depende de la licencia del corpus ⟂ INV-001. Si no la permite, el JSON omite las capas importadas o se aplaza.

### 3.12 CT-12 — JSON-LD

- `BreadcrumbList` en todas las páginas (RNF-021). `Article` en libro, capítulo y versículo, con `dateModified` = la `fechaRevision` publicada más reciente de la página (nunca la fecha de compilación), `inLanguage: "es"`, `isBasedOn` (la edición) y `citation` (las fuentes).
- Se valida contra un esquema propio en `tests/dist/` (CA-11). La validación con herramientas externas de Google es manual y opcional.

### 3.13 CT-13 — `llms.txt`

Formato Markdown: propósito, metodología resumida (enlace a `/metodologia/`), lista de libros y capítulos publicados, enlaces a `/datos/v1/indice.json` y licencia (⟂ PEND-06). Se genera a partir de los mismos datos y no aparece en el modo `preview`.

### 3.14 CT-15 — Artefacto y manifiesto

- `npm run build` produce `dist/` y `dist/build.json`: `{ commit, modo, versionEsquema, huellaDist }`, donde `huellaDist` es el SHA-256 del árbol de `dist/` sin contar `build.json`.
- CI sube `dist/` como artefacto **una vez**. Las pruebas sobre `dist/`, el despliegue y SDI usan **ese** artefacto, sin recompilar (requisito de SDI).
- «Despliegue confirmado» = `GET {SITIO_URL}/build.json` devuelve el `commit` y la `huellaDist` esperados. Hasta entonces no se ejecuta SDI (AGENTS.md §7). ⟂ INFRA-001 decide los reintentos y el tiempo máximo de espera.

---

## 4. Presentación ⟂ UX-001

Esta SDD **no elige** dirección visual, tipografía ni tokens: eso lo decide UX-001 (#8, PR #10). Solo fija los requisitos que cualquier dirección debe cumplir:

- HTML semántico (RNF-012), `<details>`/`<summary>` para comentario e interlineal (RF-026), sin islas ni frameworks (DEC-011).
- **CSS nativo** para prosa, hebreo, RTL y tipografía; **Tailwind 4** para layout y componentes (DEC-011). Nada de clases utilitarias dentro del contenido.
- Interlineal: DOM en orden lógico, `lang="he" dir="rtl"`, transliteración con `lang="he-Latn"` (RNF-001, RNF-004).
- Tipografía hebrea OFL servida desde el propio sitio (RNF-002), subconjunto y `font-display: swap`. La fuente concreta ⟂ UX-001.
- Procedencia distinguible sin depender del color (RF-040; WCAG 1.4.1).
- Presupuesto de 200 KB transferidos por capítulo con el interlineal plegado y sin fuentes (RNF-032), medido en CI.
- JS: ninguno obligatorio. Cualquier script progresivo necesita justificación en su PR.

---

## 5. Estrategia de pruebas

### 5.1 Niveles

| Nivel | Herramienta | Qué cubre |
|---|---|---|
| Unitario | Vitest | OSIS, canon, `esPublicable`, huella, analizador en línea, derivaciones (morfología, transliteración, guía) con casos dorados, referencias inversas |
| Integración de datos | Vitest + loaders | Colecciones completas: esquemas, integridad, reglas editoriales (§3.9) |
| Sobre `dist/` | Vitest/Node | Enlaces internos (CA-08), sitemap = rutas publicadas (CA-05), ausencia de borradores (búsqueda de marcadores de prueba), `noindex` ausente en producción, JSON-LD (CA-11), JSON v1 contra su esquema, presupuesto de peso, determinismo (dos builds → misma `huellaDist`) |
| E2E | Playwright (Chromium, WebKit y Firefox) | JS desactivado: Home → los 138 versículos (CA-10); axe en todas las páginas (CA-09); RTL y caracteres combinados (RNF-005); 320 px sin scroll horizontal |
| Manual documentada | Plantilla en `docs/` | CA-12 (cotejo RV1909), CA-14 (licencias), CA-15 (Anexos A/B), lectores de pantalla (⟂ UX-001) |

### 5.2 Fixtures de seguridad editorial

`tests/fixtures/` incluye un comentario `borrador` y otro `aprobado` con marcadores únicos (`CENTINELA-BORRADOR-…`). La prueba sobre `dist/` de producción falla si aparece cualquiera de ellos en algún archivo, incluidos el JSON, `llms.txt` y el sitemap (CA-05, RE-050). Para que la prueba sea real, el build de prueba carga las fixtures **junto con** el contenido real.

### 5.3 Matriz CA → prueba → fase

| CA | Prueba | Fase en que pasa a verde |
|---|---|---|
| CA-01 | integración: recuento de texto = canon | F2 |
| CA-02 | integración: interlineal completo; glosas `aprobado` | F2 (estructura) · F6 (aprobación) |
| CA-03 | integración: cobertura de la tabla de morfología | F2 |
| CA-04 | integración: resolución de referencias | F1a |
| CA-05 | dist: centinelas + sitemap | F4 |
| CA-06 | integración: RE-011 | F1a |
| CA-07 | unitario + integración: referencias inversas | F1a |
| CA-08 | dist: enlaces | F3 |
| CA-09 | e2e: axe | F3 |
| CA-10 | e2e: sin JS | F3 |
| CA-11 | dist: metadatos + JSON-LD | F4 |
| CA-12 | manual: cotejo | F6 |
| CA-13 | integración: huella + metadatos; manual: revisión | F1a (regla) · F6 (datos) |
| CA-14 | manual: licencias | F6 |
| CA-15 | manual + fixtures A/B validan | F1b |

---

## 6. CI, seguridad y dependencias

### 6.1 Principios

- GitHub Actions con `permissions: contents: read` por defecto. Los permisos de escritura solo se conceden por job (SDI: `contents: write` sobre la rama de estado ⟂ INFRA-001).
- Acciones de terceros fijadas por SHA, con Dependabot o Renovate agrupado mensualmente (ADR-001).
- `npm ci` con lockfile. Se audita qué paquetes ejecutan scripts de instalación y se documenta cualquier excepción.
- Los secretos (token de Cloudflare, `INDEXNOW_KEY`) solo existen en el environment `production` de GitHub, con el propietario como revisor obligatorio. **Nunca** están disponibles para PR de forks.
- CSP estricta en `_headers`: sin JS de terceros, `default-src 'self'`. ⟂ INFRA-001 para el resto de cabeceras.

### 6.2 Checks requeridos (contrato CT-16)

Nombres estables para la protección de rama: `calidad` (formato, lint, `astro check`), `datos` (`npm run validar`), `unit`, `build`, `dist`, `e2e`. F5 añade los workflows `preview` y `deploy`, que no son checks requeridos.

Flujo en un PR: `calidad`, `datos` y `unit` en paralelo → `build` (sube `dist`) → `dist` y `e2e` en paralelo.
Flujo en `main` (F5): el mismo flujo → `deploy` (environment `production`, **aprobación manual del propietario**) → confirmación (`build.json`) → `sdi`.

---

## 7. Infraestructura ⟂ INFRA-001

Esta sección solo fija las **invariantes** que vienen de ADR-001 y del contrato de SDI. Los mecanismos concretos los decide INFRA-001 (#9).

### 7.1 Cloudflare Workers Static Assets (DEC-011)

- Worker solo con assets: sin `main`, sin adaptador `@astrojs/cloudflare`, sin `run_worker_first` (evita coste y respeta «sin SSR»).
- `_headers` (caché inmutable en `/_astro/*`, seguridad y CSP) y `_redirects` (RF-012) en `public/`.
- 404 propia. El manejo de barras finales debe coincidir con `trailingSlash: "always"`.
- **Invariantes:** solo se despliega `main` con la aprobación del propietario. Es posible volver atrás a la versión anterior. ⟂ INFRA-001 decide el procedimiento y su efecto sobre el estado de SDI.

### 7.2 Vistas previas por PR

Invariantes de ADR-001: `SITIO_MODO=preview`, `noindex` en meta y cabecera, sin sitemap, sin SDI y con acceso protegido. Solo para PR de ramas del propio repositorio. Mecanismo (`wrangler versions upload`, alias, Cloudflare Access) ⟂ INFRA-001. Contenido renderizado ⟂ **[Q-02]**.

### 7.3 SDI (DEC-012) — CT-17

Invariantes, tomadas del repositorio oficial de SDI y de ADR-001:

1. `sdi-cli` como `devDependency` fijada. Se invoca con `node node_modules/sdi-cli/dist/cli.js` mientras no se verifique la 0.1.1.
2. Se ejecuta **solo** tras un despliegue de producción confirmado (CT-15), contra el **mismo** `dist/` del artefacto.
3. `sdi.config.mjs`: `source.distDir: "./dist"`, `sitemapPath: "./dist/sitemap-0.xml"` (confirmar en F0), `trailingSlash: "always"`, `keyEnv: "INDEXNOW_KEY"` y `siteUrl` = `SITIO_URL` de producción ⟂ PEND-10.
4. Estado en una **rama dedicada**, que según la propuesta de ADR-001 debe ser huérfana, quedar fuera de los disparadores de CI y no contener secretos. El job se serializa con `concurrency` sin cancelar ejecuciones en curso. El push se hace sin `--force`. Se comprueba que `.sdi/state.json` existe en disco, nunca mediante `cache-hit`.
5. Orden: primero un `baseline --confirm` único (sin notificar), autorizado por el propietario. Después, `run` en cada despliegue. El estado solo se guarda si la ejecución termina bien.
6. ⟂ INFRA-001: el nombre de la rama, el manejo de conflictos, los fallos parciales, los reintentos, la política tras volver atrás y la retención de los reportes.

---

## 8. Plan de fases F0–F6

### 8.1 Grafo de dependencias

```
                 ┌──────────── INV-001 (#7) resuelto ────────────┐
                 │                                                ▼
F0 ──► F1a ──────┴──────────────────────────────────────► F1b ──► F2 ──┐
 │      │                                                              │
 │      └──────────────► F6a (guía de estilo, perícopas, fuentes) ─────┤
 │                                                                     ▼
 │        UX-001 (#8) aprobado ─────────────────────────────────────► F3 ──► F4 ──┐
 │                                                                                │
 └──► F5a (diseño/IaC sin recursos) ── INFRA-001 (#9) + autorización ──► F5b ─────┤
                                                                                  ▼
                                                     F6b (redacción, revisión, cotejo) ──► lanzamiento
```

### 8.2 Fases

#### F0 — Fundación técnica

- **Depende de:** aprobación de esta SDD.
- **Entregables:** proyecto Astro 7 estático; TS 6 `strict`; Node 24 (`.nvmrc`, `engines`); estructura de CT-02; formato y lint; Vitest y Playwright configurados con un smoke test; workflow de CI con los checks de CT-16 (los que aún no tengan pruebas pasan sin contenido, sin marcarse como «saltados»); `build.json` (CT-15); modos de compilación (CT-14); determinismo comprobado; `sitemap-0.xml` confirmado.
- **Aceptación F0:**
  - F0-CA1: `npm ci && npm run build` en Node 24 limpio produce `dist/index.html` y `dist/build.json`.
  - F0-CA2: dos builds seguidos dan la misma `huellaDist`.
  - F0-CA3: `astro check` sin errores con TS 6; versiones exactas en el lockfile.
  - F0-CA4: CI verde en el PR, con los seis checks presentes.
  - F0-CA5: el build de producción no contiene `noindex`; el de `preview` sí.
- **No incluye:** estilos, contenido ni Cloudflare.

#### F1a — Contratos y validadores independientes del corpus

- **Depende de:** F0.
- **Entregables:** CT-01, CT-03 (66 libros), CT-06, CT-07, CT-08, CT-09; analizador de la sintaxis en línea; reglas de §3.9 marcadas F1a; fixtures A/B parciales (sin capas importadas); `npm run validar`; CLI `editorial:aprobar`.
- **Aceptación F1a:**
  - F1a-CA1: CA-04, CA-06, CA-07 y CA-13 (regla) automatizados y en verde con las fixtures.
  - F1a-CA2: cada regla tiene una fixture válida y otra inválida que demuestran que la regla salta.
  - F1a-CA3: los centinelas `borrador`/`aprobado` quedan fuera de `esPublicable("produccion")`.
  - F1a-CA4: cambiar una afirmación de un comentario `publicado` sin volver a revisarlo hace fallar `validar`.

#### F1b — Contratos dependientes del corpus

- **Depende de:** F1a + **resolución del propietario sobre PEND-01, PEND-02 y PEND-05** (INV-001 #7).
- **Entregables:** CT-04 y CT-05 congelados; sistema de etiquetas declarado; esquema de parches; fixtures A/B completas.
- **Aceptación F1b:** CA-15 (los Anexos A y B se representan sin campos ad hoc), revisada a mano por el propietario o el auditor.

#### F2 — Importación y derivación

- **Depende de:** F1b. PEND-03 solo bloquea la guía de lectura.
- **Entregables:** importadores del corpus hebreo y de la RV1909 (offline y deterministas, con `--check`); `data/**/normalizado` de Gn 1–5; tabla de morfología → español; generadores de transliteración y guía de lectura con casos dorados aprobados; registro de procedencia (RL-001).
- **Aceptación F2:** CA-01, CA-03 y CA-02 (estructura) en verde; `importar --check` sin diferencias; casos RNF-005 (dagesh, maqaf, sof pasuq, normalización) en verde; glosas presentes, aunque estén en `borrador`.

#### F3 — Presentación

- **Depende de:** F1a (rutas y contratos), F2 (datos reales; puede empezar con fixtures) y **aprobación del propietario de UX-001** (#8/PR #10), como exige ese Issue.
- **Entregables:** layouts, páginas de CT-10, interlineal accesible, CSS editorial + Tailwind 4, tipografías OFL servidas localmente, migas de pan y navegación anterior/siguiente.
- **Aceptación F3:** CA-08, CA-09 y CA-10 en verde; RNF-032 medido; criterios UX-CA aprobados en UX-001; RF-014 y RF-031 comprobados con un E2E.
- **[Q-07]** Opción: adelantar un **F3-0 estructural** (rutas y HTML semántico sin estilos visuales) antes de aprobar UX-001. Reduce el camino crítico, pero solo con autorización explícita, porque #8 condiciona F3.

#### F4 — SEO y agent-native

- **Depende de:** F3 (HTML) y F1a (contratos). La generación de `/datos/v1/` puede empezar en paralelo con F3, porque no depende del HTML; la prueba de coherencia sí.
- **Entregables:** metadatos (RNF-020), JSON-LD (CT-12), sitemap filtrado, `robots.txt`, `llms.txt` (CT-13) y `/datos/v1/` (CT-11, ⟂ Q-08).
- **Aceptación F4:** CA-05 y CA-11 en verde; JSON v1 válido contra su esquema; coherencia HTML ↔ JSON en Gn 1:1 y 1:3; pruebas de recuperación con preguntas reales sobre Gn 1:1 y 1:3 (cita exacta, análisis morfológico y fuente), documentadas.

#### F5 — Infraestructura

- **F5a (sin recursos):** puede hacerse en paralelo desde F0, cuando INFRA-001 tenga propuesta. Incluye `wrangler.jsonc`, `_headers`, `_redirects`, workflows `preview` y `deploy` desactivados o en modo de prueba, `sdi.config.mjs` y `sdi run --dry-run` local contra `dist/`.
- **F5b (con recursos):** **depende de la resolución de INFRA-001 y de una autorización explícita del propietario** para crear el token, el Worker, Access y los secretos. Incluye la primera vista previa y el ensayo de despliegue fuera de producción si INFRA-001 lo define.
- **Aceptación F5:** una vista previa protegida y `noindex`; despliegue confirmado por `build.json`; vuelta atrás ensayada; `sdi run --dry-run` correcto contra el artefacto; ningún secreto en logs ni en la rama de estado. **El despliegue de producción y el `baseline --confirm` no forman parte de F5**, sino del lanzamiento (F6b).

#### F6 — Contenido editorial y lanzamiento

- **F6a (puede empezar tras F1a):** guía de estilo (RE-040, que bloquea la redacción masiva), PEND-08 (perícopas), registro de fuentes verificadas y páginas institucionales en borrador.
- **F6b:** borradores asistidos por IA (RE-031: nunca datos importados o derivados), verificación automática, revisión del propietario por capítulo (RE-053), cotejo RV1909 (CA-12), licencias y atribuciones (CA-14, RL-004), PEND-06 y PEND-10.
- **Lanzamiento** (requiere autorización explícita): PR de publicación → fusión → despliegue aprobado → confirmación → `baseline --confirm` (primera vez) → `run` en los siguientes despliegues.
- **Aceptación F6:** CA-01…CA-15 completos, con evidencia enlazada en el PR de lanzamiento.

### 8.3 Camino crítico

`SDD aprobada → F0 → F1a → [INV-001] → F1b → F2 → [UX-001] → F3 → F4 → F6b → lanzamiento`. INV-001 es la espera más larga y más incierta: conviene que avance ya, en paralelo con esta SDD, como prevé #7.

---

## 9. Paralelismo seguro entre agentes

### 9.1 Carriles y propiedad

| Carril | Ámbito | Directorios propios | Fases |
|---|---|---|---|
| **A — Plataforma** | Configuración, CI, build, dependencias | `package*.json`, `astro.config.ts`, `tsconfig.json`, `.github/`, `tests/dist/` | F0, mantenimiento |
| **B — Contratos y dominio** | Esquemas, OSIS, publicación, validaciones | `src/contratos/`, `src/dominio/` (salvo `derivacion/`), `src/validacion/`, `src/content.config.ts`, `tests/unit/`, `tests/integracion/`, `tests/fixtures/` | F1a, F1b |
| **C — Corpus y derivación** | Importadores, parches, derivaciones | `scripts/importar/`, `data/original/`, `data/ediciones/`, `data/morfologia/`, `src/dominio/derivacion/` | F2 |
| **D — Presentación** | Páginas, componentes, estilos | `src/pages/` (salvo endpoints de datos), `src/layouts/`, `src/components/`, `src/styles/`, `public/fonts/`, `tests/e2e/` | F3 |
| **E — Agent-native y SEO** | JSON-LD, `/datos/v1/`, `llms.txt`, sitemap | `src/pages/datos/`, `src/seo/`, `src/pages/llms.txt.ts` | F4 |
| **F — Infraestructura** | Cloudflare, SDI | `wrangler.jsonc`, `sdi.config.mjs`, `public/_headers`, `public/_redirects`, `.github/workflows/{preview,deploy}.yml` | F5 |
| **G — Editorial** | Contenido y fuentes (IA + propietario) | `content/`, `data/lexico/`, `data/fuentes/`, `data/referencias/` | F6 |

### 9.2 Reglas

1. **Un agente por carril y por tarea; un PR por tarea.** Cada PR declara su carril y los contratos que usa (y su versión).
2. **Contratos primero.** Un cambio en `src/contratos/` va en un PR propio (`contrato`), revisado por el carril B, y se fusiona **antes** que los PR que dependen de él. Los demás carriles se ponen al día con un merge, sin reescribir historia ajena.
3. **Archivos compartidos serializados.** `package.json`, el lockfile, `astro.config.ts` y los workflows son del carril A. Otro carril que necesite una dependencia la pide en su PR y el cambio se aplica en un PR de A, o en el suyo con aprobación de A. El lockfile se regenera con `npm install`; nunca se resuelve a mano.
4. **Sin trabajo especulativo sobre contratos abiertos.** Mientras haya un ⟂, nadie implementa contra una suposición. Se usan fixtures marcadas como provisionales y no se fusiona nada que dependa de ellas en `main`.
5. **Editorial y técnica separados (RE-053).** Los PR de `content/` no tocan código, y al revés. Así la revisión del propietario puede centrarse en el contenido.
6. **Auditoría independiente.** Quien escribe un PR no lo audita. Si dos agentes discrepan, se documenta y decide el propietario (AGENTS.md §3).

### 9.3 Matriz de paralelismo

✅ en paralelo · ⚠️ en paralelo con un contrato congelado previamente · ⛔ secuencial

| | F0 | F1a | F1b | F2 | F3 | F4 | F5a | F6a |
|---|---|---|---|---|---|---|---|---|
| **INV-001 (#7)** | ✅ | ✅ | ⛔ (lo necesita) | ⛔ | ✅ | ✅ | ✅ | ✅ |
| **UX-001 (#8)** | ✅ | ✅ | ✅ | ✅ | ⛔ (lo necesita) | ✅ | ✅ | ✅ |
| **INFRA-001 (#9)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ propuesta | ✅ |
| **F1a** | ⛔ | — | | | | | | |
| **F2** | ⛔ | ⛔ | ⛔ | — | | | | |
| **F3** | ⛔ | ⚠️ CT-10 | ✅ (fixtures) | ✅ | — | | | |
| **F4** | ⛔ | ⚠️ CT-08 | ⚠️ CT-05 | ✅ | ⚠️ (coherencia) | — | | |
| **F5a** | ⚠️ CT-15 | ✅ | ✅ | ✅ | ✅ | ✅ | — | |
| **F6a** | ✅ | ⚠️ CT-06 | ✅ | ✅ | ✅ | ✅ | ✅ | — |

Ejemplo seguro con tres agentes después de F1a: carril C (F2, si INV-001 está resuelto) + carril F (F5a) + carril G (F6a). No comparten directorios ni contratos abiertos.

---

## 10. Bloqueantes

| ID | Bloqueante | Bloquea | Quién lo resuelve |
|---|---|---|---|
| BL-01 | Aprobación de esta SDD tras las auditorías de #6 | Toda implementación | Propietario |
| BL-02 | PEND-01, PEND-02 y PEND-05 (INV-001 #7) | F1b, F2 y todo lo que dependa | Propietario, con la investigación |
| BL-03 | Aprobación de UX-001 (#8, PR #10) | F3 | Propietario |
| BL-04 | INFRA-001 (#9) + autorización para crear recursos en Cloudflare | F5b | Propietario |
| BL-05 | Guía de estilo (RE-040) y PEND-08 | Redacción masiva (F6b) | Propietario + carril G |
| BL-06 | PEND-06 (licencia) y PEND-10 (dominio) | Lanzamiento; `siteUrl` de SDI y canónicas de producción | Propietario |
| BL-07 | **[Q-01]** Estado de `docs/requisitos.md` | Validez de esta SDD | Propietario |

---

## 11. Riesgos

| ID | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | La licencia del corpus o de la digitalización RV1909 no permite redistribuirlos (incluido el JSON v1) | Media | Alto | INV-001; CT-11 puede omitir capas importadas; RL-002 |
| R-02 | La normalización Unicode altera el orden de las marcas hebreas (meteg, ḥolam) | Media | Medio | Política de normalización declarada (CT-04); pruebas RNF-005; no aplicar NFC a ciegas ⟂ INV-001 |
| R-03 | Un borrador llega al sitio de producción | Baja | Alto | `esPublicable` único; centinelas (§5.2); prueba de sitemap; CODEOWNERS |
| R-04 | Las vistas previas se indexan o se confunden con contenido publicado | Media | Medio | `noindex` + Access + sin sitemap/SDI; prueba de ausencia de `noindex` en producción |
| R-05 | El estado de SDI se corrompe o se pierde | Media | Medio | Rama dedicada, serialización, guardado solo tras éxito, comprobación de existencia ⟂ INFRA-001 |
| R-06 | Un build no determinista provoca notificaciones falsas de SDI | Media | Medio | F0-CA2; sin fechas de compilación en el HTML |
| R-07 | Incompatibilidades de versión (TS 7, Astro 7.4 beta, error de `npx sdi`) | Alta | Bajo | Versiones fijadas; TS 6; entrypoint directo; PR por versión mayor |
| R-08 | El presupuesto de 200 KB se supera por el interlineal o las tipografías | Media | Medio | Interlineal plegado; subconjuntos; medición en CI |
| R-09 | Varios agentes provocan conflictos en contratos o en el lockfile | Media | Medio | Carriles y reglas de §9 |
| R-10 | La heurística RD-010 da falsos positivos o negativos | Media | Bajo | Umbral configurable; revisión humana como respaldo |
| R-11 | Borradores visibles en un repositorio público, si lo es | ? | Medio | **[Q-10]** El propietario confirma la visibilidad del repositorio y si eso es aceptable |
| R-12 | Validación incompleta de referencias fuera de Gn 1–5 sin una tabla de versificación | Alta | Medio | **[Q-06]** |
| R-13 | Independencia de la auditoría: esta SDD la redactó Claude Code, a quien #6 asignaba la auditoría independiente | Cierta | Medio | **[Q-03]** |
| R-14 | Alcance desbordado (MCP, búsqueda, más libros) | Baja | Medio | Fuera de alcance explícito (§12) |

---

## 12. Fuera de alcance

Ampliar el MVP más allá de Gn 1–5; búsqueda; cuentas; MCP remoto y WebMCP (DEC-010: no son dependencia de la lectura humana); base de datos, KV, D1 y R2; SSR o Worker con código; CMS; publicar contenido sin aprobación; desplegar a producción sin autorización; modificar el repositorio SDI.

---

## 13. Preguntas al propietario

| ID | Pregunta | Propuesta de esta SDD |
|---|---|---|
| Q-01 | `docs/requisitos.md` dice «Borrador v0.1 — pendiente de auditoría independiente», pero el registro cita sus secciones como aprobadas. ¿Es v0.1 la base aprobada para la SDD? | Confirmarlo y actualizar la cabecera del documento en un PR aparte |
| Q-02 | RE-050 prohíbe borradores «en el HTML compilado». ¿Se aplica también a la vista previa protegida que usa el propietario para revisar? | Aplicar RE-050 solo al artefacto de producción. La vista previa renderiza `borrador` y `aprobado` con una banda visible, `noindex` y acceso protegido |
| Q-03 | #6 proponía a Codex como autor y a Claude Code como auditor independiente. Esta SDD la redactó Claude Code. | Que Codex haga la auditoría técnica independiente (o una sesión de Claude Code sin este contexto), y ChatGPT la arquitectónica, sobre el mismo commit |
| Q-04 | Formato de comentario: YAML estructurado con afirmaciones tipadas (§3.5) frente a Markdown con directivas | YAML estructurado + sintaxis en línea restringida |
| Q-05 | Referencias cruzadas a pasajes fuera del MVP | Mostrarlas como texto sin enlace (análogo a RF-022) |
| Q-06 | Fuente y licencia de la tabla de recuentos de versículos para los 66 libros, necesaria para RD-013 | Incluirla en INV-001 (#7) como subpunto, sin ampliar su decisión |
| Q-07 | ¿Autorizar un F3-0 estructural antes de aprobar UX-001? | Opcional; acorta el camino crítico |
| Q-08 | ¿Entra el JSON `/datos/v1/` en el MVP? | Sí, como contrato v1 que no bloquea el lanzamiento |
| Q-09 | ¿Configurar CODEOWNERS y protección de rama con la revisión del propietario como obligatoria en `content/`, `data/` y `src/contratos/`? | Sí; es la base de RE-051 sin un sistema de permisos |
| Q-10 | ¿El repositorio es o será público? Los borradores serían visibles en GitHub | Confirmar si es aceptable |

---

## 14. Auditoría y aprobación

1. Auditorías sobre **el mismo commit** de este PR (procedimiento de #6, sujeto a Q-03): técnica (factibilidad, pruebas, seguridad, compatibilidad) y arquitectónica (contradicciones, bloqueantes, alineación).
2. Consolidar los hallazgos en bloqueantes, importantes y opcionales; corregir en este PR.
3. El propietario resuelve las preguntas Q-01…Q-10 y aprueba la SDD (o pide cambios).
4. Tras la aprobación: registrar la decisión en `docs/decisiones/registro.md` (PR aparte o en este, según indique el propietario) y abrir las tareas de F0.

## Resolución del propietario

_Pendiente._
