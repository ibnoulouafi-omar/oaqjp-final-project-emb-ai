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
