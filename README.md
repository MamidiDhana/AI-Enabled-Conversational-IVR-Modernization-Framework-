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