# Prototipo UX-001 — Génesis 1 e interlineal de Gn 1:1

- Issue: [#8](https://github.com/Gunz-cop/ComentarioBiblico/issues/8) · Propuesta: PR #10 (borrador)
- Autorización: resolución publicada en el PR #10 (comentario 6153792929), confirmada por el propietario en la sesión.
- Estado: **prototipo aislado, provisional y reversible.** No es código de producción, no se integra en Astro y no amplía el MVP.
- Autor: Claude Code · 2026-10-13

## Contenido

| Archivo | Descripción |
|---|---|
| `genesis-1.html` | Página de capítulo: migas, texto (vv. 1–5), interlineal y comentario plegables con `<details>`, banco de pruebas tipográficas y navegación de capítulos. HTML semántico y sin JavaScript. |
| `estilos.css` | Tokens de la dirección A «Códice», con la disciplina de jerarquía de B. Tema claro y oscuro mediante `prefers-color-scheme`. |
| `fonts/` | Tipografías **originales y sin modificar**, con sus licencias en `fonts/licencias/`. |
| `capturas/` | Capturas e `informe.json` de una misma ejecución. |
| `verificacion/` | Arnés portable con dependencias fijadas: `package.json`, `package-lock.json` y `verificar.mjs`. |

Para verlo, abre `genesis-1.html` en un navegador o sírvelo con cualquier servidor estático.

**El contenido no está aprobado.** El texto RV1909 es provisional (RL-003, PEND-05). El interlineal y el comentario reproducen el ejemplo ilustrativo del anexo A de `docs/requisitos.md`. Los versículos 6–31 se omiten: el prototipo **no** representa el capítulo íntegro ni aprueba su contenido. PEND-04 y PEND-05 siguen abiertos.

## Tipografías (provisionales)

| Fuente | Versión | Licencia verificada | SHA-256 |
|---|---|---|---|
| Ezra SIL (`SILEOT.ttf`) | 2.51, de software.sil.org | OFL 1.1, con nombres reservados «SIL» y «Ezra». La lógica de layout hebreo es MIT/X11. | `53c98ab9…0dce` |
| Source Serif 4 (Regular, It, Semibold OTF) | 4.005, release oficial de adobe-fonts | OFL 1.1, con nombre reservado «Source» | ver `sha256sum fonts/*` |

**Hallazgo relevante para la SDD.** Las dos licencias tienen *Reserved Font Names*. Según el OFL, un subconjunto o una conversión a WOFF2 es una «versión modificada» y **no puede usar el nombre reservado**. Por eso hay dos opciones:
- **(a)** Servir los ficheros originales, como hace este prototipo: 156 KB de Ezra y unos 495 KB de Source Serif en primera visita, o 660 KB si se carga también la itálica.
- **(b)** Generar subconjuntos con otro nombre de familia.

Además, Ezra SIL 2.51 data de 2007 y solo se distribuye en TTF. Hay que decidirlo antes de la implementación, por RNF-032 y RL-001.

## Evidencia de verificación

**Ejecución actual:** `capturas/informe.json` → `meta`. Las capturas y el informe salen de **la misma ejecución**, y `informe.json.capturas` lista los ficheros generados.
- Playwright 1.56.1 y axe-core 4.10.3, versiones fijadas en `verificacion/package.json` y `package-lock.json`.
- Navegador: Chromium **141.0.7390.37**, obtenido con `browser.version()`.
- Node 22.22.0.

### Cómo reproducirlo
```sh
cd prototipos/ux-001/verificacion
npm ci
npx playwright install chromium   # navegador gestionado por Playwright
npm run verificar                 # termina con código 1 si hay desbordamiento o violaciones de axe
# Opcional: usar otro Chromium ya instalado
PW_CHROMIUM_PATH=/ruta/a/chromium npm run verificar
```
En este entorno no se permite descargar navegadores. Por eso la ejecución registrada usó `PW_CHROMIUM_PATH=/opt/pw-browsers/chromium` (Chromium 141). Con el navegador que fija Playwright 1.56.1, la versión de Chromium puede ser otra: el informe siempre registra la que se usó.

### Método
- **Capturas:** con el JS de la página **desactivado**. Los `<details>` se abren con clics reales, que es el comportamiento nativo sin JS.
- **Mediciones:** reflow, axe, objetivos táctiles y peso se miden en contextos con JS habilitado **solo para el arnés**; la página no contiene JS. Se repiten en 320, 360 y 1280 px × claro/oscuro × plegado/desplegado.

| Criterio | Resultado | Evidencia |
|---|---|---|
| UX-CA-01 Reflow (320 px ≈ 1280 px al 400 %) | 0 px de desbordamiento horizontal en las 12 combinaciones (3 anchos × 2 esquemas × 2 estados) | `informe.json` → `reflow`, `movil-320-*-{plegado,desplegado}.png` |
| UX-CA-02 Contraste | axe: 0 violaciones y 0 resultados incompletos en claro/oscuro × plegado/desplegado. **Esto no equivale a conformidad WCAG global**: axe solo cubre una parte de los criterios. | `informe.json` → `auditoria` |
| UX-CA-03 Objetivos ≥ 24×24 px | Ningún enlace ni `summary` visible por debajo de 24 px en ningún estado | `auditoria.objetivosMenoresDe24px` |
| UX-CA-04 Foco y teclado | Orden de tabulación lógico. `Enter` abre y vuelve a cerrar el interlineal, y el foco se queda en el `summary` con contorno visible. | `informe.json` → `teclado`, `teclado-foco-360.png` |
| UX-CA-05 VoiceOver / TalkBack | **PENDIENTE — no se ha cumplido.** Solo se revisó el árbol de accesibilidad de Chromium: lista → elementos en orden lógico 1→7. Falta comprobar en un lector real cómo se leen los `dl` anidados en cada tarjeta y los estados abierto/cerrado. | `arbolAccesibleInterlineal` |
| UX-CA-06 Niqud y marcas | Sin recortes en Chromium/Linux. **Falta probarlo** en Safari iOS y Chrome Android, y comparar Ezra SIL con Noto Serif Hebrew en iOS. | banco de pruebas en las capturas |
| UX-CA-07 Procedencia sin color | Cumple: texto «Importado» / «Editorial» y borde continuo o discontinuo | capturas |
| UX-CA-08 Peso | Primera visita sin caché: **674 KB** transferidos. HTML + CSS suman 24 KB y las fuentes 650 KB (Ezra 156 KB, Source Serif Regular 241 KB, Semibold 253 KB). La itálica solo se descarga al desplegar. **La caché no neutraliza este coste en la primera visita**: hay que decidir formato y subconjuntos (ver la sección de tipografías). | `informe.json` → `pesoPrimeraVisita` |
| UX-CA-09 Sin JS | Cumple: capturas y prueba de teclado hechas con el JS de la página desactivado | capturas `*-plegado.png` / `*-desplegado.png` |

### Teamim (PEND-04)
- Ningún texto del prototipo contiene acentos U+0591–U+05AF.
- La propuesta para la capa de datos es conservar el texto importado completo y filtrar los teamim solo en la presentación, de forma determinista.
- No se han inventado cadenas con teamim. PEND-04 sigue abierto.

### Observaciones y riesgos abiertos
1. En la itálica de Source Serif, la transliteración con `ʾ`/`ʿ` (U+02BE/U+02BF) muestra un espaciado irregular. Hay que verificar la cobertura del glifo o usar redonda para la transliteración.
2. En 320 px el interlineal usa dos columnas. Con el análisis desplegado, las tarjetas crecen mucho. Se recomienda probar con usuarios la opción de mostrar el análisis solo en la página del versículo.
3. Los números de versículo en línea miden 24 px, el mínimo de WCAG 2.5.8. Agrandarlos rompería el ritmo de la prosa.
4. Ezra SIL lleva años sin actualizarse. Noto Serif Hebrew sigue siendo la alternativa si aparecen fallos de renderizado en iOS.

— Claude Code
