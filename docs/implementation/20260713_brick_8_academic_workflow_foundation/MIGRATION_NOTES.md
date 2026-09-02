# Brick 8 Migration Notes

- Strategy used: clean forward migration.
- No historical production academic data was preserved or migrated.
- Existing Brick 6 master-catalog data remains in `sims.academics`.
- New Brick 8 foundation models are additive and isolated under `/api/academics/*`.
