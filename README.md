# CrewAI Study Assistant

A 3-agent AI crew that researches any topic on Google, explains it like you're a beginner, and quizzes you - all automatically.

**Agents:**
- **Researcher** — searches Google and compiles a structured report
- **Explainer** — rewrites the research as a beginner-friendly explanation with analogies
- **Quiz Master** — generates a 5-question multiple choice quiz to test your understanding

**Output files produced in `outputs/` folder:**
- `01_research.md` — web research report
- `02_explanation.md` — beginner explanation with analogy and key takeaways
- `03_quiz.md` — 5-question MCQ quiz with answers

---

## Prerequisites

- Python 3.10 or higher
- A free Groq API key — https://console.groq.com
- A free Serper API key — https://serper.dev (2500 free searches/month)

---

## Setup (step by step)

### 1. Clone this repo
```bash
git clone <your-repo-url>
cd crewai-study-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
```bash
# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 4. Install all dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your API keys
Create a `.env` file in the root folder with this content:
```
GROQ_API_KEY=your_groq_key_here
SERPER_API_KEY=your_serper_key_here
```

- Groq key → https://console.groq.com → Sign up free → API Keys → Create Key
- Serper key → https://serper.dev → Sign up free → Dashboard → Copy API Key

### 6. Run it
```bash
python main.py "how does photosynthesis work"
```

Or run interactively (it will ask for a topic):
```bash
python main.py
```

---

## Project structure
```
crewai-study-assistant/
│
├── main.py            ← RUN THIS FILE
├── crew.py            ← agents, tasks, and crew definition
├── .env               ← your API keys
├── .gitignore         ← keeps secrets and venv out of git
├── requirements.txt   ← all dependencies
├── README.md          
│
└── outputs/           ← created automatically when you run
    ├── 01_research.md
    ├── 02_explanation.md
    └── 03_quiz.md
```

---
