from fastapi import FastAPI
from openai import OpenAI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>Chat Financiero</h1>
            <input id='q'>
            <button onclick='preguntar()'>Enviar</button>
            <div id='r'></div>

            <script>
            async function preguntar(){
                let q=document.getElementById('q').value;

                let resp=await fetch(
                    '/chat?question='+encodeURIComponent(q)
                );

                let data=await resp.json();

                document.getElementById('r').innerHTML =
                    data.respuesta;
            }
            </script>
        </body>
    </html>
    """

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