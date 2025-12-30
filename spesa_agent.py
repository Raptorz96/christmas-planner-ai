import os
from dotenv import load_dotenv
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

spesa_agent = Agent(
    name="spesa_agent",
    client=client,
    system_prompt="""Sei un esperto di pianificazione della spesa.
Dato un menu, genera una lista della spesa completa con:
- Ingrediente
- Quantità stimata
- Categoria (carne, verdure, latticini, ecc.)

Organizza la lista per categoria per facilitare gli acquisti.""",
    max_steps=3
)

# Test
menu_test = """
Antipasto: Tagliere di formaggi e salumi
Primo: Lasagna vegetariana
Secondo: Arrosto di vitello
Contorno: Patate al rosmarino
Dolce: Panettone con crema al mascarpone
Per 6 persone.
"""

response = spesa_agent.run(f"Genera la lista della spesa per questo menu: {menu_test}")
print(response.text)