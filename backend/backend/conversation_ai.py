# conversation_ai.py

def detect_intent(user_text: str):
    text = user_text.lower()

    if "book" in text or "booking" in text:
        return "booking"

    elif "status" in text or "flight status" in text:
        return "status"

    elif "agent" in text or "help" in text:
        return "agent"

    else:
        return "unknown"


def generate_response(intent: str):
    if intent == "booking":
        return {
            "menu": "booking",
            "prompt": "You want booking. Press 1 for domestic or 2 for international."
        }

    elif intent == "status":
        return {
            "menu": "status",
            "prompt": "Please enter your flight number."
        }

    elif intent == "agent":
        return {
            "menu": "agent",
            "prompt": "Connecting you to an agent."
        }

    else:
        return {
            "menu": "main",
            "prompt": "Sorry, I did not understand. Please say booking or status."
        }