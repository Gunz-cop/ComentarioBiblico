# UX-001 — Referentes y sistema visual editorial (propuesta)

- Issue: [#8](https://github.com/Gunz-cop/ComentarioBiblico/issues/8)
- Estado: **propuesta — pendiente de resolución del propietario**. No es una decisión ni autoriza implementar UI.
- Alcance: MVP Génesis 1–5 (DEC-001). No amplía alcance.
- Autor: Claude Code · 2026-10-13

> Nada de este documento sustituye `docs/requisitos.md` ni el registro de decisiones. Los requisitos citados (RF/RNF/PEND) se toman de la versión vigente en `main`.

---

## 1. Método y nivel de evidencia

Cada afirmación lleva un nivel de evidencia para no presentar como verificado lo que no lo está:

| Nivel | Significado |
|---|---|
| **V** | Verificado en esta sesión con búsqueda web y fuente enlazada. |
| **C** | Conocimiento previo del agente sobre el sitio/producto; **pendiente de verificación visual** (captura en móvil) antes de aprobar. |
| **H** | Hipótesis de diseño propia, a validar con prototipo. |

**Limitación:** en esta sesión no se capturaron pantallas ni se auditó con axe/lector de pantalla ningún sitio externo. La matriz de la §2 es un punto de partida; la verificación con capturas a 360 px y VoiceOver/TalkBack se propone como criterio de aceptación (§8).

## 2. Matriz de referentes

| Referente | Tipo | Qué aprender | Qué evitar | Evid. |
|---|---|---|---|---|
| [Sefaria](https://www.sefaria.org) | Biblioteca de textos judíos, hebreo + traducción | Alternancia hebreo / bilingüe / traducción; segmentación alineada entre versiones; panel lateral de conexiones; tipografía serif generosa | Densidad de paneles en móvil; muchas capas simultáneas | V (modelo de datos alineado: [Wikipedia](https://en.wikipedia.org/wiki/Sefaria)) / C (UI) |
| [STEP Bible](https://www.stepbible.org) (Tyndale House) | Estudio con interlineal | Interlineal palabra a palabra con lema/morfología al tocar; orden del interlineal seleccionable | Interfaz de herramienta, poco editorial; carga JS alta | V ([About STEP](https://stepweb.atlassian.net/wiki/spaces/SUG/pages/12484610/About+STEP+Bible), [Cairn](https://scroll.cairn.edu/a-helpful-tool-for-bible-classes-unlocking-the-step-bible)) |
| [Bible Hub – Interlinear](https://biblehub.com/interlinear/genesis/1.htm) | Interlineal web | Bloques apilados por palabra (Strong / hebreo / translit. / glosa / morfo.) que se reflujan en móvil | Saturación publicitaria, contraste y jerarquía débiles | C |
| [Logos (apps móviles)](https://community.logos.com/discussion/comment/522371) | Software de estudio | En móvil sustituye las líneas interlineales por consulta palabra a palabra | Confirma que el interlineal completo en móvil es un problema real | V |
| [Interlinear Study (iPad)](https://apps.apple.com/app/interlinear-study/id6759867973) | App | Disposición conmutable lado a lado / arriba-abajo por palabra | — | V |
| [ESV.org](https://www.esv.org) / [NET Bible](https://netbible.org) | Lectura por capítulo + notas | Capítulo continuo, números de versículo discretos, notas al pie expandibles | Notas que interrumpen el flujo si se despliegan en línea | C |
| [Bible Gateway](https://www.biblegateway.com) | Lectura por capítulo | Navegación libro→capítulo rápida, URLs legibles | Ruido comercial y de cuenta | C |
| [Mechon Mamre](https://mechon-mamre.org) | Tanaj hebreo/bilingüe | HTML ligerísimo, funciona sin JS, RTL correcto | Estética datada, sin móvil cuidado | C |
| [BibleProject](https://bibleproject.com) | Divulgación | Tono didáctico y cálido; jerarquía clara para lector general | Dependencia de vídeo e ilustración | C |
| Revistas de ensayo largo (p. ej. [Aeon](https://aeon.co), [The Marginalian](https://www.themarginalian.org)) | Prosa extensa | Medida 60–70 caracteres, interlineado amplio, notas laterales en escritorio | Tipos ligeros con contraste bajo | C |
| [Open Siddur — fuentes hebreas](https://opensiddur.org/help/fonts/) | Inventario técnico | Compatibilidad de niqud y teamim por tipografía | — | V |

### 2.1 Conclusiones transversales
1. **El capítulo es prosa, no tabla.** Los mejores lectores (ESV, Sefaria) tratan el capítulo como texto continuo; el aparato aparece bajo demanda. Coincide con DEC-005.
2. **El interlineal completo no cabe en 360 px** si se muestran 6–8 capas por token (Logos lo abandona en móvil). Solución propuesta: capas configurables y tokens que se reflujan RTL (§5.2).
3. **Separar herramienta y lectura**: STEP/Bible Hub son potentes pero no editoriales. PROP-004 (modos lectura/estudio) está bien orientada.
4. **Ligereza sin JS** (Mechon Mamre) demuestra que RNF-011 y RNF-032 son alcanzables con HTML semántico.

## 3. Evaluación por criterio

| Criterio | Hallazgo / riesgo | Respuesta propuesta |
|---|---|---|
| Navegación capítulo-versículo | Selectores con JS o menús enormes | `<nav>` con migas + rejilla de capítulos 1–5 en HTML; anclas `#vN` (RF-014); «anterior/siguiente» al pie |
| Móvil | Interlineal desborda; tablas horizontales | Tokens `inline-block` en flujo RTL con `flex-wrap`; nunca scroll horizontal (WCAG 1.4.10 Reflow) |
| WCAG 2.2 AA | Objetivos táctiles pequeños (números de versículo), foco oculto bajo cabecera fija | Objetivos ≥ 24×24 px (2.5.8), `scroll-margin-top` para 2.4.11, foco visible 2 px con contraste ≥ 3:1, sin cabecera fija en MVP |
| Tipografía | Niqud recortado por `line-height` bajo; fuentes sin teamim | Hebreo con `line-height` ≥ 1.9 y tamaño 1.25–1.4× el latino; fuente OFL verificada con casos de RNF-005 |
| RTL | Orden visual ≠ orden DOM; puntuación invertida en mezcla bidi | DOM en orden lógico, `dir="rtl"` en contenedor; hebreo en línea dentro de español con `<span lang="he" dir="rtl">` (aislamiento bidi) |
| Lector de pantalla | Interlineal leído capa por capa sin contexto | Cada token = `<li>` de una `<ol>` con etiquetas accesibles (`<dl>` o texto oculto) «Palabra 1: bərēʾšît, en (el) principio» (RNF-004) |
| Prosa extensa | Comentario largo cansa en móvil | Medida 60–70 ch, cuerpo 18–19 px, `<details>` por versículo para comentario; sumario de perícopas |
| Procedencia (RF-040) | Importado vs. editorial indistinguible | Marca textual + estilo (no solo color, WCAG 1.4.1): etiqueta «Importado»/«Editorial» y borde/punteado distinto |
| Agentes | Contenido detrás de JS o canvas | Todo en HTML inicial; `<details>` presente en DOM aunque plegado; IDs OSIS en `data-osis` |

## 4. Tipografía

| Rol | Candidatas (todas OFL salvo indicación) | Notas | Evid. |
|---|---|---|---|
| Hebreo | **Ezra SIL** (OFL + MIT para lógica de layout); **Noto Serif Hebrew** (OFL); alternativas: Taamey Frank CLM (licencia GPL+excepción, **no OFL** → descartar por RNF-002) | Ezra SIL: diseñada para texto bíblico con teamim. Noto Serif Hebrew: soporta niqud y teamim según Open Siddur, con incidencia reportada en *meteg* + *ḥolam* sobre *vav*; verificar versión actual | V ([Ezra SIL/Fedora](https://getfedora.org/wiki/SIL_Ezra_fonts), [Fontsource Noto Serif Hebrew](https://fontsource.org/fonts/noto-serif-hebrew/about), [Open Siddur](https://opensiddur.org/help/fonts/)) |
| Hebreo — descartada | **SBL Hebrew** | Licencia propia de Tiro Typeworks, no OFL → incumple RNF-002 | V ([sacred-texts](https://sacred-texts.com/bib/tan/font.htm)) — confirmar licencia actual |
| Texto latino (cuerpo) | Source Serif 4, Literata, Newsreader | Serif de lectura en pantalla, ejes ópticos, buen soporte de diacríticos para transliteración (ʾ ʿ ā ē ī ō ū ə š ṣ ḥ ṭ) | C |
| UI / etiquetas | Source Sans 3, Inter, o pila del sistema | La pila del sistema ahorra peso (RNF-032) | H |

**Recomendación:** Ezra SIL para hebreo (prioridad: corrección de marcas) + Source Serif 4 para cuerpo + pila del sistema para UI. Subconjuntar con `unicode-range` y `font-display: swap`. Se registrará cada tipografía según RL-001 y RF-035.

**Nota PEND-04 (teamim):** la elección de fuente debe soportar teamim aunque inicialmente se oculten, para no rehacer el sistema si el propietario decide mostrarlos.

## 5. Direcciones visuales

Las tres comparten estructura, accesibilidad y tokens base; difieren en tono, densidad y tratamiento del interlineal.

### A. «Códice» — editorial cálido *(recomendada)*
- Papel cálido (`#FBF8F2`), tinta casi negra, acento rubricado (`#8A2E1F`) como en los manuscritos.
- Serif en todo el texto; números de versículo en versalitas pequeñas de color acento.
- Interlineal en «tarjetas» sin borde, separadas por espacio; glosa en itálica.
- Encaja con un sitio didáctico y neutral, sin connotación confesional fuerte.
- Riesgo: el rojo puede asociarse a «error»; se mitiga usándolo solo en numeración y capitulares.

### B. «Biblioteca» — académico sobrio
- Blanco puro, azul tinta (`#1F4E6B`) como único acento, más aire y menos ornamento.
- Sans para UI y etiquetas; serif solo en texto bíblico y comentario.
- Interlineal tabular alineado en escritorio, reflujo por tokens en móvil.
- Ventaja: máximo contraste y neutralidad; transmite rigor.
- Riesgo: puede resultar frío o «de herramienta» (como STEP).

### C. «Atril» — lectura inmersiva con modo estudio
- Por defecto, solo texto RV1909 a gran tamaño, sin aparato visible; un conmutador sin JS (`<details>` / enlaces a anclas) abre el modo estudio.
- Fondo oscuro como opción de primera clase (`prefers-color-scheme`).
- Ventaja: la mejor experiencia de lectura de corrido.
- Riesgo: el comentario — valor diferencial del sitio — queda escondido; más estados que probar.

**Recomendación de Claude Code:** A como base, adoptando de B la disciplina de un solo acento por función y de C el modo oscuro. Desacuerdo explícito posible: si el propietario prioriza percepción académica, B es igualmente válida.

## 6. Sistema de diseño preliminar (tokens)

### 6.1 Color (dirección A) — contrastes calculados (WCAG 2.x, fórmula de luminancia relativa)

| Token | Claro | Contraste sobre fondo | Oscuro | Contraste sobre fondo |
|---|---|---|---|---|
| `--color-bg` | `#FBF8F2` | — | `#171513` | — |
| `--color-text` | `#1F1B16` | 16.15:1 | `#E8E2D6` | 14.12:1 |
| `--color-text-muted` | `#5C5348` | 7.11:1 | `#A9A08F` | 7.03:1 |
| `--color-accent` (nº versículo, capitulares) | `#8A2E1F` | 7.95:1 | `#E39A7F` | 7.97:1 |
| `--color-link` | `#1F4E6B` | 8.39:1 | `#8EC1DD` | 9.39:1 |
| `--color-editorial` (capa editorial) | `#5B3F8C` | 7.82:1 | `#B9A8E0` | 8.45:1 |
| `--color-surface` / texto tenue sobre ella | `#F3EEE3` / `#6B5A2E` | 5.8:1 | — | — |
| `--color-border` (decorativo, no informativo) | `#C9BFAE` | 1.72:1 *(solo decorativo)* | `#6E6555` | 3.17:1 |

Todos los colores de texto superan 4.5:1 (y la mayoría 7:1, AAA). Los bordes con información (foco, campos) usarán `--color-text` o `--color-link` (≥ 3:1, WCAG 1.4.11). Nunca se distingue importado/editorial solo por color.

### 6.2 Tipografía

| Token | Valor (móvil → escritorio) |
|---|---|
| `--font-body` | Source Serif 4, Georgia, serif |
| `--font-hebrew` | Ezra SIL, Noto Serif Hebrew, serif |
| `--font-ui` | system-ui, sans-serif |
| `--size-body` | `clamp(1.125rem, 1rem + 0.5vw, 1.25rem)` (18→20 px) |
| `--size-hebrew` | `calc(var(--size-body) * 1.35)` |
| `--size-small` | `0.875em` (mín. 15 px efectivos) |
| Escala de títulos | razón 1.25 (h1 ≈ 2.44em … h4 ≈ 1.25em) |
| `--leading-body` | 1.6 |
| `--leading-hebrew` | 1.9 |
| `--measure` | `66ch` |

### 6.3 Espaciado, forma y movimiento
- Escala de 4 px: `--space-1` 4 · 2 8 · 3 12 · 4 16 · 5 24 · 6 32 · 7 48 · 8 64.
- Margen lateral móvil `--space-4`; objetivo táctil mínimo 44×44 px para navegación (supera 2.5.8).
- `--radius` 4 px; sin sombras salvo foco.
- Foco: `outline: 2px solid var(--color-link); outline-offset: 2px`.
- `prefers-reduced-motion`: sin animaciones; ninguna es necesaria.
- Implementación: tokens como CSS custom properties expuestas a Tailwind 4 (`@theme`), coherente con DEC-011.

## 7. Prototipos conceptuales (móvil, 360 px)

### 7.1 Capítulo (`/genesis/1/`)
```
┌────────────────────────────────┐
│ Inicio › AT › Génesis › 1      │  ← nav migas (RNF-012)
│                                │
│ GÉNESIS 1                      │  h1
│ La creación (1:1–2:3)          │  perícopa (PEND-08)
│ [Lectura | Estudio]            │  enlaces/anclas, sin JS
│                                │
│ ¹En el principio crió Dios     │  RV1909 (PEND-05)
│ los cielos y la tierra. ²Y la  │
│ tierra estaba desordenada…     │
│                                │
│ ▸ Comentario de 1:1            │  <details>
│ ▸ Hebreo e interlineal de 1:1  │  <details>
│                                │
│ ‹ Anterior        Génesis 2 ›  │
│ Capítulos: [1][2][3][4][5]     │  objetivos 44 px
└────────────────────────────────┘
```

### 7.2 Interlineal plegado → abierto (Gn 1:1)
```
▾ Hebreo e interlineal de 1:1
  בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת…   ← línea completa, lang=he dir=rtl
  Capas: ☑ glosa ☑ translit. ☐ guía ☐ morfología   (H: sin JS → presets por enlace)

        ┌──────────┐ ┌──────────┐
        │  בָּרָא   │ │ בְּרֵאשִׁית │   ← flujo RTL, se reflujan
        │  bārāʾ   │ │ bərēʾšît │
        │  creó    │ │ en (el)  │
        │ Importado│ │ principio│
        └──────────┘ └──────────┘
   ┌──────────┐ ┌──────────┐
   │הַשָּׁמַיִם │ │   אֵת     │ │ אֱלֹהִים │
   …
  Leyenda: ● Importado (hebreo, lema, etiqueta) ◆ Editorial (glosa, guía)
```
- DOM: `<ol dir="rtl" lang="he">` con un `<li>` por token en orden lógico; el lector de pantalla oye «1, bərēʾšît, en el principio», etc. (RNF-004).
- Ver capas sin JS: la versión inicial muestra glosa + transliteración; las capas extra (morfología, lema) en un `<details>` por token o en la página de versículo. Un conmutador con JS es mejora progresiva opcional.

## 8. Criterios de aceptación propuestos (para la fase de prototipo/F3)

| ID | Criterio | Verificación |
|---|---|---|
| UX-CA-01 | Sin scroll horizontal a 320 px CSS y zoom 400 % (1.4.10) en capítulo e interlineal | Playwright a 320 px |
| UX-CA-02 | Contrastes ≥ 4.5:1 texto, ≥ 3:1 componentes/foco, en claro y oscuro | axe + script de tokens |
| UX-CA-03 | Objetivos táctiles ≥ 24×24 px (2.5.8); navegación ≥ 44 px | Playwright medición |
| UX-CA-04 | Foco nunca oculto (2.4.11) y visible | Prueba de teclado |
| UX-CA-05 | Orden de lectura del interlineal = orden lógico del texto en VoiceOver iOS y TalkBack | Prueba manual documentada |
| UX-CA-06 | Niqud sin recortes; casos RNF-005 (dagesh, maqaf, sof pasuq, meteg+ḥolam) renderizados correctamente en Safari iOS, Chrome Android y Firefox | Capturas de referencia |
| UX-CA-07 | Importado/editorial distinguibles sin color (1.4.1) | Revisión + captura en escala de grises |
| UX-CA-08 | Capítulo con interlineal plegado < 200 KB sin fuentes en caché (RNF-032) | Medición build |
| UX-CA-09 | Todo legible y navegable sin JS | Playwright con JS desactivado |
| UX-CA-10 | Capturas de los referentes «C» de la §2 a 360 px adjuntas antes de aprobar la dirección | Revisión del propietario |

## 9. Decisiones que se piden al propietario

1. Dirección visual: **A (recomendada)**, B o C, o combinación.
2. Tipografía hebrea: Ezra SIL (recomendada) o Noto Serif Hebrew.
3. ¿Modo oscuro en MVP? (Recomendado: sí, por `prefers-color-scheme`, sin conmutador JS.)
4. PEND-04 (teamim): la propuesta no lo bloquea; se recomienda ocultarlos en MVP y mantener una fuente compatible.
5. Autorizar prototipo estático (HTML/CSS, sin integrar en Astro) de la dirección elegida para validar UX-CA-01…09.

## Resolución del propietario

_Pendiente._

---
— Claude Code
