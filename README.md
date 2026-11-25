# ♻️ WasteWise AI
## AI-Powered Manufacturing Loss, Rework & Predictive Waste Intelligence

> **Turn factory data into actionable waste intelligence. Predict losses before they happen.**

WasteWise AI is an AI-powered decision-support application designed for food manufacturing. It combines production data, waste records, operational documents and machine learning to help manufacturing teams identify losses, investigate contributing factors, anticipate high-risk production batches and make better operational decisions.

The platform moves beyond traditional waste reporting by introducing predictive modelling, allowing production teams to assess potential waste risks using patterns identified in their own historical production data.

---

## The Problem

Food manufacturers often have valuable operational information scattered across:

- CSV and Excel production records
- Waste and loss logs
- Quality-control records
- Standard Operating Procedures (SOPs)
- Operational manuals
- Employee knowledge

The challenge is not simply collecting information. It is transforming fragmented production data into meaningful, evidence-based decisions.

Manufacturing teams need to understand:

- Where are production losses occurring?
- Which products, lines and shifts are most affected?
- What are the major waste drivers?
- How much material is being lost?
- What does the factory's own SOP recommend?
- Which production batches are likely to generate significant waste?
- What should the team investigate or address next?

---

## Our Solution

WasteWise brings production analytics, AI-assisted investigation and predictive modelling into one integrated workflow.

```text
       Production Data (CSV / XLSX)
                    |
                    v
             Data Processing
                    |
          +---------+----------+
          |                    |
          v                    v
    Python Analytics     Machine Learning
          |                    |
          |              Waste Prediction
          |                    |
          +---------+----------+
                    |
                    v
             Waste Intelligence
                    |
          +---------+----------+
          |                    |
          v                    v
     AI / Groq Analysis    SOP Intelligence
          |                    |
          +---------+----------+
                    |
                    v
         Investigation & Action
```

The platform follows:

> **Upload → Analyze → Predict → Investigate → Improve**

---

## Core Features

### 1. Production Data & Mapping

Upload factory production and waste data in:

- CSV
- XLSX
- XLS

WasteWise provides:

- Data validation
- Dataset previews
- Automatic column mapping
- Standardized data fields
- Missing-value and duplicate-record checks

The application allows different factory datasets to be mapped into a common analytical structure.

### 2. Manufacturing KPI Dashboard

Provides an overview of manufacturing performance through:

- Total production
- Total waste/loss
- Overall loss rate
- Production performance indicators

### 3. Loss Analysis

Identifies and analyses manufacturing losses across different operational dimensions:

- Loss by product
- Loss by production line
- Loss by shift
- Loss by category
- Loss by reason
- Loss trends over time
- Comparative waste-rate analysis

This helps identify where the greatest material losses are occurring.

### 4. Investigation Intelligence

Helps manufacturing teams identify combinations of products, production lines and shifts associated with significant losses.

The module supports investigation prioritisation by highlighting operational areas that deserve further attention.

### 5. Anomaly Detection

Identifies unusually high-loss production records and highlights observations that may require investigation.

The purpose is to help teams distinguish ordinary production variation from potentially significant loss events.

### 6. Predictive Waste Intelligence

WasteWise introduces machine learning to move from retrospective waste analysis towards proactive waste-risk assessment.

Unlike conventional analytics, which examines losses after they occur, predictive modelling uses historical production patterns to assess the likelihood of significant waste in an upcoming batch.

**How it works:**

1. The user uploads historical production and waste records.
2. WasteWise prepares the data for machine learning.
3. A predictive model is trained using the uploaded records.
4. The user enters the operating conditions of a new production batch.
5. The model evaluates the batch and generates a waste-risk classification.

**Initial prediction inputs:**

| Input | Description |
|---|---|
| Production Line | Manufacturing line |
| Shift | Production shift |
| Product | Product being manufactured |
| Production Quantity | Planned production in kg |
| Seal Temperature | Operating seal temperature in °C |

**Prediction objective:**

The initial model uses a binary classification approach:

