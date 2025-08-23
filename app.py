from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Hardcoded Gemini API key (local use only)
GEMINI_API_KEY = "AIzaSyAi4MVkyGRWw8SgUolH9Mn-XXRojDXVOiM"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

def compare_medicines(med1, med2):
    prompt = f"""
    Compare these two medicines:
    1. {med1} (prescribed)
    2. {med2} (available)

    Return ONLY JSON in this format:
    {{
      "confidence": 85,
      "side_effects": ["Nausea", "Headache", "Drowsiness"],
      "symptoms_treated": ["Fever", "Mild Pain"],
      "verdict": "Yes, it can be used as a substitute with caution."
    }}
    """

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(GEMINI_URL, headers=headers, json=data)
    result = resp.json()

    try:
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
        raw_text = raw_text.strip().strip("`")  # Remove markdown code fences
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()
        return json.loads(raw_text)
    except Exception as e:
        return {"error": f"Parsing failed: {e}", "raw_response": result}


@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    if request.method == "POST":
        med1 = request.form.get("med1")
        med2 = request.form.get("med2")
        data = compare_medicines(med1, med2)
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
