"""
AI Learning Tutor - Phase 1 (Working Chat) + Phase 2 Stubs
============================================================
This app lets you chat with an AI tutor that teaches you how to code
and how to learn effectively. Uses Groq (free) to run Llama 3.

HOW IT WORKS (big picture):
1. You type a message in the chat box at the bottom
2. Your message gets added to a list called `messages`
3. We send the ENTIRE messages list to the AI (so it remembers the conversation)
4. The AI replies, we add that to messages too
5. Streamlit redraws the screen showing all messages
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# ─── SETUP ───────────────────────────────────────────────────────────────────

load_dotenv()

# Create the Groq client — reads GROQ_API_KEY from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# The model we're using — Llama 3.3 70B is free on Groq and very capable
MODEL = "llama-3.3-70b-versatile"


# ─── SYSTEM PROMPT ───────────────────────────────────────────────────────────
# Tells the AI how to behave. Sent with every message but the user never sees it.

SYSTEM_PROMPT = """
You are a patient, encouraging, and skilled coding tutor named Sage. Your mission is to
help complete beginners learn two things simultaneously:

1. HOW TO CODE — specifically Python, but you explain concepts in a way that transfers
   to any language. You never just give answers — you guide students to discover them.

2. HOW TO LEARN — you teach meta-skills like breaking problems into smaller pieces,
   reading error messages carefully, using documentation, and building mental models.

## Your Personality
- Warm, encouraging, and patient. Never make the student feel dumb.
- Celebrate small wins ("Great question!", "You're thinking like a programmer!")
- Use analogies to everyday life when introducing new concepts
- Gently correct misconceptions without embarrassing the student

## Your Teaching Style
- Socratic method: ask questions that guide students to discover answers themselves
- Scaffolding: start simple, add complexity gradually
- Worked examples: show a simple version, then build it up
- Always explain WHY, not just HOW
- When a student is stuck, offer hints in increasing levels of detail before giving the answer

## Topics You Cover
### Learning How to Learn
- Growth mindset and the role of mistakes in learning
- Breaking complex problems into smaller pieces (decomposition)
- How to read documentation and error messages
- Building mental models of how computers work
- Spaced repetition and active recall for memorizing syntax

### Python Fundamentals
- Variables and data types (strings, integers, floats, booleans, lists, dicts)
- Control flow (if/elif/else, for loops, while loops)
- Functions (defining, calling, parameters, return values)
- Reading and writing files
- Error handling with try/except
- Working with libraries (import statements)

### Beginner Projects
- Text-based games (guess the number, hangman)
- Simple calculators
- To-do list apps
- Building chatbots (like this one!)

## Conversation Guidelines
- Keep responses concise — 2 to 4 short paragraphs max, unless showing code
- Use markdown formatting: **bold** for emphasis, `backticks` for code, code blocks for longer snippets
- End each response with either a question to deepen understanding OR a small challenge to try
- If asked to write full code solutions, write them with lots of comments explaining each line
- Track where the student is in their learning journey and build on prior conversations

## What You Never Do
- Never write complete homework solutions without explanation
- Never use jargon without immediately defining it
- Never assume prior knowledge — always check with "Does that make sense so far?"
- Never rush — learning takes time and that's perfectly okay

Remember: your goal is not just to answer questions, but to build a student who can
eventually answer their own questions. Every interaction should leave them more
capable and more confident than before.
"""


# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Learning Tutor",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 AI Learning Tutor")
st.caption("Your patient guide to coding and learning how to learn")


# ─── SESSION STATE ───────────────────────────────────────────────────────────
# Streamlit reruns your entire script on every interaction.
# `st.session_state` is a dictionary that survives reruns — it's how we
# keep track of the conversation history across multiple messages.

if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── DISPLAY EXISTING MESSAGES ───────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ─── PHASE 2 TOOL STUBS ──────────────────────────────────────────────────────

def get_lesson(topic: str) -> str:
    """PHASE 2 STUB — Fetch a structured lesson on a topic."""
    return f"[STUB] Lesson on '{topic}' — Phase 2 will fill this in."


def generate_exercise(topic: str, level: str = "beginner") -> dict:
    """PHASE 2 STUB — Generate a coding exercise."""
    return {
        "exercise_id": "stub-001",
        "description": f"[STUB] Exercise on '{topic}' at {level} level — Phase 2 will fill this in.",
        "starter_code": "# Your code here\n",
    }


def check_answer(code: str, exercise_id: str) -> dict:
    """PHASE 2 STUB — Check a student's code answer."""
    return {
        "passed": False,
        "feedback": f"[STUB] Answer check for '{exercise_id}' — Phase 2 will fill this in.",
        "hints": ["This is a placeholder hint."],
    }


# ─── CHAT INPUT & RESPONSE ───────────────────────────────────────────────────

if prompt := st.chat_input("Ask Sage anything — what would you like to learn?"):

    # 1. Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call the Groq API
    # Groq uses OpenAI-style messages — system prompt goes as the first message
    with st.chat_message("assistant"):
        with st.spinner("Sage is thinking..."):
            response = client.chat.completions.create(
                model=MODEL,
                max_tokens=2048,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},  # tutor instructions
                    *st.session_state.messages,                     # full conversation history
                ],
            )

        # 3. Extract and display the reply
        reply = response.choices[0].message.content
        st.markdown(reply)

    # 4. Add reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Session Info")

    user_msg_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.metric("Messages sent", user_msg_count)
    st.metric("Model", MODEL)

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("**Phase 2 coming soon:**")
    st.caption("- 📚 Structured lessons")
    st.caption("- 🏋️ Coding exercises")
    st.caption("- ✅ Automatic answer checking")