- **Low Risk:** Predicted waste below 200 kg.
- **High Risk:** Predicted waste of 200 kg or more.

**Machine Learning Approach:**

The initial implementation uses a Random Forest Classifier with:

- Categorical feature encoding
- Numerical missing-value imputation
- Class-weighted model training
- Stratified cross-validation
- Confusion matrix analysis
- Accuracy, precision, recall and F1-score evaluation

High-risk recall receives particular attention because failing to identify a potentially high-waste batch can be more consequential than generating an unnecessary warning.

**Data Privacy & Model Handling:**

Predictive modelling follows an upload-based approach.

- Users provide their own historical production dataset.
- The model is trained using the uploaded data.
- No permanent historical dataset is bundled with the application.
- No trained model file is required in the GitHub repository.
- The trained model is maintained in the active application session.
- Uploading a new dataset requires a new model training process.

The dataset and trained model are not intentionally written to the project repository or permanent application storage by the predictive module.

**Important:** The predictive model provides decision support, not guaranteed waste outcomes. Its reliability depends on the quality, completeness and representativeness of the uploaded historical data.

### 7. SOP Intelligence with RAG

WasteWise allows users to upload factory SOPs and operational documents in PDF format.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents.

```text
PDF / SOP
    |
    v
Text Extraction
    |
    v
Document Chunking
    |
    v
Embeddings
    |
    v
Vector Search
    |
    v
Relevant Evidence
    |
    v
AI-Generated Answer
```

Document-based answers use retrieved information to support operational understanding and investigation.

### 8. AI Analyst

Groq-powered natural-language analysis helps users interpret manufacturing data and retrieved document evidence.

Example questions:

- Which production line should we investigate first?
- What are the main waste drivers?
- Which products are contributing most to losses?
- What does the SOP recommend?
- What operational factors should be investigated?

The AI analyst is intended to connect numerical findings with relevant operational information.

---

## Manufacturing Loss & Rework Model

WasteWise is designed to distinguish different types of manufacturing outcomes rather than treating everything as generic food waste.

The broader manufacturing model can represent:

- Production
- Process loss
- Material loss
- Packaging loss
- Quality deviation
- Rework
- Recovery
- Final loss

For example:

```text
Production
    |
    v
Quality Deviation
    |
    v
Rework
    |
    +----> Recovered Material
    |              |
    |              v
    |        Saleable Product
    |
    v
Final Loss
```

This allows WasteWise to investigate questions such as:

- Which quality deviations generate the most rework?
- Which rework events ultimately result in final loss?
- Which products require the most rework?
- Where is the greatest financial impact occurring?

---

## AI Trust & Safety

WasteWise is a decision-support system, not an autonomous factory-control system.

The application distinguishes between:

| Type | Example |
|---|---|
| FACT | A production line recorded a particular loss rate. |
| INFERENCE | The findings may be related to operating conditions. |
| PREDICTION | A new batch is classified as high waste risk. |
| RECOMMENDATION | Review the relevant production and calibration records. |

WasteWise must not:

- Invent production measurements.
- Present hypotheses as confirmed root causes.
- Invent SOP requirements.
- Guarantee predictive outcomes.
- Make autonomous product-disposal decisions.
- Make autonomous quality-approval decisions.

When evidence is insufficient, the system should communicate that clearly.

---

## Technology Stack

### Frontend
- Streamlit

### Data Processing
- Python
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- One-Hot Encoding
- Stratified Cross-Validation

### Documents
- PyPDF

### Retrieval
- FAISS
- Embeddings
- Vector Search

### AI
- Groq
- Natural-language reasoning
- Retrieval-Augmented Generation

### Development
- GitHub
- Google Colab for experimentation when useful

### Deployment
- Streamlit Community Cloud

---

## Project Architecture

