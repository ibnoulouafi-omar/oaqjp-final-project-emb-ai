"""Test request contracts and failures with explicitly mocked HTTP responses."""

import unittest
from unittest.mock import Mock, patch
import requests
from EmotionDetection.emotion_detection import EMOTIONS, HEADERS, URL, emotion_detector
from server import app


class OfflineTests(unittest.TestCase):
    """Tests independent of the course service."""

    def test_request_contract_and_format(self):
        """Send the required request and select the largest returned score."""
        scores = dict(zip(EMOTIONS, [0.1, 0.05, 0.2, 0.6, 0.05]))
        response = Mock(status_code=200)
        response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=response) as post:
            result = emotion_detector("A sample sentence")
        post.assert_called_once_with(
            URL, json={"raw_document": {"text": "A sample sentence"}},
            headers=HEADERS, timeout=15,
        )
        self.assertEqual(result, {**scores, "dominant_emotion": "joy"})

    def test_http_400(self):
        """Return None fields for a service rejection."""
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=Mock(status_code=400)):
            result = emotion_detector("Rejected input")
        self.assertEqual(result, dict.fromkeys((*EMOTIONS, "dominant_emotion")))

    def test_blank_input_does_not_call_service(self):
        """Reject missing or whitespace-only input locally."""
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            for value in ("", " \t\n", None):
                self.assertIsNone(emotion_detector(value)["dominant_emotion"])
        post.assert_not_called()

    def test_http_500_propagates(self):
        """Never convert service outages into fabricated predictions."""
        response = Mock(status_code=500)
        response.raise_for_status.side_effect = requests.HTTPError("Service failure")
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=response):
            with self.assertRaises(requests.HTTPError):
                emotion_detector("Sample")

    def test_index(self):
        """Serve the application page."""
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detector", response.data)

    def test_blank_route(self):
        """Display the required blank-input message."""
        response = app.test_client().get("/emotionDetector?textToAnalyze=%20")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Invalid text! Please try again!")

    def test_success_route(self):
        """Render the supplied prediction as plain text."""
        scores = dict.fromkeys(EMOTIONS, 0.1)
        scores.update(joy=0.6, dominant_emotion="joy")
        with patch("server.emotion_detector", return_value=scores):
            response = app.test_client().get("/emotionDetector?textToAnalyze=Hello")
        self.assertEqual(response.status_code, 200)
        self.assertIn("The dominant emotion is joy.", response.text)
        self.assertEqual(response.mimetype, "text/plain")

    def test_unavailable_route(self):
        """Handle timeouts without exposing implementation details."""
        with patch("server.emotion_detector", side_effect=requests.Timeout("Timed out")):
            with self.assertLogs(app.logger, level="ERROR"):
                response = app.test_client().get("/emotionDetector?textToAnalyze=Hello")
        self.assertEqual(response.status_code, 503)
        self.assertIn("service is unavailable", response.text)


if __name__ == "__main__":
    unittest.main()
