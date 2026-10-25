# Deployable services

Read only for an API, worker, consumer, or scheduled job.

A deployable service (API, worker, consumer, scheduled job) follows the [Twelve-Factor App](https://12factor.net):
   - **II** dependencies declared in the manifest and lockfile; nothing relies on a host-installed tool
   - **III** config (URLs, credentials, flags, limits) read from the environment at startup, validated, fail fast if missing; no config in code, no per-environment files, no secrets in the repo. Convention over configuration keeps the list short: a setting exists only when deployments truly differ on it.
   - **IV** databases, queues, caches, third-party APIs are attached resources located by config
   - **VI** stateless and share-nothing; session, cache and upload state lives in a backing service
   - **VII** binds a port taken from config
   - **IX** fast startup; on `SIGTERM` stop accepting work, drain, close connections; jobs are safe to retry after a crash
   - **X** the same kinds of backing services in dev and test as in prod (a real Postgres in a container, not SQLite)
   - **XI** an unbuffered log stream to stdout; no log files or rotation in the app
   - **XII** migrations and one-off tasks are separate commands against the same code and config
   - **I** one codebase, **V** build / release / run kept separate, **VIII** scaling by process type: these belong to the repo and deploy pipeline; don't break them (for example, no config baked into a build artifact)

   A waived factor is an `ADR` in your brief; anything else you can't meet is a `⚠` in your report.