```text
                    USER
                      |
                      v
              WASTEWISE AI
                      |
         +------------+------------+
         |                         |
         v                         v
    DATA UPLOAD                PDF / SOP
     CSV / XLSX                    |
         |                         v
         v                    RAG PIPELINE
   DATA PROCESSING                  |
         |                         |
    +----+---------+                |
    |              |                |
    v              v                |
 ANALYTICS    MACHINE LEARNING      |
    |              |                |
    |         WASTE PREDICTION      |
    |              |                |
    +-------+------+----------------+
            |
            v
       GROQ REASONING
            |
            v
    WASTEWISE INSIGHTS
            |
            v
   HUMAN INVESTIGATION
```

The architecture intentionally avoids unnecessary infrastructure so that the application remains practical, maintainable and achievable within its development scope.

---

## Predictive Modelling Workflow

To use Predictive Waste Intelligence:

**Step 1 – Upload Historical Data**

Navigate to Data & Mapping and upload a historical production dataset.

**Step 2 – Confirm Column Mapping**

Ensure that the required predictive fields are correctly mapped.

**Step 3 – Train the Model**

Navigate to Predictive Waste Intelligence and select the model training option.

**Step 4 – Evaluate Performance**

Review the model's cross-validation metrics and confusion matrix.

**Step 5 – Enter a New Production Batch**

Provide the production conditions of the upcoming batch.

**Step 6 – Generate a Prediction**

WasteWise generates a high-risk or low-risk classification and an estimated high-risk score.

**Step 7 – Investigate**

Use the prediction as an early warning to review relevant production conditions and operational procedures.

---

## Model Limitations

The initial predictive model is a prototype intended for experimentation and decision support.

Its performance depends on:

- Historical data quality
- Number of available production records
- Representation of high-risk and low-risk batches
- Missing and inconsistent observations
- Changes in production conditions over time

Cross-validation provides an initial performance estimate, but future production records should be used for independent chronological validation.

The initial classification model predicts waste-risk categories. It does not directly estimate the exact quantity of waste in kilograms.

Future development may introduce regression-based waste quantity prediction.

---

## Demo Workflow

The intended demonstration flow is:

```text
1. Upload factory production data
            |
            v
2. Explore manufacturing KPI dashboard
            |
            v
3. Analyse manufacturing losses
            |
            v
4. Investigate significant loss patterns
            |
            v
5. Upload an SOP document
            |
            v
6. Ask WasteWise an operational question
            |
            v
7. Upload historical data for predictive modelling
            |
            v
8. Train and evaluate the model
            |
            v
9. Predict the risk of a new production batch
            |
            v
10. Generate actionable investigation insights
```

Synthetic demonstration data may be used where actual factory records are unavailable.

---

## MVP Scope

The WasteWise MVP focuses on:

- CSV and Excel uploads
- Data validation and mapping
- Manufacturing-loss analytics
- KPI dashboard
- Loss analysis
- Investigation prioritisation
- Basic anomaly detection
- PDF/SOP upload
- Retrieval-Augmented Generation
- Natural-language AI analysis
- Predictive waste-risk classification
- Model performance evaluation
- New batch risk assessment

The development principle is:

> **WORKING > SIMPLE > RELIABLE > IMPRESSIVE > COMPLEX**

---

## Future Roadmap

WasteWise is intended to evolve from manufacturing-loss intelligence into a broader AI-powered manufacturing operations platform.

```text
Waste Intelligence
        |
        v
Predictive Waste
        |
        v
Waste Quantity Forecasting
        |
        v
Yield Intelligence
        |
        v
Inventory & Expiry Intelligence
        |
        v
Quality Intelligence
        |
        v
Computer Vision
        |
        v
Production Optimization
        |
        v
Factory Digital Twin
        |
        v
AI Factory Operations OS
```

The long-term vision is to help food manufacturers move from identifying losses to anticipating, understanding and preventing them.

---

## Development Philosophy

WasteWise is developed in controlled phases:

```text
PLAN
  |
  v
BUILD
  |
  v
RUN
  |
  v
TEST
  |
  v
FIX
  |
  v
CHECKPOINT
  |
  v
NEXT PHASE
```

The data and analytics foundation is built before introducing more advanced AI and predictive capabilities.

This reduces technical risk and makes the application easier to test, maintain and improve.

---

## License

No open-source license has been selected for this repository yet.
