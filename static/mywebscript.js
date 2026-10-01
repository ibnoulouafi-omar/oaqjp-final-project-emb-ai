"use strict";
document.getElementById("emotion-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const result = document.getElementById("system_response");
    const button = event.currentTarget.querySelector("button");
    const text = document.getElementById("textToAnalyze").value;
    button.disabled = true;
    result.className = "";
    result.textContent = "Analyzing…";
    try {
        const query = new URLSearchParams({textToAnalyze: text});
        const response = await fetch(`/emotionDetector?${query}`);
        result.textContent = await response.text();
        result.className = response.ok ? "success" : "error";
    } catch {
        result.textContent = "Unable to reach the application. Please try again.";
        result.className = "error";
    } finally {
        button.disabled = false;
    }
});