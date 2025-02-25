# tests/test_chatbot.py
import sys
import os
import json
import pytest

# Add the project root to sys.path so that we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot import app, FAQ_RESPONSES

# Override FAQ_RESPONSES for testing purposes (ignore Excel data)
FAQ_RESPONSES.clear()
FAQ_RESPONSES.update({
    "what is your return policy": "Returns are accepted within 30 days of purchase.",
    "how can i track my order": "You can track your order using the tracking link sent to your email."
})

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_chat_endpoint_known_question(client):
    response = client.post("/chat", data=json.dumps({"message": "what is your return policy?"}),
                           content_type="application/json")
    data = json.loads(response.data)
    assert "response" in data
    # Expect the response to mention "30 days"
    assert "30 days" in data["response"].lower()

def test_chat_endpoint_unknown_question(client):
    response = client.post("/chat", data=json.dumps({"message": "unknown question?"}),
                           content_type="application/json")
    data = json.loads(response.data)
    assert "response" in data
    # With our overridden FAQ, an unknown question should trigger the default message.
    # The default in our chatbot code is: "Sorry, I didn't understand that. Could you please rephrase?"
    assert "didn't understand" in data["response"].lower()
