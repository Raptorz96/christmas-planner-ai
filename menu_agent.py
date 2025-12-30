import os
from dotenv import load_dotenv
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

menu_agent = Agent(
    name="menu_agent",
    client=client,
    system_prompt="""Sei un esperto chef di cucina natalizia italiana.
Quando ricevi una richiesta, considera:
- Numero di ospiti
- Allergie/intolleranze
- Preferenze (vegetariano, vegano, tradizionale, ecc.)

Genera un menu completo: antipasto, primo, secondo, contorno, dolce.""",
    max_steps=3
)

# Test
response = menu_agent.run("Menu per 6 persone, 1 vegetariano, nessuna allergia")
print(response.text)