import logging
import os

import backoff
import google.generativeai as genai

log = logging.getLogger(__name__)


class GeminiClient:
    """
    Thin wrapper around Google Generative AI.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY missing")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")  # text-only

    @backoff.on_exception(backoff.expo, Exception, max_time=30)
    def chat(self, prompt: str) -> str:
        log.info("Gemini prompt tokens=%s", len(prompt.split()))
        resp = self.model.generate_content(prompt, safety_settings={})
        return resp.text
