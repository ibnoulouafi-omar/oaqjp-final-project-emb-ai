"""Capture genuine submission evidence without substituting model outputs."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"


def capture(name, arguments, note=""):
    """Record a real Python command, its output, and its exit status."""
    environment = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, *arguments], cwd=ROOT, env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", check=False,
    )
    command = "python " + subprocess.list2cmdline(arguments)
    text = f"{note}\n{command}\n{result.stdout}\nExit code: {result.returncode}\n"
    (EVIDENCE / name).write_text(text.lstrip(), encoding="utf-8")
    print(f"{name}: exit {result.returncode}", flush=True)
    return result.returncode


def main():
    """Collect local checks; --live also attempts the course-only service."""
    EVIDENCE.mkdir(exist_ok=True)
    for name, source in {
        "3a_output_formatting": "EmotionDetection/emotion_detection.py",
        "7a_error_handling_function": "EmotionDetection/emotion_detection.py",
        "5a_unit_testing": "test_emotion_detection.py",
        "6a_server": "server.py",
        "7b_error_handling_server": "server.py",
        "8a_server_modified": "server.py",
    }.items():
        (EVIDENCE / name).write_text((ROOT / source).read_text(), encoding="utf-8")
    capture("offline_unit_testing_result", ["-m", "unittest", "-v", "tests.test_offline"],
            "OFFLINE TESTS: HTTP responses are mocked. Not live Watson model validation.")
    capture("8b_static_code_analysis", ["-m", "pylint", "server.py"])
    capture("4b_packaging_test", ["-c", (
        "import EmotionDetection; "
        "from EmotionDetection.emotion_detection import emotion_detector; "
        "print('EmotionDetection is a valid package:', hasattr(EmotionDetection, '__path__')); "
        "print('emotion_detector is callable:', callable(emotion_detector)); "
        "print('Blank-input check:', emotion_detector(''))"
    )])
    if "--live" in sys.argv:
        capture("2b_application_creation", ["-c", (
            "import runpy; "
            "module = runpy.run_path('evidence/2a_emotion_detection'); "
            "print('Application imported successfully', flush=True); "
            "print(module['emotion_detector']('I love this new technology.'))"
        )], "LIVE WATSON REQUEST: failure output means this evidence is not yet submission-ready.")
        capture("3b_formatted_output_test", ["-c", (
            "from EmotionDetection.emotion_detection import emotion_detector; "
            "print(emotion_detector('I am so happy I am doing this.'))"
        )], "LIVE WATSON REQUEST: no synthetic model scores are used.")
        capture("5b_unit_testing_result", ["-m", "unittest", "-v", "test_emotion_detection"],
                "LIVE WATSON TESTS: network access to the course endpoint is required.")


if __name__ == "__main__":
    main()
