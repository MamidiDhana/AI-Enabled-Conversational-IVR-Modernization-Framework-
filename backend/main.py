from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

# -----------------------------
# Application Initialization
# -----------------------------
app = FastAPI(title="IVR Integration Layer")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# In-memory Session Storage
# -----------------------------
sessions = {}

# -----------------------------
# Request Models
# -----------------------------
class StartCall(BaseModel):
    caller: str = "Simulator"

class UserInput(BaseModel):
    session_id: str
    digit: str

# -----------------------------
# Mock ACS / BAP Connector
# -----------------------------
def mock_acs_bap(digit):
    if digit == "1":
        return "Booking selected. Press 1 for Domestic, 2 for International."
    elif digit == "2":
        return "Flight Status selected. Please wait."
    else:
        return "Invalid input. Please try again."

# -----------------------------
# API: Start IVR Call
# -----------------------------
@app.post("/ivr/start")
def start_call(data: StartCall):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"state": "MAIN"}

    return {
        "session_id": session_id,
        "message": "Welcome to IVR System. Press 1 for Booking, 2 for Status."
    }

# -----------------------------
# API: Handle IVR Input
# -----------------------------
@app.post("/ivr/input")
def ivr_input(data: UserInput):
    if data.session_id not in sessions:
        return {"message": "Session expired"}

    # Send input to ACS/BAP (mocked)
    response = mock_acs_bap(data.digit)

    return {
        "message": response
    }

# -----------------------------
# Health Check API
# -----------------------------
@app.get("/")
def health():
    return {"status": "Integration Layer Running"}