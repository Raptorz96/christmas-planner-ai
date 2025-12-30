import os
from dotenv import load_dotenv
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

gift_agent = Agent(
    name="gift_agent",
    client=client,
    system_prompt="""Sei un esperto di regali natalizi.
Quando ricevi una richiesta, considera:
- Età del destinatario
- Sesso
- Interessi/hobby
- Budget disponibile

Suggerisci 3 regali concreti con prezzo stimato.""",
    max_steps=3
)

# Test
response = gift_agent.run("Regalo per ragazzo, 25 anni, appassionato di tecnologia, budget 50€")
print(response.text)