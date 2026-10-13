# Prototipo UX-001 — Génesis 1, interlineal de Gn 1:1 y Gn 1:11

- Issue: [#8](https://github.com/Gunz-cop/ComentarioBiblico/issues/8) · Propuesta: PR #10 (borrador)
- Autorización: resolución publicada en el PR #10 (comentario 6153792929), confirmada por el propietario en la sesión.
- Estado: **prototipo aislado, provisional y reversible.** No es código de producción, no se integra en Astro y no amplía el MVP.
- Iteración 2 (comentario 6154852749 en el PR #12): modo oscuro «Carbón suave», interlineal compacto y prueba de estrés con Gn 1:11 completo.
- Vista navegable para teléfono o tableta: artefacto privado en claude.ai (copia de estos ficheros, con el CSS en línea), enlazado en el PR.
- Valoración del propietario tras probarlo en su iPhone (2026-10-13): «Aceptable». Es una validación visual provisional, no la aprobación final del diseño.
- Autor: Claude Code · 2026-10-13

## Contenido

| Archivo | Descripción |
|---|---|
| `genesis-1.html` | **Variante compacta** (propuesta): hebreo, transliteración y glosa visibles por palabra; el análisis gramatical está en una tabla plegable a la que lleva cada palabra. Gn 1:1 (7 palabras) y Gn 1:11 (20 palabras, completo). |
| `genesis-1-tarjetas.html` | **Variante en tarjetas** (la anterior), con los mismos datos, para comparar. |
| `datos/` | `oshb-gn-1.json` (extraído sin editar de OSHB con `extraer_oshb.py`), `editorial-borrador.json` (transliteración y glosas **sin revisar**) y `generar.py`, que produce ambas páginas. Las páginas son generadas: no se editan a mano. |
| `estilos.css` | Tokens de la dirección A «Códice», con la disciplina de jerarquía de B. Claro «Códice» y oscuro «Carbón suave» mediante `prefers-color-scheme`. |
| `fonts/` | Tipografías **originales y sin modificar**, con sus licencias en `fonts/licencias/`. |
| `capturas/` | Capturas e `informe.json` de una misma ejecución. |
| `verificacion/` | Arnés portable con dependencias fijadas: `package.json`, `package-lock.json` y `verificar.mjs`. |

Para verlo, abre `genesis-1.html` en un navegador o sírvelo con cualquier servidor estático. Para regenerar: `cd datos && python3 -I generar.py`.

**El contenido no está aprobado.**
- Texto RV1909 provisional (RL-003, PEND-05).
- Hebreo, lemas (Strong) y morfología: **OSHB** (`openscriptures/morphhb`, `wlc/Gen.xml`). El texto WLC es de dominio público; lemas y morfología, CC BY 4.0 (Open Scriptures Hebrew Bible Project). OSHB es una candidata de PEND-01: usarla aquí **no** decide la fuente.
- Capa **derivada** (determinista, `generar.py`): hebreo sin teamim (filtra U+0591–U+05AF) y análisis legible en español a partir del código OSHB.
- Capa **editorial en borrador**: transliteración (estilo SBL aproximado, sin generador; PEND-02) y glosas, redactadas por Claude Code y **sin revisar** (DEC-007). Gn 1:1 sigue el anexo A de `docs/requisitos.md`.
- El comentario de 1:1 reproduce el borrador del anexo A.
- Se muestran los vv. 1–5 y 11; los vv. 6–10 y 12–31 se omiten: el prototipo **no** representa el capítulo íntegro ni aprueba su contenido. PEND-04 y PEND-05 siguen abiertos.

## Tipografías (provisionales)

| Fuente | Versión | Licencia verificada | SHA-256 |
|---|---|---|---|
| Ezra SIL (`SILEOT.ttf`) | 2.51, de software.sil.org | OFL 1.1, con nombres reservados «SIL» y «Ezra». La lógica de layout hebreo es MIT/X11. | `53c98ab9…0dce` |
| Source Serif 4 (Regular, It, Semibold OTF) | 4.005, release oficial de adobe-fonts | OFL 1.1, con nombre reservado «Source» | ver `sha256sum fonts/*` |

**Hallazgo relevante para la SDD.** Las dos licencias tienen *Reserved Font Names*. Según el OFL, un subconjunto o una conversión a WOFF2 es una «versión modificada» y **no puede usar el nombre reservado**. Por eso hay dos opciones:
- **(a)** Servir los ficheros originales, como hace este prototipo: 156 KB de Ezra y unos 495 KB de Source Serif en primera visita, o 660 KB si se carga también la itálica.
- **(b)** Generar subconjuntos con otro nombre de familia.

Además, Ezra SIL 2.51 data de 2007 y solo se distribuye en TTF. Hay que decidirlo antes de la implementación, por RNF-032 y RL-001.

## Modo oscuro «Carbón suave»

Valores de partida del propietario: fondo `#181A1D` y texto `#E3E5E7`. El resto de tokens se derivó y se calcularon sus contrastes con la fórmula WCAG, sobre el fondo y sobre la superficie `#212429`:

| Token | Valor | Sobre fondo | Sobre superficie |
|---|---|---|---|
| texto | `#E3E5E7` | 13.81:1 | 12.33:1 |
| texto atenuado | `#A7ADB4` | 7.71:1 | 6.88:1 |
| acento (n.º de versículo) | `#E8A08A` | 8.16:1 | 7.28:1 |
| enlace y foco | `#8EC1DD` | 8.99:1 | 8.02:1 |
| editorial | `#BCAEE6` | 8.58:1 | 7.66:1 |
| borde | `#6B727C` | 3.59:1 | 3.20:1 (≥ 3:1, WCAG 1.4.11) |

## Compacto frente a tarjetas (Gn 1:11, 20 palabras, 360 px)

| Aspecto | Compacto | Tarjetas |
|---|---|---|
| Altura del interlineal desplegado | **≈ 950 px** (`genesis-1--detalle-1-11-360-light.png`) | ≈ 2 230 px (`genesis-1-tarjetas--detalle-1-11-360-light.png`) |
| Información visible sin otra acción | hebreo, transliteración y glosa | hebreo, transliteración y glosa |
| Análisis gramatical | Una tabla por versículo; cada palabra enlaza a su fila y la fila enlaza de vuelta. Comparar palabras es fácil. | Un `<details>` por palabra: abrir varios descoloca la rejilla |
| Paradas de tabulación | **20 enlaces** (uno por palabra) + resumen de la tabla + 20 enlaces de vuelta | 20 `summary` |
| Lectura de corrido del hebreo | Mejor: las palabras forman una línea continua de derecha a izquierda | Peor: la rejilla rompe el ritmo de la frase |
| Riesgos | Las palabras con glosa larga («según su especie») ensanchan la línea. El salto a la tabla saca al lector del contexto, aunque el enlace de vuelta lo devuelve. Sin JS, la tabla se abre sola al seguir el enlace solo si el navegador expande `<details>` en la navegación por fragmento (verificado en Chromium; **sin verificar en Safari iOS**). Un script opcional de 6 líneas la abre en cualquier navegador. | Muy largo en móvil. La morfología queda dispersa. |
| Maqaf | Las palabras unidas por maqaf (זַרְעוֹ־בוֹ, עַל־הָאָרֶץ, וַיְהִי־כֵן) se muestran como dos unidades con el maqaf al final de la primera, igual que en las tarjetas. **Hay que decidir** si el token del interlineal es la palabra OSHB o la unidad gráfica unida por maqaf (glosario de `requisitos.md`). | igual |

Recomendación provisional: el patrón compacto, mejor para leer y comparar. Su coste es más paradas de tabulación y una dependencia de comportamiento nativo que hay que probar en Safari iOS.

## Evidencia de verificación

**Ejecución actual:** `capturas/informe-genesis-1.json` y `capturas/informe-genesis-1-tarjetas.json` → `meta`. Las capturas y el informe de cada página salen de **la misma ejecución**, y `capturas` lista los ficheros generados.
- Playwright 1.56.1 y axe-core 4.10.3, versiones fijadas en `verificacion/package.json` y `package-lock.json`.
- Navegador: Chromium **141.0.7390.37**, obtenido con `browser.version()`.
- Node 22.22.0.
- Las capturas `*--detalle-1-11-360-*.png` se tomaron aparte, con el mismo navegador y el JS de la página activo, solo para recortar el bloque.

### Cómo reproducirlo
```sh
cd prototipos/ux-001/verificacion
npm ci
npx playwright install chromium   # navegador gestionado por Playwright
npm run verificar                 # verifica las dos variantes; código 1 si hay desbordamiento o violaciones de axe
# Opcional: usar otro Chromium ya instalado
PW_CHROMIUM_PATH=/ruta/a/chromium npm run verificar
```
En este entorno no se permite descargar navegadores. Por eso la ejecución registrada usó `PW_CHROMIUM_PATH=/opt/pw-browsers/chromium` (Chromium 141).

### Método
- **Capturas:** con el JS de la página **desactivado**. Los `<details>` se abren con clics reales.
- **Mediciones:** reflow, axe, objetivos táctiles y peso, con JS habilitado **solo en el arnés**. Se repiten en 320, 360, 768 y 1280 px × claro/oscuro × plegado/desplegado.
- **Prueba propia del compacto:** con el JS de la página desactivado, se abre el interlineal de 1:11, se pulsa la palabra 3 y se comprueba que la tabla de análisis se abre en su fila.

| Criterio | Compacto | Tarjetas | Evidencia |
|---|---|---|---|
| UX-CA-01 Reflow | 0 px en las 16 combinaciones | 0 px en las 16 combinaciones | `reflow` |
| UX-CA-02 Contraste (axe) | 0 violaciones y 0 incompletos en claro/oscuro × plegado/desplegado. **Esto no equivale a conformidad WCAG global.** | igual | `auditoria` |
| UX-CA-03 Objetivos ≥ 24 px | ninguno por debajo | ninguno por debajo | `auditoria.objetivosMenoresDe24px` |
| UX-CA-04 Foco y teclado | `Enter` abre y cierra; el foco queda en el `summary`, con contorno visible | igual | `teclado`, `*--teclado-foco-360.png` |
| Enlace palabra → análisis sin JS | **Funciona en Chromium**: 20 enlaces en 1:11; la tabla se abre y marca la fila 3 | — | `compacto`, `genesis-1--compacto-1-11-analisis-sin-js.png` |
| UX-CA-05 VoiceOver / TalkBack | **PENDIENTE — no se ha cumplido** | **PENDIENTE** | — |
| UX-CA-06 Niqud y marcas | Sin recortes en Chromium/Linux, incluido el pataḥ furtivo y el sin con punto. **Safari iOS (iPhone del propietario, 2026-10-13, modo oscuro):** niqud, dagesh, maqaf, sof pasuq y meteg se ven correctamente, y la tabla de análisis se abre desde las palabras; capturas aportadas en la sesión, no versionadas. **Falta Chrome Android.** | igual | banco de pruebas |
| UX-CA-07 Procedencia sin color | Texto y forma del borde: continuo (importado), doble (derivado), discontinuo (borrador) | igual | capturas |
| UX-CA-08 Peso, primera visita | ≈ 691 KB (HTML + CSS ≈ 41 KB; fuentes ≈ 650 KB) | ≈ 693 KB | `pesoPrimeraVisita` |
| UX-CA-09 Sin JS | Cumple | Cumple | capturas |

### Teamim (PEND-04)
- Las páginas no muestran acentos U+0591–U+05AF.
- `datos/oshb-gn-1.json` conserva el texto importado **con** teamim. `generar.py` los filtra solo para la vista, así que mostrarlos más adelante es cambiar una línea.
- No se ha inventado ninguna cadena con teamim. PEND-04 sigue abierto.

### Observaciones y riesgos abiertos
1. En la itálica de Source Serif, la transliteración con `ʾ`/`ʿ` (U+02BE/U+02BF) muestra un espaciado irregular. Hay que verificar la cobertura del glifo o usar redonda para la transliteración.
2. El tamaño de las tarjetas en móvil motivó la variante compacta; ver la comparación.
3. Los números de versículo en línea miden 24 px, el mínimo de WCAG 2.5.8. Agrandarlos rompería el ritmo de la prosa.
4. Ezra SIL lleva años sin actualizarse. Noto Serif Hebrew sigue siendo la alternativa si aparecen fallos de renderizado en iOS.
5. En la primera iteración, la regla `:lang(he)` también se aplicaba a la transliteración (`he-Latn`) y la mostraba en la fuente hebrea. Ya está corregido con `:not(:lang(he-Latn))`.
6. El peso de las fuentes (≈ 650 KB) sigue siendo la decisión abierta más relevante para el rendimiento.

— Claude Code
