# AGENTS.md — Comentario Bíblico

Instrucciones compartidas para Codex, Claude Code y otros agentes que trabajen en este repositorio.

## 1. Objetivo y límites
- Sitio editorial en español de comentario bíblico versículo por versículo.
- **MVP estrictamente Génesis 1–5.** No ampliar alcance sin autorización del propietario.
- Perspectiva neutral, didáctica, basada en fuentes verificables. El propietario revisa y aprueba contenido antes de publicar.
- Este archivo es una guía de colaboración, **no sustituye los requisitos ni concede autorización para cambiar decisiones**.

## 2. Autoridad y fuentes de verdad
Orden de prioridad:
1. Decisiones explícitas y vigentes del propietario.
2. `docs/decisiones/registro.md` y resoluciones aprobadas en Issues enlazados.
3. `docs/requisitos.md` en su versión aprobada.
4. SDD, arquitectura y especificaciones aprobadas.
5. Issues/PR/código vigente.
6. Conversaciones y propuestas no aprobadas.

Antes de actuar, **comprobar la rama, el estado del repo, los PR abiertos y la versión de los documentos**. No dar por fusionada una rama ni por aprobado un borrador. Si hay contradicciones relevantes, detener solo el trabajo afectado y pedir resolución.

**Roles:** propietario = autoridad final; ChatGPT = consultoría arquitectónica e investigación/auditoría; Codex = desarrollo, SDD, pruebas y propuestas arquitectónicas; Claude Code = desarrollo, SDD, auditoría y criterio arquitectónico independiente. Ningún agente aprueba por el propietario.

## 3. Decisiones en GitHub
- **Issue/ADR:** plantear contexto, alternativas, riesgos, recomendación y desacuerdos. Dejar la sección «Resolución del propietario» pendiente hasta aprobación explícita.
- **PR:** cambios concretos a documentación, SDD o código; enlazar el Issue/ADR y las pruebas.
- Registrar en `docs/decisiones/registro.md` una referencia concisa a decisiones aprobadas y su Issue, no duplicar debates completos.
- Los agentes pueden disentir justificadamente; no se requiere unanimidad ni rondas infinitas de auditoría.
- No crear Issues, etiquetas, dependencias ni tareas fuera de alcance sin necesidad.

## 4. Flujo de trabajo
1. Leer requisitos y decisiones pertinentes; verificar estado real.
2. Aclarar el objetivo y los criterios de aceptación.
3. Para cambios importantes: propuesta/plan → SDD → auditoría independiente → aprobación → implementación en rama → pruebas → PR → revisión del propietario.
4. Para cambios pequeños y autorizados: solución mínima, pruebas proporcionales y PR cuando corresponda.
5. Reportar evidencia de ejecución: comandos, resultados, limitaciones y riesgos residuales. Nunca declarar pruebas como ejecutadas si no lo fueron.
6. No fusionar, desplegar, publicar comentarios ni cambiar decisiones sin autorización explícita.

## 5. Ingeniería
- Priorizar la última versión **estable y compatible** de Astro al iniciar implementación, verificando documentación oficial; evitar características experimentales sin justificación y aprobación.
- Astro SSG y HTML semántico inicial completo; navegación y lectura funcionales sin JavaScript.
- TypeScript estricto; Content Collections/Content Layer y Zod según los requisitos.
- CSS moderno, diseño mobile-first, accesibilidad WCAG 2.2 AA; evaluar Tailwind v4 sin imponerlo hasta cerrar ADR.
- JavaScript progresivo solo cuando sea útil; evitar hidratar páginas enteras o añadir frameworks por defecto.
- Separar canon, textos, corpus original, léxico, comentarios, fuentes y presentación.
- Mantener dependencias y complejidad mínimas; contratos verificables, tests automatizados y CI.
- No introducir base de datos ni CMS para el MVP sin nueva decisión.

## 6. Editorial y datos bíblicos
- Traducción base RV1909, con verificación documental de edición digital y licencia.
- IDs OSIS internos; URLs canónicas estables.
- Interlineal hebreo con tokens, segmentos, lemas, morfología, transliteración y glosas revisadas.
- Separar **importado**, **derivado determinísticamente** y **editorial**; preservar procedencia y licencias.
- No inventar referencias, fuentes, morfología, traducciones ni atribuciones.
- El texto bíblico no se incrusta en los comentarios; se referencia por OSIS.
- Respetar estados `borrador`, `aprobado`, `publicado`; solo publicar tras revisión humana y según reglas de requisitos.
- Resolver pendientes bloqueantes del documento de requisitos antes de implementar los componentes afectados.

## 7. SDI y agent-native
- Integrar SDI desde el diseño; evitar duplicar su núcleo. Publicación verificable antes de notificar URLs.
- HTML legible para agentes sin JS, fuentes y procedencia explícitas, enlaces estables y datos estructurados coherentes.
- Considerar salidas estructuradas y MCP remoto/WebMCP según decisiones aprobadas; no hacerlos dependencias de la lectura humana.
- Probar recuperación, exactitud de citas y coherencia entre HTML y datos para agentes.

## 8. Calidad y entrega
- Validar esquemas, referencias OSIS, fuentes, enlaces internos, estados editoriales, accesibilidad y renderizado RTL/hebreo.
- Aplicar pruebas unitarias/E2E y presupuestos de rendimiento según la SDD aprobada.
- Documentar por qué se introduce cada dependencia relevante.
- Entregar un resumen corto: qué cambió, Issue/PR, pruebas, decisiones pendientes y riesgos.
- Si un hallazgo es menor y no bloquea, registrarlo y avanzar: **calidad sin parálisis**.

Documentos de consulta: `docs/requisitos.md`, `docs/decisiones/registro.md`, `docs/decisiones/README.md`, `docs/arquitectura-y-referencias.md`.
