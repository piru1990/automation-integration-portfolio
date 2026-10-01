# Demos / Demonstrations

[Español](README.md) · [English](README.en.md)

## Español

Ejemplos independientes creados para este portafolio. No contienen código empresarial ni se conectan a sistemas reales. Requieren Python 3.10 o superior y usan únicamente la biblioteca estándar.

```sh
python3 monitor_demo.py
python3 sla_demo.py
python3 sync_demo.py
python3 -m unittest -v test_demos.py
```

- **Monitoreo:** historial ficticio con estados `up`, `down` y `unknown`. La disponibilidad es la proporción de muestras conocidas exitosas; no representa tiempo real de disponibilidad ni un SLA de producción. Las muestras desconocidas se reportan por separado. Un timeout se clasifica como caída; otro error de la sonda, como desconocido.
- **SLA:** objetivo ilustrativo de 24 horas transcurridas, sin calendario laboral. El cierre exactamente en el límite cumple. Solo cuentan tickets resueltos; abiertos, cancelados y duplicados se excluyen. Sin casos resueltos, los porcentajes y el promedio son `null`.
- **Sincronización:** flujo unidireccional de tickets ficticios a tareas simuladas, con clave estable `helpdesk:<id>`. Repetir el proceso no duplica tareas; cambiar un ticket actualiza su tarea. No cierra tickets reales. Un adaptador real necesitaría control de concurrencia, paginación y política de reintentos.

Para probar persistencia entre ejecuciones:

```sh
python3 sync_demo.py --store /tmp/portfolio-demo-tasks.json
python3 sync_demo.py --store /tmp/portfolio-demo-tasks.json
```

La segunda ejecución debe mostrar cero creaciones. El archivo indicado contiene únicamente tareas ficticias. Los resultados numéricos de estas demos no son métricas de mi trabajo profesional.

## English

Independent examples created for this portfolio. They contain no employer source code and do not connect to real systems. Python 3.10+ is required; only the standard library is used. Run the commands above.

- **Monitoring:** synthetic history with `up`, `down`, and `unknown` states. Availability is the share of successful known samples, not measured uptime duration or a production SLA. Unknown samples are reported separately. A probe timeout means down; another probe error means unknown.
- **SLA:** illustrative target of 24 elapsed hours, without a business calendar. Closure exactly at the deadline meets the target. Only resolved tickets count; open, cancelled, and duplicate records are excluded. With no resolved tickets, percentages and mean are `null`.
- **Synchronization:** one-way flow from fictitious tickets to mock tasks, keyed by `helpdesk:<id>`. Replays do not create duplicates; changed tickets update their tasks. No real tickets are closed. A real adapter would require concurrency control, pagination, and a retry policy.

The optional `--store` commands above persist mock tasks across runs; the second run should create none. All demo numbers are synthetic and are not professional impact metrics.
