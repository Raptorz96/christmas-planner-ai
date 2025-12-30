import os
from dotenv import load_dotenv
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o"
)

# Agent specializzati - con istruzioni esplicite di fermarsi
gift_agent = Agent(
    name="gift_agent",
    client=client,
    system_prompt="""Sei un esperto di regali natalizi.
Suggerisci 3 regali concreti con prezzo stimato.
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=1
)

menu_agent = Agent(
    name="menu_agent",
    client=client,
    system_prompt="""Sei uno chef di cucina natalizia italiana.
Genera un menu completo: antipasto, primo, secondo, contorno, dolce.
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=1
)

spesa_agent = Agent(
    name="spesa_agent",
    client=client,
    system_prompt="""Sei un esperto di pianificazione della spesa.
Genera lista della spesa con ingrediente, quantità, categoria.
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=1
)

# Orchestratore
# Orchestratore - modifica solo questa parte
main_planner = Agent(
    name="main_planner",
    client=client,
    system_prompt="""Sei un assistente per pianificare il Natale.
Chiama UN SOLO agent tra: gift_agent, menu_agent, spesa_agent.
Dopo aver ricevuto la risposta, presentala all'utente.""",
    can_call=[gift_agent, menu_agent, spesa_agent],
    max_steps=2
)

# Test
response = main_planner.run("Aiutami a organizzare il pranzo di Natale per 4 persone, uno è celiaco")
print(response.text)