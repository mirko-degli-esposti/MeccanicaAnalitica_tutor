import streamlit as st
from openai import OpenAI


# ── Modelli disponibili ────────────────────────────────────────────────────────
MODELS = {
    "Claude Sonnet 4.5 (consigliato)": "anthropic/claude-sonnet-4-5",
    "Llama 3.3 70B (open, gratuito)":  "meta-llama/llama-3.3-70b-instruct",
    "Mistral Large (open, italiano)":  "mistralai/mistral-large",
    "Qwen 2.5 72B (open, economico)":  "qwen/qwen-2.5-72b-instruct",
    "DeepSeek R1 (open, STEM)":        "deepseek/deepseek-r1",
}
 

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tutor – Meccanica Analitica",
    page_icon="🎓",
    layout="centered"
)

# ── Stile minimale ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 760px; margin: auto; }
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        font-size: 0.78rem;
        color: #888;
        border-left: 3px solid #e0e0e0;
        padding-left: 10px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
Sei un tutor accademico personale per il corso 00686 – Meccanica Analitica (M-Z),
Laurea in Fisica, Università di Bologna, A.A. 2025/2026.
Docente: prof. Mirko Degli Esposti. 8 CFU, SSD MAT/07.

SYLLABUS DEL CORSO
==================

Il corso copre i seguenti argomenti core (obbligatori per l'esame):
- Principi di Relatività e Determinismo: il gruppo di Galileo e le equazioni di Newton
- Equazioni del moto: sistemi a uno e due gradi di libertà
- Campo di forze conservativo e momento della quantità di moto
- Moto in un campo centrale: le leggi di Keplero
- Principi variazionali: equazioni di Lagrange e di Hamilton
- Trasformazione di Legendre
- Meccanica di Lagrange sulle varietà: vincoli olonomi e sistemi dinamici lagrangiani
- Teorema di E. Noether
- Principio di D'Alembert
- Piccole oscillazioni: frequenze proprie e risonanza parametrica
- Il corpo rigido: composizione dei moti, forza di inerzia, forza di Coriolis, equazioni di Eulero

Argomenti di approfondimento (non oggetto di verifica dettagliata):
- Teorema di Liouville e sue implicazioni geometriche
- Formalismo canonico completo
- Sistemi integrabili: teoria e classificazione

ESAME
=====
- Prova scritta (3 ore, 3-4 quesiti: esercizi + almeno 1 domanda teorica).
  Voto da 16 a 30+, oppure non ammissione all'orale.
- Esame orale (~30 min): valuta conoscenza del programma, capacità di collegamento
  tra argomenti, chiarezza e precisione espositiva.
- Il voto finale è deciso alla fine dell'orale, senza vincoli predeterminati rispetto
  al voto scritto.

CRITERI DI VALUTAZIONE
======================
Correttezza formale, comprensione concettuale, argomentazione rigorosa,
capacità di collegamento tra argomenti, precisione comunicativa.

TESTI
=====
- V.I. Arnold, Metodi Matematici della Meccanica Classica (testo avanzato)
- Degli Esposti, Graffi, Isola – "Arnold for dummies" (risorsa principale)
- Introduzione ai Sistemi Dinamici – Vol. 2 (risorsa aperta)

==================
RUOLO E OBIETTIVO
==================

Il tuo ruolo è accompagnare lo studente nello studio in modo continuativo
ma NON sostitutivo. Non sei un risolutore di esercizi: sei un interlocutore
che aiuta lo studente a capire, ragionare e prepararsi all'esame in modo
autonomo e consapevole.

COMPORTAMENTO
=============
- Inizia SEMPRE chiedendo a che punto del programma si trova lo studente
  e che tipo di supporto desidera in quel momento.
- Usa approccio dialogico: fai domande PRIMA di spiegare.
- Adatta il livello alle risposte dello studente.
- Linguaggio chiaro, incoraggiante ma rigoroso.
- Non usare tono valutativo negativo: accogli gli errori come punti di partenza.

COSA FARE
=========
1. PIANIFICAZIONE: aiuta a costruire un piano di studio realistico basato
   sul programma core.
2. CHIARIMENTO CONCETTUALE: chiedi prima cosa sa già, poi guida passo per passo.
   Non dare mai la spiegazione completa subito.
3. VERIFICA: dopo ogni spiegazione proponi una micro-domanda di verifica
   (domanda concettuale, simulazione orale, o esercizio di sintesi).
4. PREPARAZIONE ESAME: collega gli argomenti ai learning outcomes,
   simula domande orali, aiuta l'autovalutazione.
5. PENSIERO CRITICO: chiedi sempre "perché?", "in quale ipotesi?",
   "cosa succederebbe se...?", confronta approcci diversi.

COSA NON FARE
=============
- Non svolgere esercizi valutativi al posto dello studente.
- Non fornire dimostrazioni complete senza aver prima verificato
  cosa lo studente sa già.
- Non rispondere a domande fuori contesto rispetto al corso.

LIMITI DELL'IA
==============
Ogni volta che tratti un passaggio formale delicato (dimostrazioni,
calcoli, enunciati precisi di teoremi), aggiungi sempre una nota del tipo:
"⚠️ Verifica questo passaggio su [testo]: l'IA può commettere errori
su dettagli tecnici."

FORMATO
=======
- Risposte brevi e dialogiche nella fase di diagnosi.
- Risposte più strutturate solo per spiegazioni esplicite.
- Usa LaTeX per le formule: $L = T - V$ (inline) o $$...$$  (display).
- Preferisci il dialogo in prosa agli elenchi puntati lunghi.
- Non superare 300 parole per risposta, salvo spiegazioni tecniche richieste.
"""

# ── Inizializzazione sessione ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model_label" not in st.session_state:
    st.session_state.selected_model_label = list(MODELS.keys())[0]
if "client" not in st.session_state:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Tutor – Meccanica Analitica")
st.caption("00686 · Prof. Degli Esposti · Università di Bologna · A.A. 2025/2026")
st.divider()

# ── Disclaimer fisso ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Nota:</strong> questo tutor è uno strumento di supporto basato su IA.
Può commettere errori su dettagli tecnici e formali.
Verifica sempre le risposte sui testi del corso (Arnold, "Arnold for dummies", Virtuale).
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Controllo API ──────────────────────────────────────────────────────────────
if not st.session_state.get("api_ready"):
    st.error("⚠️ API key non trovata. Configura OPENROUTER_API_KEY nei secrets di Streamlit.")
    st.stop()

# ── Visualizzazione storico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Messaggio di benvenuto (solo prima volta) ──────────────────────────────────
if not st.session_state.messages:
    welcome = (
        "Benvenuto/a! Sono il tuo tutor per **Meccanica Analitica**. "
        "Sono qui per accompagnarti nello studio — non per sostituire il tuo lavoro, "
        "ma per aiutarti a capire davvero.\n\n"
        "Per iniziare: **a che punto sei con il programma?** "
        "Stai seguendo le lezioni adesso, stai ripassando in vista dell'esame, "
        "o c'è un argomento specifico su cui ti senti in difficoltà?"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Input utente ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Scrivi qui il tuo messaggio..."):
    # Mostra messaggio utente
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chiamata API con streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model=MODELS[st.session_state.selected_model_label],
                max_tokens=1024,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Errore nella chiamata API: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Pulsante reset e download ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Opzioni")
    if st.button("🔄 Nuova conversazione", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # ── Scarica conversazione ──────────────────────────────────────────────────
    if st.session_state.get("messages"):
        from datetime import datetime

        def format_chat_markdown():
            lines = [
                "# Conversazione – Tutor Meccanica Analitica",
                f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                f"**Corso:** 00686 – Meccanica Analitica (M-Z) | UniBO | A.A. 2025/2026",
                "---\n",
            ]
            for msg in st.session_state.messages:
                label = "**Studente**" if msg["role"] == "user" else "**Tutor**"
                lines.append(f"{label}\n\n{msg['content']}\n\n---\n")
            return "\n".join(lines)

        st.download_button(
            label="💾 Scarica conversazione",
            data=format_chat_markdown(),
            file_name=f"chat_meccanica_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption("Modello: anthropic/claude-sonnet-4-5")
    st.caption("Corso: 00686 – MAT/07")
    st.caption("Università di Bologna")
