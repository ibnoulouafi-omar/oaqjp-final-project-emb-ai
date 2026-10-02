# Emotion Detector submission checklist

The code, package import, local Flask deployment, blank-input handling, and static analysis have been validated. Live Watson outputs are still blocked by network access. Do not submit this checklist, pending notes, failure logs, or the offline tests in place of required successful live evidence. Wait until all required evidence is complete before resubmitting.

| Question | Required submission | Status |
| --- | --- | --- |
| 1 | https://github.com/ibnoulouafi-omar/oaqjp-final-project-emb-ai/blob/main/README.md | Ready |
| 2 | [2a_emotion_detection](evidence/2a_emotion_detection) | Ready: initial raw-response function |
| 3 | [2b_application_creation](evidence/2b_application_creation) | Blocked: actual live request fails |
| 4 | [3a_output_formatting](evidence/3a_output_formatting) | Ready |
| 5 | [3b_formatted_output_test](evidence/3b_formatted_output_test) | Blocked: actual live request fails |
| 6 | https://github.com/ibnoulouafi-omar/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py | Ready |
| 7 | [4b_packaging_test](evidence/4b_packaging_test) | NOT READY: regenerate in the course lab; rubric requires numeric scores and dominant_emotion anger |
| 8 | [5a_unit_testing](evidence/5a_unit_testing) | Ready: live test code |
| 9 | [5b_unit_testing_result](evidence/5b_unit_testing_result) | Blocked: requires passing live tests in course lab |
| 10 | [6a_server](evidence/6a_server) | Ready |
| 11 | [6b_deployment_test.png](evidence/6b_deployment_test.png) | NOT READY: previous initial-interface screenshot was rejected; replace with successful analysis in lab |
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

If the repository is already cloned in your course lab, run `git pull --ff-only` from that folder instead of cloning again.

## Changes after grading feedback

- Questions 2 and 12: parameter spelling is now exactly `text_to_analyse`.
- Question 12: both normal and HTTP-400 dictionaries explicitly list the quoted field names; the HTTP-400 dictionary assigns `None` to every field.
- Question 10: the startup host is now `0.0.0.0`, port 5000.
- Question 14: the new screenshot shows a truly empty text field without a placeholder, plus the actual invalid-text response. HTTP 400 and empty input were asserted during capture. Detailed feedback for this question was not included in the supplied report, so this addresses the visible ambiguity without claiming it was the only grading issue.
- Question 7: the live collector now executes the required anger example. The earlier blank-input package check is preserved for reference but is not valid rubric evidence.
- Questions 3 and 5: live evidence now records the project directory, Python version, executed interactive commands, and their actual results.

The feedback's claim that the original dictionary comprehension failed to generate string keys was incorrect: its iteration values were strings. The explicit dictionaries preserve that correct behavior while matching the requested form.
