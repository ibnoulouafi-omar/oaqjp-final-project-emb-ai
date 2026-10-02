"""Capture real browser screenshots of the running local Flask application."""

from pathlib import Path
import sys
from playwright.sync_api import sync_playwright, expect

EVIDENCE = Path(__file__).resolve().parent / "evidence"


def main():
    """Verify deployment and blank-input handling without mocking the browser."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        page.goto("http://127.0.0.1:5000/", wait_until="networkidle")
        expect(page.get_by_role("heading", name="Emotion Detector", exact=True)).to_be_visible()
        page.screenshot(path=str(EVIDENCE / "deployment_initial_interface.png"), full_page=True)
        page.get_by_label("Text to analyze").fill("")
        expect(page.get_by_label("Text to analyze")).to_have_value("")
        with page.expect_response("**/emotionDetector?textToAnalyze=") as invalid_response:
            page.get_by_role("button", name="Analyze emotions").click()
        assert invalid_response.value.status == 400
        expect(page.locator("#system_response")).to_have_text("Invalid text! Please try again!")
        page.screenshot(path=str(EVIDENCE / "7c_error_handling_interface.png"), full_page=True)
        if "--blank-only" in sys.argv:
            browser.close()
            print("PASS: empty input, real HTTP 400 response, and visible invalid-text message.")
            return
        page.get_by_label("Text to analyze").fill("I am glad this happened")
        page.get_by_role("button", name="Analyze emotions").click()
        if "--live" in sys.argv:
            expect(page.locator("#system_response")).to_contain_text(
                "The dominant emotion is joy.", timeout=60000
            )
            page.screenshot(path=str(EVIDENCE / "6b_deployment_test.png"), full_page=True)
        else:
            expect(page.locator("#system_response")).to_have_text(
                "The emotion detection service is unavailable. Please try again later.", timeout=60000
            )
            page.screenshot(path=str(EVIDENCE / "service_unavailable.png"), full_page=True)
        browser.close()
    print("PASS: deployed page, real blank-input response, and requested service-response check.")


if __name__ == "__main__":
    main()
