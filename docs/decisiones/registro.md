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

## Propuestas abiertas

| ID | Propuesta | Estado | Siguiente acción |
|---|---|---|---|
| PROP-001 | Tailwind CSS 4, CSS moderno y TypeScript estricto | Propuesta técnica | Validar compatibilidad y versionado estable en SDD |
| PROP-002 | HTML sin JS como superficie primaria; JSON estructurado y posible MCP/WebMCP | Propuesta de diseño | Especificar contratos y pruebas agent-native |
| PROP-003 | Integrar SDI tras despliegue confirmado | Propuesta de diseño | Definir disparadores y evitar notificar URLs inexistentes |
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
