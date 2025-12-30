import streamlit as st
import os
from dotenv import load_dotenv
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from datapizza.tools.duckduckgo import DuckDuckGoSearchTool
from fpdf import FPDF
from io import BytesIO

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o"
)

gift_agent = Agent(
    name="gift_agent",
    client=client,
    tools=[DuckDuckGoSearchTool()],
    system_prompt="""Sei un esperto di regali natalizi.
Usa la ricerca web per trovare regali reali e disponibili.
Per ogni regalo suggerisci:
- Nome prodotto
- Prezzo stimato
- Link per l'acquisto (se disponibile)
Suggerisci 3 regali concreti e acquistabili.
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=3
)

menu_agent = Agent(
    name="menu_agent",
    client=client,
    system_prompt="""Sei un esperto chef di cucina natalizia italiana.
Genera un menu completo: antipasto, primo, secondo, contorno, dolce.
Considera: numero ospiti, preferenze alimentari, allergeni.
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=1
)

spesa_agent = Agent(
    name="spesa_agent",
    client=client,
    system_prompt="""Sei un esperto di pianificazione della spesa.
Dato un menu, genera lista della spesa con: ingrediente, quantità, categoria.
Organizza per categoria (carne, pesce, verdure, latticini, ecc.).
Rispondi UNA SOLA VOLTA e fermati.""",
    max_steps=1
)

def genera_pdf_natalizio(menu_text=None, spesa_text=None, regali_text=None):
    """Genera un PDF con stile natalizio"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header rosso natalizio
    pdf.set_fill_color(139, 0, 0)  # Rosso scuro
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(255, 215, 0)  # Oro
    pdf.set_y(12)
    pdf.cell(0, 10, 'Christmas Planner', align='C', ln=True)
    
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'Il tuo piano di Natale', align='C', ln=True)
    
    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    
    # Sezione Menu (se presente)
    if menu_text:
        pdf.set_fill_color(34, 139, 34)  # Verde
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, '  Menu di Natale', fill=True, ln=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', '', 11)
        pdf.ln(3)
        menu_clean = menu_text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 6, menu_clean)
        pdf.ln(8)
    
    # Sezione Spesa (se presente)
    if spesa_text:
        pdf.set_fill_color(178, 34, 34)  # Rosso
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, '  Lista della Spesa', fill=True, ln=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', '', 11)
        pdf.ln(3)
        spesa_clean = spesa_text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 6, spesa_clean)
        pdf.ln(8)
    
    # Sezione Regali (se presente)
    if regali_text:
        pdf.set_fill_color(218, 165, 32)  # Oro
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, '  Idee Regalo', fill=True, ln=True)
        
        pdf.set_font('Helvetica', '', 11)
        pdf.ln(3)
        regali_clean = regali_text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 6, regali_clean)
    
    # Footer
    pdf.set_y(-20)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, 'Generato con Christmas Planner AI - Buon Natale!', align='C')
    
    return bytes(pdf.output())

st.set_page_config(
    page_title="Christmas Planner 🎄",
    page_icon="🎄",
    layout="wide"
)

st.markdown("""
<style>
    /* Sfondo principale */
    .stApp {
        background: linear-gradient(180deg, #1a472a 0%, #2d5a3f 50%, #1a472a 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #8B0000 0%, #a52a2a 100%);
        border-right: 3px solid #FFD700;
    }
    
    /* Titoli */
    h1 {
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px #000000;
    }
    
    h2, h3 {
        color: #F0E68C !important;
    }
    
    /* Bottoni */
    .stButton > button {
        background: linear-gradient(90deg, #c41e3a 0%, #8B0000 100%);
        color: white;
        border: 2px solid #FFD700;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #8B0000 0%, #c41e3a 100%);
        border-color: #FFF;
    }
    
    /* Form e input */
    [data-testid="stForm"] {
        background-color: rgba(0, 0, 0, 0.3);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFD700;
    }
    
    /* Header rosso natalizio */
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #8B0000 0%, #c41e3a 100%) !important;
    }
    
    /* Testo generale */
    .stMarkdown {
        color: #FFFFFF;
    }
    
    /* Radio buttons sidebar */
    [data-testid="stSidebar"] .stRadio label {
        color: #FFFFFF !important;
    }
    
    /* Animazione neve */
    .snowflakes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
        overflow: hidden;
    }
    
    .snowflake {
        position: absolute;
        top: -20px;
        color: white;
        font-size: 1.5em;
        animation: fall linear infinite;
        opacity: 0.8;
    }
    
    @keyframes fall {
        0% { transform: translateY(-10px) rotate(0deg); }
        100% { transform: translateY(100vh) rotate(360deg); }
    }
    
    .snowflake:nth-child(1) { left: 5%; animation-duration: 8s; animation-delay: 0s; font-size: 1.2em; }
    .snowflake:nth-child(2) { left: 15%; animation-duration: 10s; animation-delay: 1s; font-size: 1.8em; }
    .snowflake:nth-child(3) { left: 25%; animation-duration: 9s; animation-delay: 2s; font-size: 1.4em; }
    .snowflake:nth-child(4) { left: 35%; animation-duration: 11s; animation-delay: 0.5s; font-size: 1.6em; }
    .snowflake:nth-child(5) { left: 45%; animation-duration: 8s; animation-delay: 3s; font-size: 1.3em; }
    .snowflake:nth-child(6) { left: 55%; animation-duration: 12s; animation-delay: 1.5s; font-size: 1.7em; }
    .snowflake:nth-child(7) { left: 65%; animation-duration: 9s; animation-delay: 2.5s; font-size: 1.5em; }
    .snowflake:nth-child(8) { left: 75%; animation-duration: 10s; animation-delay: 0s; font-size: 1.9em; }
    .snowflake:nth-child(9) { left: 85%; animation-duration: 7s; animation-delay: 1s; font-size: 1.2em; }
    .snowflake:nth-child(10) { left: 95%; animation-duration: 11s; animation-delay: 2s; font-size: 1.6em; }
