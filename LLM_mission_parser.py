import google.generativeai as genai
import json

class MissionParserLLM:
    def __init__(self,model_name: str = "gemini-1.5-pro"):
        genai.configure(api_key="AIzaSyD94Ty4f8HkPMIj2KOccGuy8_Q8PjlFQ34") # Should be stored securely, not hardcoded.
        self.model = genai.GenerativeModel(model_name)

    def parse_mission(self, user_input: str):
        system_prompt = """
You are a mission parsing assistant. A user will give you a one-sentence request, like:

"Detect all cars in images between 11:00 and 11:05"

Your job is to extract:
1. The object to detect (like 'car', 'bus', 'dog', etc.) THE OBJECT IS ALWAYS A SINGLE WORD, AND SINGULAR, CAR insted of CARS.

2. The time range (in 24-hour format)

Return ONLY valid JSON in the following format:

{
  "target_object": "car",
  "start_time": "11:00",
  "end_time": "11:05"
}

Don't return explanations or markdown.
"""
        response = self.model.generate_content([system_prompt, user_input])
        text = response.text.strip()
        # Strip markdown formatting if present
        if text.startswith("```"):
            text = text.strip("```").strip()
            if text.startswith("json"):
                text = text[len("json"):].strip()

        return json.loads(text)
