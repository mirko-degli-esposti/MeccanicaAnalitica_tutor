# 🎓 Tutor IA – Meccanica Analitica

Applicazione web basata su Streamlit e Claude (Anthropic API) per supportare
gli studenti del corso 00686 – Meccanica Analitica (M-Z), Università di Bologna.

---

## Struttura del progetto

```
tutor_app/
├── app.py                   # Applicazione principale
├── requirements.txt         # Dipendenze Python
├── .gitignore               # Protegge i file sensibili
├── .streamlit/
│   └── secrets.toml         # API key (NON caricare su GitHub)
└── README.md
```

---

## Come eseguire in locale (test)

### 1. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2. Configura la API key
Apri `.streamlit/secrets.toml` e inserisci la tua chiave:
```toml
ANTHROPIC_API_KEY = "sk-ant-la-tua-chiave"
```

### 3. Avvia l'app
```bash
streamlit run app.py
```
L'app si aprirà automaticamente su `http://localhost:8501`

---

## Deploy su Streamlit Cloud (hosting gratuito)

### Passo 1 — Crea un repository GitHub
1. Vai su [github.com](https://github.com) e crea un nuovo repository
   (es. `tutor-meccanica-analitica`)
2. Carica tutti i file del progetto **TRANNE** `.streamlit/secrets.toml`
   (è già in `.gitignore`, non verrà incluso automaticamente)

```bash
git init
git add .
git commit -m "Prima versione tutor"
git remote add origin https://github.com/TUO-USERNAME/tutor-meccanica-analitica.git
git push -u origin main
```

### Passo 2 — Connetti Streamlit Cloud
1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. Accedi con il tuo account GitHub
3. Clicca **"New app"**
4. Seleziona il repository e il file `app.py`
5. Clicca **"Deploy"**

### Passo 3 — Aggiungi la API key in modo sicuro
1. Nella dashboard di Streamlit Cloud, vai su **Settings → Secrets**
2. Incolla il contenuto seguente:
```toml
ANTHROPIC_API_KEY = "sk-ant-la-tua-chiave"
```
3. Salva — l'app si riavvierà automaticamente

### Passo 4 — Condividi il link
Streamlit Cloud ti fornirà un URL pubblico del tipo:
```
https://tutor-meccanica-analitica-XXXXXX.streamlit.app
```
Incollalo su Virtuale o invialo agli studenti.

---

## Personalizzare per altri corsi

Per adattare il tutor a un corso diverso:

1. Apri `app.py`
2. Modifica la variabile `SYSTEM_PROMPT`:
   - Aggiorna il nome del corso, docente, CFU
   - Sostituisci il syllabus nella sezione `SYLLABUS DEL CORSO`
   - Aggiorna le informazioni sull'esame
3. Aggiorna titolo e caption nelle righe `st.title()` e `st.caption()`

---

## Costi stimati (Anthropic API)

- Modello usato: `claude-sonnet-4-5`
- Costo indicativo: ~$0.003 per conversazione media (10-15 scambi)
- Per 100 studenti attivi al mese: circa $1–5/mese
- Monitorabile su [console.anthropic.com](https://console.anthropic.com)

> **Consiglio:** imposta un budget limit sulla console Anthropic
> per evitare costi imprevisti.

---

## Sicurezza

- La API key non è mai esposta nel codice sorgente
- Il file `secrets.toml` è escluso da Git tramite `.gitignore`
- Su Streamlit Cloud la key è cifrata nei secrets della piattaforma

---

## Limiti e avvertenze

Questo tutor è uno strumento di supporto didattico basato su IA generativa.
Può commettere errori su dettagli tecnici e formali. Gli studenti sono
sempre invitati a verificare le risposte sui testi del corso.
