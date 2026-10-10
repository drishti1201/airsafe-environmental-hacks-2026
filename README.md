Mitanin Heat Desk (मितानिन हीट डेस्क)Predictive Wet-Bulb Triage & Automated Voice Briefing System for Community Health Workers in Raipur, Chhattisgarh.   Built for the Environmental Hacks 2026 Hackathon.   Live Links & DeploymentLive Web Application (AWS Amplify): https://main.d2e9o4nf8jvnh9.amplifyapp.comLive Serverless Backend API (AWS Lambda Function URL): https://jiy3g526lmitpenyg25tvbbhze0dsajn.lambda-url.ap-southeast-2.on.aws/?mitanin=M01&demo=hot   GitHub Repository: https://github.com/harshita-k24/airsafe-environmental-hacks-2026   The ChallengeDuring extreme pre-monsoon heat events in central India, high dry-bulb temperatures combine with high humidity, pushing the Wet-Bulb Temperature past critical physiological thresholds (>31°C). At these levels, the human body cannot cool itself through evaporative sweating, leading to acute heat exhaustion, heat stroke, and cardiovascular distress.Frontline community health workers (Mitanins) monitor hundreds of households across urban slums and informal settlements. Without localized, data-driven prioritization, vulnerable residents—especially elders living alone, infants under uninsulated tin or asbestos roofs, and outdoor laborers—cannot be reached in time before peak afternoon heat hits.   The SolutionMitanin Heat Desk provides a triage engine that delivers daily action plans directly to health workers:   Predictive Wet-Bulb Analytics: Evaluates hourly dry-bulb temperature and relative humidity from Open-Meteo forecasts to compute true thermodynamic wet-bulb heat curves and severity tiers.   Household Vulnerability Scoring Engine: Multiplies wet-bulb severity by a structured vulnerability matrix accounting for:Age (65+ or under 2 years)   Social vulnerability (living alone, no caregiver)   Housing infrastructure (tin or asbestos roofing)   Occupational risk (outdoor/sun exposure)   Chronic health conditions   Automated Hindi Voice Briefing: Generates concise, audio-ready briefings in regional Hindi, summarizing the day's peak heat timeline and prioritized households for field workers on the move.   Field Action Tracking: Interactive interface allowing Mitanins to mark visits as completed and track ORS packet distribution in real time[cite: 17].System Architecture               +-------------------------------+
               |    Frontline Health Worker    |
               |   (Mitanin Mobile / Browser)  |
               +---------------+---------------+
                               |
                AWS Amplify Static Web Hosting
                               |
               +---------------v---------------+
               |   AWS Lambda API Handler      |
               |        (Python 3.12)          |
               +-------+---------------+-------+
                       |               |
       +---------------+---+       +---+----------------+
       | Open-Meteo Hourly |       |  Raipur Household  |
       | Weather Forecast  |       |  Vulnerability DB  |
       +-------------------+       +--------------------+
Frontend: Single-page dashboard with zero framework overhead, canvas-based heat curve visualization, and real-time scenario simulation controls[cite: 20].Hosting: AWS Amplify Hosting.Backend: AWS Lambda Function URL (ap-southeast-2) with CORS enabled[cite: 5, 18].Audio Synthesis: AWS Polly (Hindi Voice engine).Project Structureairsafe-environmental-hacks-2026/
|-- data/
|   |-- generate_households.py   # Synthetic household generation script
|   `-- households.json          # Household demographic and housing risk dataset
|-- infra/
|   |-- DEPLOY.md                # Infrastructure deployment instructions
|   `-- build.sh                 # Lambda packaging and deployment bundle script
|-- src/
|   |-- lambda/
|   |   `-- handler.py           # Lambda entry point, route routing, and briefing generation
|   |-- risk/
|   |   |-- scoring.py           # Household vulnerability matrix calculation
|   |   `-- wetbulb.py           # Wet-bulb temperature formulas & curve modeling
|   `-- web/
|       `-- index.html           # Interactive Mitanin Heat Desk frontend dashboard
`-- tests/
    `-- test_risk.py             # Unit tests for scoring and threshold algorithms
