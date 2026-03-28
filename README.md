# Conversational IVR Modernization Framework – Milestone 2

## Objective
The objective of Milestone 2 is to design and implement an integration layer that enables communication between a legacy IVR system and Conversational AI platforms such as ACS/BAP.

## Architecture Overview
Legacy IVR (Web Simulator) → Integration Layer (Backend APIs) → Conversational AI (ACS/BAP – Mocked)

## Technologies Used
- Python
- FastAPI
- REST APIs
- HTML, JavaScript
- Web-based IVR Simulator

## Integration Layer Development
A REST-based middleware was developed to receive IVR inputs and forward them to a Conversational AI service. The ACS/BAP service is mocked to simulate intent processing and response generation.

## APIs Implemented
- POST /ivr/start – Starts an IVR session
- POST /ivr/input – Handles user input and returns conversational response
- POST /ai/message – Handles natural language requests and maps them to IVR-aligned intents

## Sample Transaction Validation
A web-based IVR simulator was used to validate the integration layer. Sample IVR transactions were executed and verified using real-time API calls.

## Outcome
The integration layer successfully enables real-time communication between the legacy IVR and Conversational AI logic, validating the modernization framework approach.

## Module 3 Status: Completed
- Conversational dialogue flows are implemented and mapped to IVR services (appointment, doctor, emergency, departments, timings, location, insurance).
- Conversational AI is integrated into the legacy architecture through existing FastAPI endpoints.
- Real-time voice input/output is enabled in the frontend using Web Speech API (input) and SpeechSynthesis (output).

## Module 4: Testing and Deployment

### Objective
Final validation and production rollout of the modernized IVR system.

### Task 1: Full-cycle Testing

Functional validation is implemented through automated API tests in `tests/test_hospital_api.py`.

Run tests:

```powershell
python -m pytest
```

Performance validation is implemented through a load-test utility.

Run performance test (example):

```powershell
python scripts/performance_test.py --base-url http://127.0.0.1:8000 --requests 200 --concurrency 20
```

This reports success rate, average latency, and P95 latency.

### Task 2: Deployment to Production Environment

Containerized deployment artifacts are included:
- `Dockerfile`
- `docker-compose.yml`

Deploy backend service:

```powershell
docker compose up -d --build
```

Access service health endpoint:

```text
http://127.0.0.1:8000/
```

### Task 3: Post-Deployment Monitoring

Monitoring utility is included for periodic health and latency checks.

Run monitor (example):

```powershell
python scripts/monitor_post_deploy.py --base-url http://127.0.0.1:8000 --interval 10 --checks 30 --latency-threshold 300
```

This outputs:
- Health check pass/fail status
- Request latency per interval
- Summary of failures and latency alerts

## Module 4 Status: Completed
- Full-cycle testing support includes functional tests and performance test tooling.
- Deployment support includes Docker-based production rollout configuration.
- Post-deployment monitoring support includes health and latency monitoring script.

---

## 🏥 Final Implementation – Hospital Conversational IVR System

### 📌 Description

This project implements an AI-enabled conversational IVR system for hospitals. It modernizes traditional IVR systems by enabling intelligent interaction between patients and hospital services using conversational AI.

The system supports:

* Appointment booking
* Doctor and department navigation
* Emergency handling
* Hospital information services
* Voice-based interaction using speech APIs

### ⚙️ API Endpoints

* POST /ivr/start → Start IVR session
* POST /ivr/input → Process user input
* POST /ai/message → Generate AI response
* POST /tts → Convert text to speech
* GET /health → System health check

### 🌐 Deployment

The backend is successfully deployed on Render cloud platform.

🔗 Live URL:https://ai-enabled-conversational-ivr-fsvu.onrender.com/docs

