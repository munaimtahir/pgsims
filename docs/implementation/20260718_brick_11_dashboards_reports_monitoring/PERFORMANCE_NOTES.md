# Performance Notes - Brick 11: Dashboards, Reports, and Exports

## Query Optimizations
1. **Model pre-fetching**:
   - `EvaluationSubmission` query uses `select_related` on `resident__user`, `supervisor__user`, `template`, and `training_record`.
   - `LogbookEntry` query uses `select_related` on `resident__user`, `supervisor__user`, `category`, and `training_record`, and prefetches `procedure_record` inline.
2. **Aggregations over loops**: Dashboard counts use database-level `Count` aggregations and `values_list` lookups rather than in-memory loops.
3. **Indices**: Query filtering maps to indexed foreign keys (resident, supervisor, template) for fast pagination and subset lookups.
