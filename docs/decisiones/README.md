# Registro de decisiones — Comentario Bíblico

Este directorio contiene las decisiones compartidas entre el propietario, ChatGPT, Codex y Claude Code.

## Autoridad y proceso
- **Propietario:** define prioridades, acepta riesgos y aprueba decisiones, contenido y publicación.
- **ChatGPT:** consultor arquitectónico, investigación, análisis de alternativas y auditoría independiente.
- **Codex:** implementación, pruebas, especificaciones SDD y arquitectura cuando se le encargue.
- **Claude Code:** implementación, SDD, auditoría y criterio arquitectónico independiente.
- Ningún agente aprueba en nombre del propietario. Las propuestas de agentes no son decisiones aceptadas.
- Ante contradicción: decisión aprobada más reciente > requisitos aprobados > propuestas; los cambios a requisitos requieren aprobación explícita.
- Evitar rondas infinitas: una observación no bloqueante se registra para después; solo se reabre una decisión ante evidencia nueva, riesgo crítico o cambio de alcance.

## Flujo
1. Registrar propuesta y alternativas con su motivación.
2. Recoger evaluación de los agentes pertinentes, incluyendo desacuerdos.
3. El propietario decide: **propuesta**, **aprobada**, **rechazada** o **supersedida**.
4. Documentar impacto, fecha y enlaces a PR/Issue/requisitos.
5. Si afecta a código o requisitos, implementar mediante PR separado y pruebas.

## Archivos
- [Decisiones compartidas](./registro.md): acuerdos y pendientes.
- [Arquitectura técnica y referencias](../arquitectura-y-referencias.md): orientación técnica y de producto; no sustituye requisitos.

No registrar como aprobado lo que solo haya sido sugerido en una conversación.
