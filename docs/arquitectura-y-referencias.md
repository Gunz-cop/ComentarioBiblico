# Arquitectura moderna, UX y agent-native — notas de trabajo

**Estado: propuestas para análisis; no reemplazan ni modifican los requisitos aprobados.**

## Dirección técnica
- Astro SSG en la última versión **estable compatible al iniciar la implementación**, sin fijar aquí una versión no verificada.
- TypeScript estricto, Content Collections/Content Layer y validación con Zod.
- HTML semántico y CSS nativo como base; evaluar Tailwind CSS v4 para el sistema visual.
- JavaScript progresivo solo cuando aporte interacción; evaluar islas Astro y Preact si el interlineal lo exige.
- Vitest, Playwright, auditorías de accesibilidad y enlaces, y CI en GitHub.
- Despliegue estático en Cloudflare; verificar límites vigentes y requisitos de adaptadores antes de cerrar SDD.

## UI y UX
- Priorizar lectura móvil, legibilidad, hebreo RTL, navegación sin JS y accesibilidad WCAG 2.2 AA.
- Evaluar dos superficies: lectura continua del capítulo y estudio lingüístico bajo demanda.
- Benchmark: [STEP Bible](https://www.stepbible.org/), [Sefaria](https://www.sefaria.org/), [Bible Hub](https://biblehub.com/), [Logos](https://www.logos.com/), [BibleProject](https://bibleproject.com/), [Blue Letter Bible](https://www.blueletterbible.org/), [BibliaTodo](https://www.bibliatodo.com/).
- Son referencias de patrones, no modelos para copiar contenido o identidad visual.

## SDI desde el inicio
- Integrar el sitio como consumidor del SDI existente, sin duplicar su núcleo.
- Propuesta: build validado → despliegue confirmado → comparar estado de URLs → distribución/notificación y reporte.
- SDI facilita descubrimiento, pero no garantiza indexación.

## Agent-native desde el inicio
1. HTML inicial completo y navegable sin JS, metadatos, enlaces estables, fuentes y procedencia.
2. Datos estructurados derivados de la misma fuente aprobada que genera HTML.
3. Estudiar MCP remoto y WebMCP como superficies complementarias, con contratos y control de versiones.
4. Pruebas de recuperación con preguntas reales sobre Génesis 1:1 y 1:3, incluyendo citas y análisis morfológico.

## Reglas de implementación
- Mantener el MVP de Génesis 1–5 y no introducir un CMS ni una base de datos por anticipación.
- Separar decisión aprobada de propuesta, experimento o investigación.
- Resolver las decisiones pendientes y bloqueantes identificadas en `docs/requisitos.md` antes de implementar los componentes afectados.
