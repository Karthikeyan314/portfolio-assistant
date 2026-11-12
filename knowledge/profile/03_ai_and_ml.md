# AI and machine learning work

## Scout: conversational analytics assistant

Scout is a conversational analytics assistant that Karthikeyan built and maintains at Autodesk. A business user asks a question in plain language; Scout writes SQL against Snowflake, runs it, and answers with a short analysis grounded in the results.

How it is built:

- **Platform:** Microsoft Copilot Studio with generative orchestration. The model composes the SQL, guided by a detailed instruction layer and a knowledge base.
- **Execution:** a Power Automate flow runs the SQL against Snowflake through the certified connector and returns the rows, which the model turns into a plain-language answer.
- **Reports:** a second flow renders branded HTML reports, and a custom Azure Function (Python) converts them into PowerPoint decks.
- **Grounding (retrieval-augmented generation):** Scout retrieves from a curated knowledge base of documented business definitions before it answers, including fiscal-calendar logic.

## Scout: engineering against hallucination and risk

Language models tend to invent table and column names. Karthikeyan addressed this with engineering, not only prompting:

- A single source-of-truth schema registry, distilled from the underlying BI models, with a strict "registry wins" rule, and a requirement that the model verify names against the schema before querying.
- Multi-layer error handling with retry and escalation.
- A guardrail that allows only a single SQL statement per execution.
- Rules that never expose raw customer identifiers.
- Error telemetry.
- Karthikeyan turned off the code interpreter after it leaked raw code into the chat, and documented the fix.

## Churn-prediction model

At Autodesk, Karthikeyan built and evaluated a supervised churn-propensity model that scores customer accounts on renewal risk, end to end from Snowflake data through evaluation.

- **Features:** an account-by-quarter panel from engagement, support, finance and renewal sources, such as utilization and assignment rates, support cases per seat, customer-effort scores, quarter-over-quarter trends and prior renewal history.
- **Leakage control:** features are lagged one quarter, so they always predate the outcome.
- **Models:** an interpretable logistic-regression baseline alongside a gradient-boosted tree model (scikit-learn HistGradientBoosting), with balanced class weights.
- **Validation:** a time-based split (train on earlier quarters, test on the most recent complete quarter), reporting train-versus-test AUC and the overfit gap, PR-AUC, and a confusion matrix with precision, recall and F1.

**Outcome:** the model was built and validated but not put into production. The business chose a simpler, more interpretable cohort analysis for rollout. Karthikeyan's takeaway is that the most sophisticated model is not always the one that ships: interpretability and operational fit matter. The plan for productionizing it would add scheduled retraining, probability calibration, a serving endpoint and drift monitoring.

## Indian dog-breed detector

A personal computer-vision project: a model that recognizes Indian dog breeds, covering the full loop from collecting and annotating images to training the model. The project is public on Roboflow.
