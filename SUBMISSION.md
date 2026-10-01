# Emotion Detector submission checklist

The code, package, local Flask deployment, blank-input handling, and static analysis have been validated. Live Watson outputs are still blocked by network access. Do not submit failure logs as successful prediction or test evidence.

| Question | Required submission | Status |
| --- | --- | --- |
| 1 | https://github.com/ibnoulouafi-omar/oaqjp-final-project-emb-ai/blob/main/README.md | Ready |
| 2 | [2a_emotion_detection](evidence/2a_emotion_detection) | Ready: initial raw-response function |
| 3 | [2b_application_creation](evidence/2b_application_creation) | Blocked: actual live request fails |
| 4 | [3a_output_formatting](evidence/3a_output_formatting) | Ready |
| 5 | [3b_formatted_output_test](evidence/3b_formatted_output_test) | Blocked: actual live request fails |
| 6 | https://github.com/ibnoulouafi-omar/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py | Ready |
| 7 | [4b_packaging_test](evidence/4b_packaging_test) | Ready: real package import and blank-input call |
| 8 | [5a_unit_testing](evidence/5a_unit_testing) | Ready: live test code |
| 9 | [5b_unit_testing_result](evidence/5b_unit_testing_result) | Blocked: requires passing live tests in course lab |
| 10 | [6a_server](evidence/6a_server) | Ready |
| 11 | [6b_deployment_test.png](evidence/6b_deployment_test.png) | Initial deployed interface only; capture successful analysis in lab |
| 12 | [7a_error_handling_function](evidence/7a_error_handling_function) | Ready |
| 13 | [7b_error_handling_server](evidence/7b_error_handling_server) | Ready |
| 14 | [7c_error_handling_interface.png](evidence/7c_error_handling_interface.png) | Ready: genuine blank-input error |
| 15 | [8a_server_modified](evidence/8a_server_modified) | Ready |
| 16 | [8b_static_code_analysis](evidence/8b_static_code_analysis) | Ready: Pylint 10.00/10 |

## Complete the blocked evidence inside the course lab

```bash
git clone https://github.com/ibnoulouafi-omar/oaqjp-final-project-emb-ai.git
cd oaqjp-final-project-emb-ai
python3 -m pip install -r requirements-dev.txt
python3 collect_evidence.py --live
python3 -m flask --app server run --host 0.0.0.0 --port 5000
```

Check that the regenerated live-output files end with `Exit code: 0` and that the live tests report `OK`. Open the lab's port-5000 preview, analyze `I am so happy I am doing this.`, and capture the visible successful result as `6b_deployment_test.png`. Keep any new error output if the service remains unavailable; it is not a successful test.