</style>
""", unsafe_allow_html=True)

# Fiocchi di neve HTML
st.markdown("""
<div class="snowflakes">
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❄</div>
</div>
""", unsafe_allow_html=True)

st.title("🎄 Christmas Planner")

pagina = st.sidebar.radio(
    "Sezione",
    ["📋 Pianifica Tutto", "🎁 Regali", "🍝 Menu", "🛒 Lista Spesa"]
)

if pagina == "📋 Pianifica Tutto":
    st.header("📋 Pianifica il tuo Natale completo")
    
    with st.form("planner_form"):
        st.subheader("🍝 Menu")
        col1, col2 = st.columns(2)
        with col1:
            num_persone = st.number_input("Numero ospiti", min_value=1, max_value=50, value=4)
            preferenze = st.selectbox("Stile menu", ["Tradizionale", "Vegetariano", "Vegano", "Pesce"])
        with col2:
            allergeni = st.multiselect("Allergeni", ["Glutine", "Lattosio", "Frutta a guscio", "Uova", "Crostacei"])
        
        st.subheader("🎁 Regali")
        budget_totale = st.slider("Budget totale regali (€)", 20, 500, 100)
        destinatari = st.text_area("Descrivi i destinatari", placeholder="es. Mamma 60 anni ama giardinaggio, Nipote 8 anni ama videogiochi")
        
        submitted = st.form_submit_button("🎄 Genera Piano Completo")
        
        if submitted:
            allergeni_str = ", ".join(allergeni) if allergeni else "nessuna"
            
            # Step 1: Menu
            st.subheader("🍝 Il tuo Menu")
            with st.spinner("👨‍🍳 Preparo il menu..."):
                menu_query = f"Menu di Natale per {num_persone} persone, stile {preferenze}, allergeni: {allergeni_str}"
                try:
                    menu_response = menu_agent.run(menu_query)
                    st.markdown(menu_response.text)
                    st.session_state.menu_generato = menu_response.text
                except Exception as e:
                    st.error(f"❌ Errore menu: {e}")
                    st.stop()
            
            # Step 2: Lista Spesa
            st.subheader("🛒 Lista della Spesa")
            with st.spinner("🛒 Calcolo ingredienti..."):
                spesa_query = f"Genera la lista della spesa per questo menu:\n{menu_response.text}"
                try:
                    spesa_response = spesa_agent.run(spesa_query)
                    st.markdown(spesa_response.text)
                    st.session_state.spesa_generata = spesa_response.text
                except Exception as e:
                    st.error(f"❌ Errore spesa: {e}")
            
            # Step 3: Regali (solo se ci sono destinatari)
            regali_text = None
            if destinatari.strip():
                st.subheader("🎁 Idee Regalo")
                with st.spinner("🔍 Cerco regali..."):
                    gift_query = f"Trova regali per: {destinatari}. Budget totale: {budget_totale}€"
                    try:
                        gift_response = gift_agent.run(gift_query)
                        st.markdown(gift_response.text)
                        regali_text = gift_response.text
                        st.session_state.regali_generati = regali_text
                    except Exception as e:
                        st.error(f"❌ Errore regali: {e}")
            
            st.success("🎄 Piano completo generato!")
            
            # Salva per il PDF (fuori dal form)
            st.session_state.pdf_pronto = True
            st.session_state.pdf_menu = menu_response.text
            st.session_state.pdf_spesa = spesa_response.text
            st.session_state.pdf_regali = regali_text
    
    # Bottone download PDF (fuori dal form)
    if st.session_state.get('pdf_pronto'):
        try:
            pdf_bytes = genera_pdf_natalizio(
                st.session_state.pdf_menu,
                st.session_state.pdf_spesa,
                st.session_state.pdf_regali
            )
            st.download_button(
                label="📥 Scarica PDF",
                data=pdf_bytes,
                file_name="piano_natale.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning(f"⚠️ Impossibile generare PDF: {e}")

elif pagina == "🎁 Regali":
    st.header("🎁 Trova il regalo perfetto")
    
    with st.form("regalo_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            eta = st.number_input("Età", min_value=1, max_value=100, value=25)
            sesso = st.selectbox("Sesso", ["Uomo", "Donna", "Altro"])
        
        with col2:
            budget = st.slider("Budget (€)", 10, 500, 50)
            interessi = st.text_input("Interessi", placeholder="es. tecnologia, sport, cucina...")
        
        submitted = st.form_submit_button("🔍 Cerca regali")
        
        if submitted:
            with st.spinner("🔍 Cerco i regali migliori..."):
                query = f"Regalo per {sesso}, {eta} anni, interessi: {interessi}, budget: {budget}€"
                try:
                    response = gift_agent.run(query)
                    st.markdown(response.text)
                    st.session_state.regali_singoli = response.text
                except Exception as e:
                    st.error(f"❌ Errore durante la ricerca: {e}")
                    st.info("💡 Riprova tra qualche secondo")
    
    # PDF export regali
    if st.session_state.get('regali_singoli'):
        try:
            pdf_bytes = genera_pdf_natalizio(None, None, st.session_state.regali_singoli)
            st.download_button(
                label="📥 Scarica PDF Regali",
                data=pdf_bytes,
                file_name="regali_natale.pdf",
                mime="application/pdf",
                key="pdf_regali"
            )
        except Exception as e:
            st.warning(f"⚠️ Impossibile generare PDF: {e}")

elif pagina == "🍝 Menu":
    st.header("🍝 Crea il tuo menu di Natale")
    
    with st.form("menu_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            num_persone = st.number_input("Numero ospiti", min_value=1, max_value=50, value=4)
            preferenze = st.selectbox("Stile menu", ["Tradizionale", "Vegetariano", "Vegano", "Pesce"])
        
        with col2:
            allergeni = st.multiselect(
                "Allergeni/Intolleranze",
                ["Glutine", "Lattosio", "Frutta a guscio", "Uova", "Crostacei", "Nessuno"]
            )
        
        submitted = st.form_submit_button("🍽️ Genera menu")
        
        if submitted:
            with st.spinner("👨‍🍳 Preparo il menu..."):
                allergeni_str = ", ".join(allergeni) if allergeni else "nessuna"
                query = f"Menu di Natale per {num_persone} persone, stile {preferenze}, allergeni: {allergeni_str}"
                try:
                    response = menu_agent.run(query)
                    st.session_state.menu_generato = response.text
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"❌ Errore durante la generazione: {e}")
                    st.info("💡 Riprova tra qualche secondo")
    
    # Mostra menu salvato se esiste
    if "menu_generato" in st.session_state and not submitted:
        st.markdown(st.session_state.menu_generato)
    
    # PDF export menu
    if st.session_state.get('menu_generato'):
        try:
            pdf_bytes = genera_pdf_natalizio(st.session_state.menu_generato, None, None)
            st.download_button(
                label="📥 Scarica PDF Menu",
                data=pdf_bytes,
                file_name="menu_natale.pdf",
                mime="application/pdf",
                key="pdf_menu"
            )
        except Exception as e:
            st.warning(f"⚠️ Impossibile generare PDF: {e}")

elif pagina == "🛒 Lista Spesa":
    st.header("🛒 Lista della spesa")
    
    if "menu_generato" in st.session_state:
        st.success("Menu trovato! Genero la lista della spesa...")
        
        if st.button("📝 Genera lista spesa"):
            with st.spinner("🛒 Preparo la lista..."):
                query = f"Genera la lista della spesa per questo menu:\n{st.session_state.menu_generato}"
                try:
                    response = spesa_agent.run(query)
                    st.session_state.spesa_singola = response.text
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"❌ Errore durante la generazione: {e}")
                    st.info("💡 Riprova tra qualche secondo")
        
        # PDF export spesa
        if st.session_state.get('spesa_singola'):
            try:
                pdf_bytes = genera_pdf_natalizio(None, st.session_state.spesa_singola, None)
                st.download_button(
                    label="📥 Scarica PDF Spesa",
                    data=pdf_bytes,
                    file_name="spesa_natale.pdf",
                    mime="application/pdf",
                    key="pdf_spesa"
                )
            except Exception as e:
                st.warning(f"⚠️ Impossibile generare PDF: {e}")
    else:
        st.warning("⚠️ Prima genera un menu nella sezione Menu!")