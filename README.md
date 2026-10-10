# Mitanin Heat Desk 🌡️

### Predictive Wet-Bulb Triage & Decision-Support System for Frontline Health Workers

**Built for Environmental Hacks 2026 | Raipur, Chhattisgarh, India**

Mitanin Heat Desk is an environmental health decision-support dashboard designed to help community health workers (Mitanins) and municipal planners prioritize vulnerable households during extreme heat events in central India.

By combining predictive wet-bulb temperature modeling with household vulnerability indicators—including roof construction, age, pregnancy, living alone, and outdoor occupational exposure—the tool translates weather data into actionable triage queues and concise Hindi voice briefings.

---

## 🚀 Live Demo & Endpoints

- **Live Dashboard (AWS Amplify):** [Open Mitanin Heat Desk](https://main.d2e9o4nf8jvnh9.amplifyapp.com)
- **Serverless API (AWS Lambda):** [Open Demo API](https://jiy3g526lmitpenyg25tvbbhze0dsajn.lambda-url.ap-southeast-2.on.aws/?mitanin=M01&demo=hot)
- **GitHub Repository:** [heatguard-environmental-hacks](https://github.com/drishti1201/heatguard-environmental-hacks)

---

## 💡 Key Features

- **Predictive Wet-Bulb Analytics:** Evaluates wet-bulb temperatures using Open-Meteo forecasts to estimate environmental heat stress.
- **Multi-Factor Vulnerability Scoring:** Ranks synthetic households using roof materials (tin/asbestos versus pucca), age, living alone, pregnancy, and outdoor occupational exposure.
- **👷 Outdoor Worker Safe-Work Windows:** Supports planning work and rest periods around forecast heat conditions.
- **🏛️ Ward-Level Planning:** Aggregates household vulnerability indicators to help planners explore cool-roof interventions and heat-preparedness priorities.
- **⏪ Historical Weather Replay:** Supports exploring historical summer heatwaves using Open-Meteo historical weather archives, where implemented.
- **🔊 Automated Hindi Audio Briefings:** Generates concise field briefings using the Web Speech API, with optional Amazon Polly integration.

---

## ⚙️ How It Works

1. **Retrieve Weather Data:** Fetch hourly weather forecasts from Open-Meteo.
2. **Estimate Wet-Bulb Temperature:** Calculate estimated wet-bulb conditions from air temperature and humidity.
3. **Assess Heat Severity:** Evaluate forecast conditions against configured risk thresholds.
4. **Score Household Vulnerability:** Assess demographic, housing, and occupational risk factors.
5. **Prioritize Households:** Rank synthetic demonstration households by estimated heat risk.
6. **Generate Hindi Briefings:** Summarize heat conditions and household priorities for frontline workers.
7. **Support Field Actions:** Track visits and ORS distribution where the functionality is enabled.

---

## 🏗️ System Architecture

```text
        +----------------------------------+
        |     Frontline Health Worker      |
        |      Mobile / Web Browser        |
        +----------------+-----------------+
                         |
                         v
        +----------------------------------+
        |       AWS Amplify Hosting        |
        |       HTML, CSS, JavaScript      |
        +----------------+-----------------+
                         |
                         v
        +----------------------------------+
        |     AWS Lambda API Handler       |
        |          Python 3.12             |
        +-----------+----------------------+
                    |
          +---------+----------+
          |                    |
          v                    v
+--------------------+  +----------------------+
| Open-Meteo API     |  | Synthetic Household  |
| Forecast / Archive |  | Vulnerability Data   |
+--------------------+  +----------------------+
          |                    |
          +----------+---------+
                     |
                     v
        +----------------------------------+
        | Wet-Bulb Estimation & Risk       |
        | Scoring Engine                   |
        +----------------+-----------------+
                         |
                         v
        +----------------------------------+
        | Household Prioritization &       |
        | Hindi Voice Briefing             |
        +----------------+-----------------+
                         |
              +----------+----------+
              |          |          |
              v          v          v
          Browser     Amazon     Amazon
          Speech      Polly      DynamoDB
          API         Optional   Optional
                         |
                         v
                      Amazon S3
                      Optional
```

### Architecture Components

- **Frontend:** Single-page dashboard using HTML, CSS, and JavaScript.
- **Hosting:** AWS Amplify.
- **Backend:** Python-based AWS Lambda function exposed through a Lambda Function URL.
- **Weather Source:** Open-Meteo forecast and historical weather APIs.
- **Risk Engine:** Python modules for wet-bulb estimation and household vulnerability scoring.
- **Voice Output:** Browser Speech Synthesis API, with optional Amazon Polly.
- **Optional Persistence:** Amazon S3 for generated audio and Amazon DynamoDB for visit logging.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Frontend | HTML, CSS, JavaScript |
| Frontend Hosting | AWS Amplify |
| Serverless Backend | AWS Lambda |
| API Endpoint | AWS Lambda Function URL |
| Weather Data | Open-Meteo API |
| Wet-Bulb Estimation | Python |
| Vulnerability Scoring | Python |
| Browser Voice Playback | Web Speech / Speech Synthesis API |
| Optional Voice Generation | Amazon Polly |
| Optional Audio Storage | Amazon S3 |
| Optional Visit Logging | Amazon DynamoDB |
| Development & Deployment | AWS SAM CLI, AWS CLI |
| Testing | Python unit tests, pytest |

---

## 📁 Repository Structure

```text
heatguard-environmental-hacks/
├── data/
│   ├── generate_households.py   # Synthetic household generation
│   └── households.json          # Synthetic demographic and housing records
├── infra/
│   ├── DEPLOY.md                # AWS deployment guide
│   └── build.sh                 # SAM/Lambda packaging script
├── src/
│   ├── lambda/
│   │   └── handler.py           # Lambda routing and briefing generation
│   ├── risk/
│   │   ├── scoring.py            # Household vulnerability scoring
│   │   └── wetbulb.py            # Wet-bulb estimation and heat curves
│   └── web/
│       └── index.html            # Single-page dashboard
└── tests/
    └── test_risk.py              # Risk scoring and threshold tests
```

### Important Files

- `data/generate_households.py` — Generates synthetic household records.
- `data/households.json` — Stores synthetic demographic and housing-risk attributes.
- `infra/DEPLOY.md` — Contains deployment instructions.
- `infra/build.sh` — Prepares the backend deployment package.
- `src/lambda/handler.py` — Handles API requests and generates briefings.
- `src/risk/scoring.py` — Calculates household vulnerability scores.
- `src/risk/wetbulb.py` — Estimates wet-bulb temperature and models heat curves.
- `src/web/index.html` — Implements the dashboard interface.
- `tests/test_risk.py` — Tests risk-scoring and threshold logic.

---

## 🧪 Testing & Deployment

### Run Local Tests

```bash
python -m pytest tests/test_risk.py
```

Ensure Python and the project's required dependencies are installed before running the tests.

### AWS Deployment

The repository includes deployment guidance and a build script in the `infra/` directory.

- **AWS Amplify:** Frontend hosting.
- **AWS Lambda:** Serverless backend processing.
- **AWS SAM CLI:** Local development, testing, and deployment support.

The live application and API are linked above. Optional AWS integrations require their respective resources, permissions, and configuration.

---

## 🔒 Responsible Data & Security

- **Synthetic Data Only:** Household entries are synthetic demonstration data and do not represent real individuals or clinical records.
- **Privacy:** Do not upload real household details, patient information, or personally identifiable information.
- **Credential Safety:** Never commit AWS access keys, secret keys, tokens, or other credentials.
- **Access Controls:** Configure appropriate IAM permissions and resource policies before enabling optional AWS services for broader use.
- **Public Endpoint:** Use the demonstration API with synthetic data only.

---

## ⚠️ Limitations & Disclaimer

- **Decision Support Only:** Risk indices are estimates intended to assist triage planning and are not clinical diagnoses.
- **Official Guidance:** The system must not replace official IMD heat warnings, public-health advisories, emergency protocols, or professional medical advice.
- **Forecast Uncertainty:** Forecasts and estimated wet-bulb temperatures may differ from actual local conditions.
- **Scientific Validation:** Risk thresholds and vulnerability weights should be validated against appropriate scientific and public-health guidance before operational use.
- **Feature Availability:** Historical replay, ward-level aggregation, safe-work windows, and optional AWS integrations should be considered available only where implemented and verified.

---

## 🌍 Expected Impact

Mitanin Heat Desk aims to help communities:

- **Prioritize vulnerable households** during extreme heat events.
- **Improve preventive outreach** using forecast-based risk estimates.
- **Support outdoor worker safety** through heat-aware work and rest planning.
- **Inform ward-level planning** for housing and cooling interventions.
- **Improve field accessibility** through concise Hindi voice briefings.
- **Strengthen heat preparedness** through data-informed decision support.

The long-term vision is to support more proactive, accessible, and locally informed community heat-health preparedness.

---

## 👥 Hackathon Project

**Event:** Environmental Hacks 2026

**Project:** Mitanin Heat Desk — Predictive Wet-Bulb Triage & Decision-Support System for Frontline Health Workers.

**Focus Areas:** Environmental health, extreme-heat preparedness, community healthcare, and responsible technology.

---

**Disclaimer:** This project is a hackathon prototype. It has not been established as a clinically validated or officially approved heat-health triage system.
