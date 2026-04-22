import json
from langchain_google_genai import ChatGoogleGenerativeAI

class FormIntelligence:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

    async def get_application_plan(self, html_content, user_profile):
        prompt = f"""
        Analyze this HTML form and the user's profile. 
        Create a JSON mapping of Playwright actions.
        
        USER PROFILE: {user_profile}
        HTML SNIPPET: {html_content[:8000]}
        
        Return ONLY a JSON list:
        [
          {{"selector": "input#first_name", "action": "fill", "value": "John"}},
          {{"selector": "button[type='submit']", "action": "click", "value": null}}
        ]
        """
        response = self.llm.invoke(prompt)
        # Strip markdown code blocks if present
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
        