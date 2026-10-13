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
| `capturas/` | Capturas e `informe.json` con los resultados automáticos. |

Para verlo, abre `genesis-1.html` en un navegador o sírvelo con cualquier servidor estático.

**El contenido no está aprobado.** El texto RV1909 es provisional (RL-003, PEND-05). El interlineal y el comentario reproducen el ejemplo ilustrativo del anexo A de `docs/requisitos.md`. Los versículos 6–31 se omiten.

## Tipografías (provisionales)

| Fuente | Versión | Licencia verificada | SHA-256 |
|---|---|---|---|
| Ezra SIL (`SILEOT.ttf`) | 2.51, de software.sil.org | OFL 1.1, con nombres reservados «SIL» y «Ezra». La lógica de layout hebreo es MIT/X11. | `53c98ab9…0dce` |
| Source Serif 4 (Regular, It, Semibold OTF) | 4.005, release oficial de adobe-fonts | OFL 1.1, con nombre reservado «Source» | ver `sha256sum fonts/*` |

**Hallazgo relevante para la SDD.** Las dos licencias tienen *Reserved Font Names*. Según el OFL, un subconjunto o una conversión a WOFF2 es una «versión modificada» y **no puede usar el nombre reservado**. Por eso hay dos opciones:
- **(a)** Servir los ficheros originales, como hace este prototipo: unos 155 KB de Ezra y unos 660 KB en total de Source Serif.
- **(b)** Generar subconjuntos con otro nombre de familia.

Además, Ezra SIL 2.51 data de 2007 y solo se distribuye en TTF. Hay que decidirlo antes de la implementación, por RNF-032 y RL-001.

## Evidencia de verificación

Chromium 1194 (Playwright), servidor local. Resultados completos en `capturas/informe.json`.

| Criterio | Resultado | Evidencia |
|---|---|---|
| UX-CA-01 Reflow 320 px (equivale a 1280 px al 400 %) | **Cumple**: 0 px de desbordamiento horizontal en 320, 360 y 1280 px, en claro y oscuro | `informe.json`, `movil-320-*.png` |
| UX-CA-02 Contraste | **Cumple en axe**: 0 violaciones WCAG 2.0/2.1/2.2 A/AA en claro y oscuro (27 reglas aprobadas). Los contrastes de los tokens se calcularon en la propuesta del PR #10. | `informe.json` |
| UX-CA-03 Objetivos ≥ 24×24 px | **Cumple**: ningún enlace ni `summary` visible por debajo de 24 px. La navegación usa 44 px. | `informe.json` |
| UX-CA-04 Foco visible y no oculto | **Cumple** en la prueba: el orden de tabulación es lógico y no hay cabecera fija | `teclado-foco-360.png`, `informe.json` |
| Teclado | `Tab` recorre migas → versículos → `summary` → navegación. `Enter` abre el interlineal. | `informe.json` |
| UX-CA-05 VoiceOver / TalkBack | **PENDIENTE — no se ha cumplido.** El entorno no dispone de lectores de pantalla reales. Solo se comprobó el árbol de accesibilidad de Chromium: los tokens se exponen como `list` → `listitem` en el orden lógico 1→7, con términos ocultos visualmente (Palabra, Hebreo, Transliteración, Glosa). | `informe.json` (`arbolAccesibleInterlineal`) |
| UX-CA-06 Niqud y marcas | **Cumple en Chromium/Linux.** Dagesh, shin/sin, ḥatef, maqaf, ḥolam male, sof pasuq y meteg se ven sin recortes. **Falta probarlo** en Safari iOS y Chrome Android. | banco de pruebas en las capturas |
| UX-CA-07 Procedencia sin color | **Cumple**: etiqueta textual («Importado» / «Editorial») y borde continuo o discontinuo | capturas |
| UX-CA-08 < 200 KB | HTML + CSS ≈ 24 KB. Las fuentes originales pesan unos 815 KB (RNF-032 las excluye en caché); ver el hallazgo de licencias. | `informe.json` |
| UX-CA-09 Sin JS | **Cumple**: todas las capturas se hicieron con JavaScript desactivado en la página. Los `<details>` funcionan de forma nativa. | `movil-360-plegado-sin-js.png` |

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
