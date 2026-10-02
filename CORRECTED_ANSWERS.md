# Corrected submissions after grading feedback

These corrections address Questions 2, 10, 12, and 14. Questions 3, 5, 7, 9, and 11 still require successful live Watson evidence from the course lab. Do not submit pending notes or failure logs.

## Question 2

```python
"""Initial application function, before output formatting and error handling."""

import requests


def emotion_detector(text_to_analyse):
    """Send text to Watson NLP and return the raw JSON response text."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    response = requests.post(
        url,
        json={"raw_document": {"text": text_to_analyse}},
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()
    return response.text
```

## Question 10

```python
"""Serve the Emotion Detector interface and Watson-backed analysis route."""

from flask import Flask, Response, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the text entry page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze text and return a readable, plain-text result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Emotion service request failed")
        return Response(
            "The emotion detection service is unavailable. Please try again later.",
            status=503,
            mimetype="text/plain",
        )
    if result["dominant_emotion"] is None:
        return Response(
            "Invalid text! Please try again!", status=400, mimetype="text/plain"
        )
    message = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return Response(message, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Question 12

```python
"""Analyze text with the Watson NLP EmotionPredict service."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Return emotion scores and the dominant emotion for input text.

    Blank text and HTTP 400 responses return None for every output field.
    Other service failures propagate to the caller for appropriate handling.
    """
    empty_result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return empty_result
    response = requests.post(
        URL,
        json={"raw_document": {"text": text_to_analyse}},
        headers=HEADERS,
        timeout=15,
    )
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }
    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {
        "anger": scores["anger"],
        "disgust": scores["disgust"],
        "fear": scores["fear"],
        "joy": scores["joy"],
        "sadness": scores["sadness"],
    }
    result["dominant_emotion"] = max(result, key=result.get)
    return result
```

## Question 14

Upload the regenerated [7c_error_handling_interface.png](evidence/7c_error_handling_interface.png), which shows a truly blank field and the invalid-text message.
