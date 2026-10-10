# Mitanin Heat Desk

**A heat-risk decision-support tool for community health workers.**

## Problem

Extreme heat can put vulnerable households at risk. Community health workers need a practical way to identify which households may need attention first.

## Our Solution

Mitanin Heat Desk estimates heat stress and ranks demonstration households by their potential heat risk, helping health workers prioritize visits during hot weather.

## How It Works

1. Retrieves tomorrow's weather forecast from Open-Meteo.
2. Estimates wet-bulb temperature using air temperature and humidity.
3. Calculates heat-risk severity and ranks synthetic households by priority.
4. Generates a Hindi field briefing, with browser-based speech playback.
5. Includes optional Amazon Polly, S3 audio storage, and DynamoDB visit logging when configured.

## Technology Stack

- Python
- AWS Lambda
- AWS SAM CLI for local development and testing
- Open-Meteo API
- HTML, CSS, and JavaScript
- Browser Speech Synthesis API
- Amazon Polly and S3 (optional audio generation and storage)
- Amazon DynamoDB (optional visit logging)

## Testing and Deployment

The local heat-risk tests have passed. AWS deployment and live end-to-end functionality are still being verified.

## Data Disclaimer

Household records are synthetic demonstration data. They do not represent real households or patients. Risk scores are estimates for decision support and must not replace official heat-health guidance or professional judgment.

## Security

The public demonstration endpoint, if enabled, is intended for synthetic data only. Do not upload personal household information or AWS credentials to this repository.