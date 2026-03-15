from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
import base64
import uuid
from gtts import gTTS

# -----------------------------
# Application Initialization
# -----------------------------
app = FastAPI(title="Hospital Conversational IVR Integration Layer")

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

MAIN_MENU_PROMPT = (
    "Welcome to City Hospital IVR. "
    "Press 1 for Appointment Booking, "
    "Press 2 for Doctor Availability, "
    "Press 3 for Emergency Services, "
    "Press 4 for Department Information, "
    "Press 5 for Hospital Timings, "
    "Press 6 for Hospital Location, "
    "Press 9 to hear this menu again."
)


def estimate_wait_minutes(seed_value: str) -> int:
    # Deterministic estimate to keep responses stable during a session.
    if not seed_value:
        return 10

    minute_bands = [5, 8, 12, 15, 18]
    index = sum(ord(char) for char in seed_value) % len(minute_bands)
    return minute_bands[index]

# -----------------------------
# Request Models
# -----------------------------
class StartCall(BaseModel):
    caller: str = "Simulator"

class UserInput(BaseModel):
    session_id: str
    digit: str

class AIMessage(BaseModel):
    message: str
    session_id: str | None = None


class TTSRequest(BaseModel):
    text: str
    language: str = "en-US"


INTENT_TO_IVR_OPTION = {
    "appointment": "1",
    "doctor": "2",
    "emergency": "3",
    "departments": "4",
    "timings": "5",
    "location": "6",
}

TTS_LANGUAGE_MAP = {
    "en-US": "en",
    "hi-IN": "hi",
    "ta-IN": "ta",
    "te-IN": "te",
    "kn-IN": "kn",
    "ml-IN": "ml",
    "bn-IN": "bn",
}

# -----------------------------
# Conversational AI Functions
# -----------------------------
def detect_intent(text):

    text = text.lower()

    if "appointment" in text or "book appointment" in text:
        return "appointment"

    elif "doctor" in text or "doctor availability" in text:
        return "doctor"

    elif "emergency" in text:
        return "emergency"

    elif (
        "departments" in text
        or "hospital departments" in text
        or "what departments are available" in text
    ):
        return "departments"

    elif (
        "timing" in text
        or "timings" in text
        or "hours" in text
        or "opening time" in text
        or "working hours" in text
    ):
        return "timings"

    elif (
        "location" in text
        or "address" in text
        or "where is hospital" in text
        or "directions" in text
    ):
        return "location"

    elif "insurance" in text or "cashless" in text:
        return "insurance"

    else:
        return "unknown"


def generate_response(intent, wait_minutes=None):

    if intent == "appointment":
        return {
            "menu": "appointment",
            "prompt": "You want to book an appointment. Press 1 for General Physician or 2 for Specialist."
        }
    
    elif intent == "doctor":
        wait_text = (
            f" Estimated wait time is about {wait_minutes} minutes."
            if wait_minutes is not None
            else ""
        )
        return {
            "menu": "doctor",
            "prompt": "Doctor availability selected. Please wait while we retrieve doctor schedules." + wait_text
        }

    elif intent == "emergency":
        return {
            "menu": "emergency",
            "prompt": "Emergency department selected. Please stay on the line."
        }

    elif intent == "departments":
        return {
            "menu": "departments",
            "prompt": "Our hospital departments include Cardiology, Orthopedics, and General Medicine."
        }

    elif intent == "timings":
        return {
            "menu": "timings",
            "prompt": "Hospital timings are Monday to Saturday, 8 AM to 8 PM. Emergency services are available 24 by 7."
        }

    elif intent == "location":
        return {
            "menu": "location",
            "prompt": "City Hospital is located on MG Road, near Central Metro Station."
        }

    elif intent == "insurance":
        return {
            "menu": "insurance",
            "prompt": "We support cashless treatment for major insurance providers. Please share your insurer name at the help desk."
        }

    else:
        return {
            "menu": "main",
            "prompt": "Sorry, I didn't understand. You can ask about appointment, doctor availability, emergency, departments, timings, location, or insurance."
        }


def build_conversation_result(intent: str, seed_value: str = "") -> dict:
    wait_minutes = estimate_wait_minutes(seed_value) if intent == "doctor" else None
    response = generate_response(intent, wait_minutes)

    return {
        "intent": intent,
        "prompt": response["prompt"],
        "menu": response["menu"],
        "ivr_option": INTENT_TO_IVR_OPTION.get(intent),
    }

# -----------------------------
# Mock Hospital IVR Logic
# -----------------------------
def mock_acs_bap(digit, session_id=""):

    if digit == "1":
        return "Appointment booking selected. Press 1 for General Physician, Press 2 for Specialist."

    elif digit == "2":
        wait_minutes = estimate_wait_minutes(session_id)
        return (
            "Doctor availability selected. Please wait while we retrieve doctor schedules. "
            f"Estimated wait time is about {wait_minutes} minutes."
        )

    elif digit == "3":
        return "Emergency department selected. Please stay on the line."

    elif digit == "4":
        return "Our hospital departments include Cardiology, Orthopedics, and General Medicine."

    elif digit == "5":
        return "Hospital timings are Monday to Saturday, 8 AM to 8 PM. Emergency services are available 24 by 7."

    elif digit == "6":
        return "City Hospital is located on MG Road, near Central Metro Station."

    elif digit == "9":
        return MAIN_MENU_PROMPT

    else:
        return "Invalid input. Please try again."

# -----------------------------
# API: Start IVR Call
# -----------------------------
@app.post("/ivr/start")
def start_call(data: StartCall):

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "state": "MAIN"
    }

    return {
        "session_id": session_id,
        "message": MAIN_MENU_PROMPT
    }

# -----------------------------
# API: Handle IVR Input
# -----------------------------
@app.post("/ivr/input")
def ivr_input(data: UserInput):

    if data.session_id not in sessions:
        return {"message": "Session expired"}

    response = mock_acs_bap(data.digit, data.session_id)

    return {
        "message": response
    }

# -----------------------------
# API: Conversational AI Input
# -----------------------------
@app.post("/ai/message")
def ai_message(data: AIMessage):

    user_text = data.message
    intent = detect_intent(user_text)
    seed_value = data.session_id if data.session_id else user_text

    return build_conversation_result(intent, seed_value)


# -----------------------------
# API: Server-side TTS
# -----------------------------
@app.post("/tts")
def text_to_speech(data: TTSRequest):

    text = data.text.strip()
    if not text:
        return {"audio_base64": "", "language": data.language}

    tts_lang = TTS_LANGUAGE_MAP.get(data.language, "en")
    buffer = BytesIO()

    # gTTS improves multilingual consistency when client machine lacks local voices.
    tts = gTTS(text=text, lang=tts_lang)
    tts.write_to_fp(buffer)

    encoded_audio = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {
        "audio_base64": encoded_audio,
        "language": data.language,
    }

# -----------------------------
# Health Check API
# -----------------------------
@app.get("/")
def health():

    return {
        "status": "Hospital Conversational IVR Integration Layer Running"
    }