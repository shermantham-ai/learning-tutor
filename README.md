# AI Learning Tutor

A web-based AI tutor that teaches you **how to code** and **how to learn** — built with Python, Streamlit, and the Anthropic Claude API.

---

## What This App Does

You chat with an AI tutor named **Sage** who:
- Teaches Python programming from scratch
- Explains *why* things work, not just *how*
- Gives you hints before answers so you actually learn
- Teaches meta-skills like breaking problems down and reading error messages

---

## Before You Start — What You Need

1. **Python 3.9 or newer** — check by running `python --version` in your terminal
   - If you don't have it: download from [python.org](https://www.python.org/downloads/)
2. **An Anthropic API key** — get one free at [console.anthropic.com](https://console.anthropic.com/settings/keys)
3. **A terminal** — on Windows, use PowerShell or Command Prompt

---

## Setup (Do This Once)

### Step 1 — Open a terminal and go to this folder

```
cd C:\Users\sherm\.codex\learning-tutor
```

### Step 2 — Create a virtual environment (keeps this project's packages separate)

```
python -m venv venv
```

Then activate it:

- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (Command Prompt):** `.\venv\Scripts\activate.bat`
- **Mac/Linux:** `source venv/bin/activate`

You should see `(venv)` appear at the start of your terminal prompt — that means it worked.

### Step 3 — Install dependencies

```
pip install -r requirements.txt
```

This installs three packages:
- `anthropic` — the official Python library for talking to Claude
- `streamlit` — turns Python scripts into web apps
- `python-dotenv` — loads your API key from a file

### Step 4 — Add your API key

Copy the example file and fill in your real key:

```
copy .env.example .env
```

Open `.env` in any text editor and replace `your-api-key-here` with your actual key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

> **Important:** Never share your `.env` file or commit it to git. It contains your private API key.

---

## Running the App

Every time you want to use the tutor:

1. Open a terminal in this folder
2. Activate your virtual environment (Step 2 above)
3. Run:

```
streamlit run app.py
```

4. Your browser will open automatically at `http://localhost:8501`
5. Start chatting with Sage!

To stop the app: press `Ctrl+C` in the terminal.

---

## How the Code Works (High-Level)

```
You type a message
       ↓
app.py adds it to st.session_state.messages  ← this is your "memory"
       ↓
app.py sends ALL messages to Claude via the Anthropic API
       ↓
Claude reads the full conversation + system prompt (tutor instructions)
       ↓
Claude replies
       ↓
app.py adds the reply to messages and displays it
       ↓
Next message, repeat — Claude always sees the full history
```

**Why send all messages every time?** The Claude API is *stateless* — it doesn't remember previous calls. So we pass the entire conversation each time. This is the standard pattern for building chatbots with LLM APIs.

**What is prompt caching?** The system prompt (tutor instructions) is long and sent every call. With `cache_control: {type: "ephemeral"}`, Anthropic caches it for ~5 minutes — so you only pay full price once, then get ~90% discounts on the cached portion. Watch the "Cache read tokens" counter in the sidebar grow!

---

## Project Structure

```
learning-tutor/
├── app.py              ← Main application (start here)
├── requirements.txt    ← Python packages to install
├── .env.example        ← Template for your API key
├── .env                ← Your actual API key (don't share this!)
└── README.md           ← This file
```

---

## Phase 2 — Coming Soon

The code already contains stubs for three tools Claude will be able to call:

| Tool | What it will do |
|------|-----------------|
| `get_lesson(topic)` | Pull up a structured lesson on any topic |
| `generate_exercise(topic, level)` | Create a hands-on coding challenge |
| `check_answer(code, exercise_id)` | Automatically evaluate your code and give feedback |

In Phase 2, you'll uncomment `tools=TOOLS` in `app.py` and implement the tool functions. Claude will then be able to run these tools *during* a conversation — that's what makes it "agentic."

---

## Troubleshooting

**"streamlit: command not found"** — Your virtual environment isn't activated. Run the activate command from Step 2.

**"AuthenticationError"** — Your API key is wrong or missing. Double-check your `.env` file.

**"ModuleNotFoundError"** — Run `pip install -r requirements.txt` again.

**The page is blank** — Try refreshing. If still blank, check the terminal for error messages.

**PowerShell says "running scripts is disabled"** — Run this once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
