# Allan Rosales — Automation & integrations

[Español](README.md) · [Profile](https://github.com/piru1990) · [Case studies](CASES.en.md) · [Demos](DEMO-GUIDE.md)

I build automation and integrations between business systems and resolve incidents through root cause analysis. My documented experience includes Odoo, Microsoft 365/SharePoint, APIs, Cloudflare Workers, and MCP tools.

This portfolio presents six anonymized case studies supported by Git history or resolution notes, alongside three independent demos that run without credentials.

## Selected case studies

| Case | Documented contribution | Evidence reviewed |
|---|---|---|
| [01 · Service monitoring](CASES.en.md#01-service-monitoring-and-operational-visibility) | Historical collection and indicator integration with Odoo | Git history and code |
| [02 · SLA dashboards](CASES.en.md#02-automated-sla-dashboard-refresh) | Scheduled refresh and transient-error retries | Git history and code |
| [03 · Workflow consistency](CASES.en.md#03-workflow-consistency-automation) | Initial scheduled routine implementation | Git history and code |
| [04 · MCP queries](CASES.en.md#04-graphql-query-integration-through-mcp) | Python server for a GraphQL backend | Git history and code |
| [05 · Odoo build recovery](CASES.en.md#05-odoo-build-recovery-after-a-regression) | Diagnosis, restoration, and documented validation | Git and archived ticket |
| [06 · ERP data integrity](CASES.en.md#06-diagnosis-of-incorrect-identity-on-erp-documents) | Incorrect identity diagnosis and resolution | Archived ticket and communication |

## Runnable demos

Python 3.10+, with no external packages or connections to real systems:

```sh
python3 monitor_demo.py
python3 sla_demo.py
python3 sync_demo.py
python3 -m unittest -v test_demos.py
```

See the [bilingual guide](DEMO-GUIDE.md) for rules, examples, and limitations. Tests cover outages, unknown data, SLA boundaries, exclusions, persistence, and duplicate-free retries.

## Interpreting the evidence

Case studies describe historical work; demos and diagrams are educational reconstructions created for this portfolio. Corporate sources, credentials, and personal data remain private. No employer source code was copied. The MIT license covers only the original content published here.

The review found HelpDesk records from December 2025 through September 2026. Coverage of earlier periods is not claimed, and no personal resolved-ticket total is published: assignments, automated closures, and archived records alone do not prove a personal resolution. Savings and percentage improvements are not claimed without measurement.

Work took place in a team environment; my contributions are distinguished, and assistance tools are used where applicable. Historical dates appear in documentation without artificially reconstructing the GitHub contribution history.
