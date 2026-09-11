# P3 debt disposition

## Legacy routes

The Django dashboard routes under `sims/users/urls.py` remain reachable and are referenced by
backend tests, redirects, and compatibility documentation. Repository-wide proof of zero use is
therefore absent. They are retained and explicitly classified as compatibility debt.

## `User.supervisor`

The field remains because legacy search, attendance, case, and import code still reads it. New
canonical supervision code uses `ResidentSupervisorAssignment` and `SupervisorProfile`; the field
is marked deprecated in the model and must not be used to widen authorization.

## Ruff and generic exceptions

Ruff was run against `backend/sims` and reported 2,663 findings, largely executable legacy modules,
migrations, import ordering, mutable class attributes, and broad exception handling. A blanket
`ruff --fix` would create a large unreviewed change and may affect compatibility modules, so no
bulk fix was applied. Functional narrowing is deferred to a dedicated cleanup change.

## Test fixtures

The temporary verification secret is supplied only through the shell environment and is not stored
in the repository. Existing fixture passwords remain test data and are not production credentials.
