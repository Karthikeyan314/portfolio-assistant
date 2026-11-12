# Work experience

## Autodesk: Data Analytics Engineer (February 2025 to present, Bangalore)

Develops and validates Snowflake SQL transformations, analytical data models and Power BI reporting for customer success, product adoption, support and renewal performance.

- Built Snowflake-backed support and issue-resolution reporting. Led source-data validation during the migration from legacy sources, worked with engineering on Salesforce field mappings, and secured stakeholder approval for the issue-resolution reporting.
- Builds historical account dimensions using SCD2 techniques and point-in-time (effective-date) logic, with reconciliation checks for finance, customer cohorts and schema migrations.
- Reconciles finance, engagement and customer-cohort metrics, investigates reporting discrepancies, and supports schema migrations and scheduled refresh workflows.
- Created a curated-data refresh pattern that the team reuses.
- Led a three-person first-stage dashboard QA group covering data checks, labels and reporting consistency.
- Completed Gainsight UAT ahead of schedule.
- Develops Python tools for dashboard comparison and for controlled QBR (quarterly business review) deck updates, using source manifests and checks that preserve historical content and presentation structure.
- Built and maintains Scout, a Copilot Studio analytics assistant connected to Snowflake and documented business definitions (see the Scout section).
- Built and evaluated a churn-prediction model. The business adopted a simpler cohort-based approach rather than productionizing the model (see the machine learning section).

## Autodesk: how Karthikeyan keeps numbers right

At Autodesk, Karthikeyan's data checks work in layers:

- **Pipeline tests:** checks built into the data pipeline for keys, completeness and expected values.
- **Post-build checks:** after a pipeline is built and has run, Karthikeyan runs checks to make sure the numbers stay the same as before, catching unintended changes from code edits or migrations.
- **Refresh-over-refresh QC:** as lead of the dashboard QA group, Karthikeyan compares each month's refresh against the previous month's, using data taken directly from the Snowflake tables, so a number that leadership already saw cannot change silently.
- **Alerting:** Karthikeyan set up email notifications that flag failed refresh tasks, so problems are seen before users find them.

Karthikeyan's public bank data platform project rebuilds these same ideas on open data: a blocking quality gate, dbt tests, refresh-over-refresh QC and alerts.

## ExxonMobil: Product Analyst (June 2023 to January 2025, Bangalore)

Developed the Lubricants Direct and Distributor Voice of Customer (VoC) dashboard, bringing customer-feedback reporting into a common view for customer-experience analysis. Used Tableau and SQL to analyze feedback themes, experience trends and recurring pain points. Worked with customer-experience stakeholders on reporting requirements and data validation, translating business questions into dashboards and analysis.

## ExxonMobil: Business Analyst (May 2022 to June 2023, Bangalore)

Partnered with sales, supply-chain and S&OP (sales and operations planning) teams to turn business requirements into analytical datasets, Tableau dashboards and custom reporting. Used SQL and Python to prepare and validate operational data.

- Migrated annual sales stewardship reporting from Excel to automated Tableau dashboards.
- Automated the manual data inputs feeding the E2E (end-to-end) Supply Chain dashboard, in partnership with S&OP. This work received global recognition.
- Served as a subject matter expert for data validation and reporting.

## apna: Validation Expert (October 2021 to May 2022, Bangalore)

Managed incoming job postings from across India and reviewed submissions against the platform's safety standards, working to a 30-minute service-level target and balancing turnaround with content-validation requirements.

## Basidia: Subject Matter Expert (June 2021 to October 2021, Bangalore)

Worked closely with the COO to curate physics educational content for students preparing for NEET, India's medical entrance exam.
