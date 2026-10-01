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


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for input text.

    Blank text and HTTP 400 responses return None for every output field.
    Other service failures propagate to the caller for appropriate handling.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result
    response = requests.post(
        URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers=HEADERS,
        timeout=15,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
