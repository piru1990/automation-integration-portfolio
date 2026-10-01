# Allan Rosales — Automatización e integraciones

[English](README.en.md) · [Perfil](https://github.com/piru1990) · [Casos](CASES.es.md) · [Demos](DEMO-GUIDE.md)

Construyo automatizaciones e integraciones entre sistemas empresariales y resuelvo incidentes analizando su causa raíz. Mi experiencia documentada incluye Odoo, Microsoft 365/SharePoint, APIs, Cloudflare Workers y herramientas MCP.

Este portafolio presenta seis casos anonimizados respaldados por historial Git o notas de resolución, junto con tres demos independientes que se ejecutan sin credenciales.

## Casos destacados

| Caso | Aporte documentado | Evidencia revisada |
|---|---|---|
| [01 · Monitoreo de servicios](CASES.es.md#01-monitoreo-de-servicios-y-visibilidad-operativa) | Recolección histórica e integración de indicadores con Odoo | Historial Git y código |
| [02 · Dashboards SLA](CASES.es.md#02-actualización-automatizada-de-dashboards-sla) | Actualización programada y reintentos ante fallos temporales | Historial Git y código |
| [03 · Consistencia de flujos](CASES.es.md#03-automatización-de-controles-de-consistencia-en-flujos) | Implementación inicial de rutina programada | Historial Git y código |
| [04 · Consultas mediante MCP](CASES.es.md#04-integración-de-consultas-graphql-mediante-mcp) | Servidor Python para un backend GraphQL | Historial Git y código |
| [05 · Recuperación de build Odoo](CASES.es.md#05-recuperación-de-un-build-de-odoo-tras-una-regresión) | Diagnóstico, restauración y validación documentada | Git y ticket archivado |
| [06 · Integridad de datos ERP](CASES.es.md#06-diagnóstico-de-identidad-incorrecta-en-documentos-erp) | Diagnóstico y resolución de identidad incorrecta | Ticket archivado y comunicación |

## Demos ejecutables

Python 3.10+, sin paquetes externos ni conexiones a sistemas reales:

```sh
python3 monitor_demo.py
python3 sla_demo.py
python3 sync_demo.py
python3 -m unittest -v test_demos.py
```

Consulta las reglas, ejemplos y limitaciones en la [guía bilingüe](DEMO-GUIDE.md). Los tests cubren caídas, datos desconocidos, límites de SLA, exclusiones, persistencia y reintentos sin duplicados.

## Cómo interpretar la evidencia

Los casos describen trabajo histórico; las demos y los diagramas son reconstrucciones educativas creadas para este portafolio. Las fuentes corporativas, credenciales y datos personales permanecen privados. No se copió código empresarial. La licencia MIT cubre únicamente el contenido original publicado aquí.

La revisión encontró registros de HelpDesk desde diciembre de 2025 hasta septiembre de 2026. No se afirma cobertura de períodos anteriores ni se publica un total de tickets resueltos: asignaciones, cierres automáticos y registros archivados no bastan por sí solos para demostrar una resolución personal. Tampoco se atribuyen ahorros o mejoras porcentuales sin medición.

El trabajo se realizó en un entorno de equipo; se distingue mi aporte y se utilizan herramientas de asistencia cuando corresponde. Las fechas históricas se presentan en la documentación, sin reconstruir artificialmente el historial de contribuciones de GitHub.
