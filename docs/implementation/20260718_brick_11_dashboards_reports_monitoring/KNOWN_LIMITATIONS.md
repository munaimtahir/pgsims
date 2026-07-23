# Known Limitations - Brick 11: Dashboards, Reports, and Exports

1. **Large query counts pagination**: Large report listings (e.g. evaluating 10,000 records) are not explicitly paginated on the frontend, relying on basic list query sizing. Should load metrics rise in the future, standard DRF pagination controls can be easily applied.
2. **Browser Print styling**: Report print views are configured via standard browser media query prints. No custom PDF generation templates are bundled, as inline browser print features provide high fidelity layout mapping.
