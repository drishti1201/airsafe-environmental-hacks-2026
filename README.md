# Mitanin Heat Desk 🌡️
### Predictive Wet-Bulb Triage & Automated Voice Briefing System for Community Health Workers

**Built for Environmental Hacks 2026 | Raipur, Chhattisgarh, India**

Mitanin Heat Desk is a **heat-risk decision-support tool** designed to help community health workers (Mitanins) identify and prioritize households that may be more vulnerable during extreme heat events.

By combining weather forecasts, wet-bulb temperature estimation, household vulnerability scoring, and Hindi voice briefings, the system helps frontline health workers plan timely visits and take preventive action.

---

## 🎯 The Challenge

Extreme heat poses serious health risks, particularly during pre-monsoon heat events in central India. High temperatures combined with humidity can increase heat stress, potentially leading to heat exhaustion, heatstroke, and cardiovascular complications.

Community health workers often monitor hundreds of households, including older adults living alone, infants in poorly insulated homes, and outdoor workers. Without a practical prioritization system, identifying households that need attention first can be challenging.

**The goal:** Enable health workers to make informed, data-driven decisions about which households may require attention during extreme heat events.

## 💡 Our Solution

**Mitanin Heat Desk** provides a predictive triage dashboard that estimates heat stress, ranks demonstration households by potential risk, and generates daily field briefings in Hindi.

### Key Features

- **Predictive Wet-Bulb Analytics:** Retrieves hourly weather forecasts from Open-Meteo and estimates wet-bulb temperature using air temperature and relative humidity.
- **Household Vulnerability Scoring:** Evaluates synthetic household profiles using age, social vulnerability, housing conditions, occupational exposure, and chronic health conditions.
- **Risk-Based Prioritization:** Combines estimated heat severity with household vulnerability factors to rank households for potential follow-up.
- **Automated Hindi Voice Briefings:** Generates concise field briefings with browser-based speech playback and optional Amazon Polly integration.
- **Interactive Heat Dashboard:** Visualizes heat trends and supports scenario simulations to explore how changing weather conditions may affect estimated risk.
- **Field Action Tracking:** Supports visit-status updates and ORS packet distribution tracking in the demonstration interface.
- **AWS Integration:** Uses AWS Amplify for frontend hosting and AWS Lambda for serverless backend processing, with optional Amazon Polly, S3, and DynamoDB integrations.

## ⚙️ How It Works

1. **Fetch Weather Forecast:** Retrieves tomorrow's hourly weather forecast from Open-Meteo.
2. **Estimate Wet-Bulb Temperature:** Uses air temperature and relative humidity to estimate wet-bulb conditions.
3. **Calculate Heat Severity:** Evaluates forecast conditions against configured heat-risk thresholds.
4. **Score Household Vulnerability:** Assesses synthetic household characteristics to estimate relative vulnerability.
5. **Prioritize Households:** Ranks demonstration households according to estimated risk.
6. **Generate Hindi Briefing:** Produces a concise briefing highlighting heat conditions and prioritized households.
7. **Track Field Actions:** Supports recording demonstration visits and ORS distribution where enabled.

## 🏗️ System Architecture

```text
        +--------------------------------+
        |     Mitanin / Health Worker    |
        |       Mobile or Web Browser    |
        +----------------+---------------+
                         |
                         v
        +--------------------------------+
        |       AWS Amplify Hosting      |
        |      HTML, CSS, JavaScript     |
        +----------------+---------------+
                         |
                         v
        +--------------------------------+
        |    AWS Lambda Function URL     |
        |          Python 3.12           |
        +----------+-----------+---------+
                   |           |
           +-------v------+  +-v-------------------+
           |  Open-Meteo  |  | Synthetic Household |
           |  Weather API |  | Vulnerability Data  |
           +--------------+  +---------------------+
                   |           |
                   +-----+-----+
                         |
                         v
        +--------------------------------+
        | Wet-Bulb Estimation & Risk      |
        | Scoring Engine                  |
        +----------------+---------------+
                         |
                         v
        +--------------------------------+
        | Household Prioritization &      |
        | Hindi Field Briefing            |
        +----------------+---------------+
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          Browser    Amazon Polly  DynamoDB
          Speech     (Optional)    (Optional)
          Synthesis       |
                          v
                       Amazon S3
                       (Optional)
```

### Architecture Overview

- **Frontend:** Single-page dashboard built with HTML, CSS, and JavaScript, featuring canvas-based heat-curve visualization and scenario controls.
- **Backend:** Python-based AWS Lambda handler exposed through a Lambda Function URL.
- **Weather Data:** Open-Meteo hourly forecast API.
- **Risk Engine:** Python modules for wet-bulb estimation and household vulnerability scoring.
- **Voice Briefing:** Browser Speech Synthesis API, with optional Amazon Polly integration.
- **Optional Storage:** Amazon S3 for generated audio and Amazon DynamoDB for visit logs.
- **Hosting:** AWS Amplify Hosting for the live web application.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Frontend | HTML, CSS, JavaScript |
| Frontend Hosting | AWS Amplify |
| Backend | AWS Lambda |
| Backend API | AWS Lambda Function URL |
| Weather Forecast | Open-Meteo API |
| Wet-Bulb Estimation | Python |
| Risk Scoring | Python |
| Browser Voice Playback | Web Speech API |
| Optional Voice Generation | Amazon Polly |
| Optional Audio Storage | Amazon S3 |
| Optional Visit Logging | Amazon DynamoDB |
| Development & Deployment | AWS SAM CLI, AWS CLI |
| Testing | Python unit tests, pytest-compatible test structure |

