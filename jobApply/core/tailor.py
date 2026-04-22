from langchain_google_genai import ChatGoogleGenerativeAI

class ResumeTailor:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    async def generate_custom_answer(self, job_description, question, user_profile):
        """Generates custom answers for 'Why do you want to work here?' etc."""
        prompt = f"""
        JOB DESCRIPTION: {job_description}
        USER PROFILE: {user_profile}
        QUESTION: {question}
        
        Write a concise, professional 2-3 sentence answer to the question 
        that aligns the user's experience with the job requirements.
        """
        response = self.llm.invoke(prompt)
        return response.content.strip()

    async def summarize_job(self, page_text):
        """Distills a massive job page into just the requirements."""
        prompt = f"Summarize the key requirements of this job in 5 bullets: {page_text[:4000]}"
        response = self.llm.invoke(prompt)
        return response.content
        