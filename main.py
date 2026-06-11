from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

@app.get("/")
def home():
    return {"mensaje": "Chat AI funcionando"}

@app.get("/chat")
def chat(question: str):

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "respuesta": completion.choices[0].message.content
    }