## 📁 Project Structure

```text
airsafe-environmental-hacks-2026/
│
├── data/
│   ├── generate_households.py
│   └── households.json
│
├── infra/
│   ├── DEPLOY.md
│   └── build.sh
│
├── src/
│   ├── lambda/
│   │   └── handler.py
│   │
│   ├── risk/
│   │   ├── scoring.py
│   │   └── wetbulb.py
│   │
│   └── web/
│       └── index.html
│
└── tests/
    └── test_risk.py
```

### Important Files

- `data/generate_households.py` — Generates synthetic household demonstration data.
- `data/households.json` — Contains synthetic demographic and housing-risk attributes.
- `infra/DEPLOY.md` — Provides infrastructure deployment instructions.
- `infra/build.sh` — Prepares the backend deployment bundle.
- `src/lambda/handler.py` — Implements the Lambda entry point, request routing, and briefing generation.
- `src/risk/scoring.py` — Calculates household vulnerability scores.
- `src/risk/wetbulb.py` — Implements wet-bulb estimation and heat-curve modeling.
- `src/web/index.html` — Contains the interactive dashboard.
- `tests/test_risk.py` — Tests risk-scoring and threshold algorithms.

## 🚀 Live Demo & Resources

- **Live Web Application (AWS Amplify):** [https://main.d2e9o4nf8jvnh9.amplifyapp.com](https://main.d2e9o4nf8jvnh9.amplifyapp.com)
- **Serverless Backend API (AWS Lambda):** [https://jiy3g526lmitpenyg25tvbbhze0dsajn.lambda-url.ap-southeast-2.on.aws/?mitanin=M01&demo=hot](https://jiy3g526lmitpenyg25tvbbhze0dsajn.lambda-url.ap-southeast-2.on.aws/?mitanin=M01&demo=hot)
- **GitHub Repository:** [https://github.com/harshita-k24/airsafe-environmental-hacks-2026](https://github.com/harshita-k24/airsafe-environmental-hacks-2026)

### Deployment Status

**The application is deployed on AWS Amplify, with a serverless backend hosted on AWS Lambda and accessible through a Lambda Function URL.** The local heat-risk tests have passed. Optional integrations depend on their respective AWS resources and configuration.

## 🧪 Testing & Deployment

### Local Testing

Run the heat-risk tests using Python:

```bash
python -m pytest tests/test_risk.py
```

Ensure Python and the required project dependencies are installed before running the tests.

### AWS Deployment

The project includes deployment instructions and a build script under the `infra/` directory.

- `infra/DEPLOY.md` — Deployment guidance.
- `infra/build.sh` — Backend packaging script.
- **AWS SAM CLI** — Supports local development and testing.

The live frontend and backend deployment are available through the links above. Optional services such as Amazon Polly, S3, and DynamoDB require their respective AWS resources, permissions, and configuration.

## 🔒 Security Considerations

- The public demonstration endpoint is intended for **synthetic demonstration data only**.
- Do not upload real household, patient, or personally identifiable information.
- Never commit AWS access keys, secret keys, tokens, or other credentials to the repository.
- Configure appropriate IAM permissions, access controls, and resource policies before enabling optional AWS services for broader use.
- Review API access and CORS settings before exposing the service publicly.

## ⚠️ Data Disclaimer & Limitations

- **Synthetic Data:** All household records are synthetic demonstration data and do not represent real households or patients.
- **Estimated Risk:** Risk scores are estimates intended to support prioritization, not provide a clinical diagnosis.
- **Decision Support Only:** The tool must not replace official heat-health advisories, established emergency protocols, or professional judgment.
- **Forecast Limitations:** Weather forecasts and estimated wet-bulb temperatures may differ from actual local conditions.
- **Threshold Limitations:** Configured risk thresholds should be validated against appropriate scientific and public-health guidance before operational use.
- **Optional Integrations:** Availability of voice generation, audio storage, and visit logging depends on AWS configuration.

## 🌍 Expected Impact

Mitanin Heat Desk aims to help community health workers:

- **Prioritize outreach** to households with higher estimated heat vulnerability.
- **Plan visits proactively** using forecast heat conditions.
- **Improve accessibility** through concise Hindi voice briefings.
- **Support field coordination** through visit-status and ORS distribution tracking.
- **Explore preventive interventions** using scenario-based heat-risk assessment.

The long-term vision is to support more proactive, accessible, and data-informed community heat-health preparedness.

## 👥 Built For

**Environmental Hacks 2026 Hackathon**

**Project:** Mitanin Heat Desk — Predictive Wet-Bulb Triage & Automated Voice Briefing System for Community Health Workers.

**Focus Areas:** Environmental health, extreme-heat preparedness, community healthcare, and responsible decision-support technology.

---

**Disclaimer:** This project is a hackathon demonstration and has not been established as a clinically validated or officially approved heat-health triage system.
