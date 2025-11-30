# Backend/GeminiBrain.py — Updated for Gemini 2.5
import os
import requests
import json
import datetime
from dotenv import dotenv_values

class GeminiAgent:
    def __init__(self, knowledge_base_content=None, api_key=None):
        self.history = []
        
        # 1. Get API Key
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            env_vars = dotenv_values(".Env")
            self.api_key = env_vars.get("GOOGLE_API_KEY")

        if not self.api_key:
            print("Warning: No API Key found.")

        # 2. UPDATED MODEL LIST (Based on your successful test)
        self.available_models = [
            "gemini-2.5-flash",       # Available in your list! (Index 1)
            "gemini-2.5-pro",         # Available in your list! (Index 4)
            "gemini-2.0-flash",       # Available in your list! (Index 6)
            "gemini-flash-latest"     # Fallback
        ]
        self.current_model_index = 0
        self.model_name = self.available_models[0]
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
        
        now = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        
        # 3. System Prompt
        if knowledge_base_content:
            system_instruction = (
                f"System: Current Date is {now}. "
                "You are a specialized Knowledge Base Agent. "
                "The user has uploaded a document. Your job is to answer questions "
                "STRICTLY based on the content provided below.\n\n"
                f"--- START OF DOCUMENT ---\n{knowledge_base_content}\n--- END OF DOCUMENT ---\n\n"
                "If the answer is not in the document, state that you cannot find the information."
            )
        else:
            system_instruction = (
                f"System: Current Date is {now}. "
                "You are Proton, an advanced AI Assistant. "
                "Please ask the user to upload a document to begin."
            )

        self.system_prompt = {
            "role": "model",
            "parts": [{"text": system_instruction}]
        }
        self.history.append(self.system_prompt)

    def update_url(self):
        return f"{self.base_url}{self.model_name}:generateContent?key={self.api_key}"

    def send_message(self, user_text):
        if not self.api_key:
            return "Error: API Key is missing. Please enter it in the sidebar."

        self.history.append({"role": "user", "parts": [{"text": user_text}]})

        payload = {
            "contents": self.history,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 8192 
            }
        }

        # 4. Auto-Retry Logic
        for attempt in range(len(self.available_models)):
            current_url = self.update_url()
            try:
                response = requests.post(
                    current_url, 
                    headers={"Content-Type": "application/json"}, 
                    data=json.dumps(payload)
                )
                
                if response.status_code == 404:
                    self.current_model_index += 1
                    if self.current_model_index < len(self.available_models):
                        self.model_name = self.available_models[self.current_model_index]
                        continue 
                    else:
                        return f"Error: All models returned 404. Last tried: {self.model_name}"

                if response.status_code != 200:
                    return f"Google API Error ({response.status_code}): {response.text}"
                
                data = response.json()
                try:
                    if "candidates" in data and len(data["candidates"]) > 0:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            reply = candidate["content"]["parts"][0]["text"]
                            self.history.append({"role": "model", "parts": [{"text": reply}]})
                            return reply
                        else:
                            return "Error: Content blocked or empty."
                    else:
                        return "Error: Empty response from AI."
                except (KeyError, IndexError) as e:
                    return f"Parsing Error: {str(e)}"

            except Exception as e:
                return f"Connection Error: {e}"
        

        return "Error: Failed to connect."
