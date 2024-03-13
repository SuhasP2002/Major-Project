import requests
import os

API_KEY = os.environ.get("API_KEY")
API_URL = "https://api-inference.huggingface.co/models/pszemraj/pegasus-x-large-book-summary"


def summarize_text(input_text):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(API_URL, headers=headers, json={"inputs": f"""{input_text}""",})
        output = response.json()
        summary_text = output[0]['summary_text']
        return summary_text
    except Exception as e:
        return None
