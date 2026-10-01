# Emotion Detector

An AI-based web application that uses the IBM Watson NLP EmotionPredict service to analyze English text. It returns scores for anger, disgust, fear, joy, and sadness, together with the dominant emotion. A Flask interface displays the result and handles blank input.

This project was cloned from [the IBM course starter](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai).

## Run

Python 3.10 or later is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python server.py
```

On Windows, activate with `.venv\Scripts\Activate.ps1` instead. Open `http://127.0.0.1:5000`.

The Watson service is `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`. On this workstation it resolves to private IP addresses and cannot be reached. Nonblank predictions therefore require execution inside a course environment that can access this service. No alternative model or fabricated scores are used.

## Package API

```python
from EmotionDetection.emotion_detection import emotion_detector
result = emotion_detector("I am glad this happened")
print(result)
```

The result has keys `anger`, `disgust`, `fear`, `joy`, `sadness`, and `dominant_emotion`. Blank input and HTTP 400 responses return `None` for every field. Other upstream errors are reported as service unavailability by the web application.

## Validation

```bash
# Eight offline tests using explicitly mocked HTTP responses:
python -m unittest -v tests.test_offline

# Five live emotion tests; requires access to the Watson service:
python -m unittest -v test_emotion_detection

# Static analysis, with default checks enabled:
python -m pylint server.py
```

Offline tests passed. Pylint rated `server.py` 10.00/10. The live tests cannot pass here because the endpoint is unreachable; their actual failure output is kept in `evidence/5b_unit_testing_result`. Offline test success is not evidence of live model accuracy.

## Submission evidence

See [SUBMISSION.md](SUBMISSION.md) for all 16 fields. Files are saved under `evidence/` using the requested names. `2a_emotion_detection` preserves the initial raw-response implementation; the package contains the completed implementation with formatting and error handling.

```bash
python collect_evidence.py
# In the course lab, regenerate the live outputs:
python collect_evidence.py --live
```

`6b_deployment_test.png` shows the real locally deployed initial interface, without a prediction. `7c_error_handling_interface.png` shows a real blank-input error. Neither screenshot uses a mocked response. A successful live prediction screenshot remains to be captured inside the course lab.
