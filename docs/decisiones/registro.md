# Decisiones compartidas

Última actualización: 2026-10-13.

| ID | Tema | Decisión | Estado | Autoridad / origen | Referencia |
|---|---|---|---|---|---|
| DEC-001 | Alcance | MVP Génesis 1–5; evolución gradual | Aprobada | Propietario | `docs/requisitos.md` |
| DEC-002 | Enfoque | Neutral, didáctico, con atribución de lecturas diferentes | Aprobada | Propietario | `docs/requisitos.md` |
| DEC-003 | Texto base | Reina-Valera 1909; edición y licencia digital por verificar | Aprobada con verificación pendiente | Propietario | RL-001 a RL-003 |
| DEC-004 | Interlineal | Hebreo, tokens, morfología, transliteración, glosas revisadas | Aprobada | Propietario | Sección 6 |
| DEC-005 | Lectura | Capítulo como experiencia principal; versículos individuales con contenido sustancial | Aprobada | Propietario | RF-024 a RF-032 |
| DEC-006 | Arquitectura | Astro SSG, contenido versionado en Git, validación tipada, sin base de datos en MVP | Aprobada conceptualmente | Propietario | Secciones 2, 7 y 10 |
| DEC-007 | Revisión | IA propone borradores; propietario aprueba antes de publicar | Aprobada | Propietario | Secciones 8 y 9 |
| DEC-008 | Roles | Propietario decide; ChatGPT consulta/audita; Codex y Claude Code implementan y aportan arquitectura | Aprobada | Propietario | `README.md` de este directorio |
| DEC-009 | SDI | Integración desde el inicio del proyecto | Intención aprobada; diseño pendiente | Propietario | `docs/arquitectura-y-referencias.md` |
| DEC-010 | Agent-native | Diseño para agentes desde el inicio | Intención aprobada; contratos pendientes | Propietario | `docs/arquitectura-y-referencias.md` |
| DEC-011 | Stack MVP | Astro 7 estático, Node 24 LTS, TS 6 compatible, Zod, Tailwind 4 para UI + CSS nativo editorial, sin islas, Vitest/Playwright/axe, GitHub Actions, Cloudflare Workers Static Assets sin SSR ni BD | Aprobada | Propietario, 2026-10-13 | [ADR-001 / Issue #2](https://github.com/Gunz-cop/ComentarioBiblico/issues/2) |
| DEC-012 | Persistencia SDI | Usar el SDI externo oficial, ejecutado tras deploy; estado persistente en rama dedicada, con serialización y controles de integridad; detalles operativos en SDD | Aprobada en principio; detalles pendientes | Propietario, 2026-10-13 | [ADR-001 / Issue #2](https://github.com/Gunz-cop/ComentarioBiblico/issues/2), [SDI](https://github.com/Gunz-cop/SDI) |
| DEC-013 | Interlineal: maqaf | Cada palabra es la unidad de análisis morfológico; la unión por maqaf (`־`) se conserva visible en la lectura hebrea (p. ej. `עַל־הָאָרֶץ`). El contrato de datos distinguirá palabra analizable, token gráfico y segmentos morfológicos. No autoriza resegmentar ni modificar el corpus fuente; los detalles técnicos se especifican y validan aparte | Aprobada (regla conceptual); contrato de datos pendiente | Propietario, 2026-10-13 | [PR #12, comentario 6157488991](https://github.com/Gunz-cop/ComentarioBiblico/pull/12#issuecomment-6157488991), [Issue #8](https://github.com/Gunz-cop/ComentarioBiblico/issues/8) |

## Propuestas abiertas

| ID | Propuesta | Estado | Siguiente acción |
|---|---|---|---|
| PROP-001 | Tailwind CSS 4, CSS moderno y TypeScript estricto | Aprobada en DEC-011 | Concretar versiones y configuración en SDD |
| PROP-002 | HTML sin JS como superficie primaria; JSON estructurado y posible MCP/WebMCP | Propuesta de diseño | Especificar contratos y pruebas agent-native |
| PROP-003 | Integrar SDI tras despliegue confirmado | Aprobada en DEC-012 | Diseñar recuperación, escritura y fallos de estado en SDD |
| PROP-004 | UI editorial con modos de lectura y estudio | Propuesta de UX | Benchmark y prototipo antes de aprobar |

## Plantilla para nuevas decisiones

```md
### DEC-XXX — Título
- Fecha:
- Estado: propuesta | aprobada | rechazada | supersedida
- Proponente:
- Contexto y problema:
- Opciones evaluadas:
- Recomendación y desacuerdos:
- Decisión del propietario:
- Consecuencias y riesgos:
- Evidencia / enlaces:
- Sustituye a (si aplica):
```
