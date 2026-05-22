from groq import Groq
from app.config.settings import settings


client = Groq(
    api_key=settings.GROK_API_KEY
)

MODEL_NAME = "llama3-70b-8192"


def generate_completion(prompt: str):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a compliance assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()