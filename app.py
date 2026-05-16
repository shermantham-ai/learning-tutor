"""
AI Learning Tutor - Phase 1 (Working Chat) + Phase 2 Stubs
============================================================
This app lets you chat with an AI tutor that teaches you how to code
and how to learn effectively.

HOW IT WORKS (big picture):
1. You type a message in the chat box at the bottom
2. Your message gets added to a list called `messages`
3. We send the ENTIRE messages list to Claude (so it remembers the conversation)
4. Claude replies, we add that to messages too
5. Streamlit redraws the screen showing all messages
"""

import os  # Read environment variables (like your API key)
import anthropic  # The official Anthropic Python library
import streamlit as st  # Turns Python scripts into web apps
from dotenv import load_dotenv  # Loads variables from your .env file


# ─── SETUP ───────────────────────────────────────────────────────────────────

# Load ANTHROPIC_API_KEY from .env file into the environment
load_dotenv()

# Create the Anthropic client — this is your connection to Claude
# It automatically reads ANTHROPIC_API_KEY from the environment
client = anthropic.Anthropic()


# ─── SYSTEM PROMPT ───────────────────────────────────────────────────────────
# The system prompt is a special instruction that tells Claude HOW to behave.
# It's sent with every message but the user never sees it.
# We make it long on purpose — prompt caching needs ~1024+ tokens to activate.

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
- Web scraping basics
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

# Prompt caching: wrapping the system prompt in a list with cache_control
# tells Anthropic to cache this text after the first request.
# Result: ~90% cheaper on repeated calls (the cached part isn't re-processed).
# Note: caching activates only when the prompt is 1024+ tokens — ours qualifies!
SYSTEM = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},  # "ephemeral" = cache for ~5 minutes
    }
]


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
    # First time the app loads — start with an empty conversation
    st.session_state.messages = []

# Also track token usage so you can see caching in action
if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0
if "total_cache_read_tokens" not in st.session_state:
    st.session_state.total_cache_read_tokens = 0


# ─── DISPLAY EXISTING MESSAGES ───────────────────────────────────────────────
# Loop through every message in history and render it in the chat UI.
# `role` is either "user" (you) or "assistant" (Claude/Sage).

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # Creates a chat bubble with the right avatar
        st.markdown(msg["content"])    # Renders markdown formatting in replies


# ─── PHASE 2 TOOL STUBS ──────────────────────────────────────────────────────
# These functions are PLACEHOLDERS for Phase 2 (agentic tool use).
# In Phase 2, Claude will be able to CALL these functions automatically
# to generate lessons, exercises, and check your answers.
# For now, they just return placeholder text.

def get_lesson(topic: str) -> str:
    """
    PHASE 2 STUB — Fetch a structured lesson on a topic.

    In Phase 2, this will:
    - Look up a lesson template for the given topic
    - Possibly fetch examples from a lessons database
    - Return a formatted lesson with theory + examples

    Example call: get_lesson("for loops")
    """
    # TODO Phase 2: Replace with real lesson lookup logic
    return f"[STUB] Lesson on '{topic}' — Phase 2 will fill this in."


def generate_exercise(topic: str, level: str = "beginner") -> dict:
    """
    PHASE 2 STUB — Generate a coding exercise for a topic and skill level.

    In Phase 2, this will:
    - Pick an exercise template matching topic + level
    - Fill in variables (e.g., different numbers or scenarios each time)
    - Return the exercise description AND a hidden solution for checking

    Example call: generate_exercise("variables", "beginner")
    Returns: {"exercise_id": "...", "description": "...", "starter_code": "..."}
    """
    # TODO Phase 2: Replace with real exercise generation logic
    return {
        "exercise_id": "stub-001",
        "description": f"[STUB] Exercise on '{topic}' at {level} level — Phase 2 will fill this in.",
        "starter_code": "# Your code here\n",
    }


def check_answer(code: str, exercise_id: str) -> dict:
    """
    PHASE 2 STUB — Check a student's code answer against an exercise.

    In Phase 2, this will:
    - Safely run the student's code in a sandbox
    - Compare output/behavior against expected results
    - Return detailed feedback: what passed, what failed, hints for fixes

    Example call: check_answer("print('hello')", "ex-001")
    Returns: {"passed": True/False, "feedback": "...", "hints": [...]}
    """
    # TODO Phase 2: Replace with real code execution + checking logic
    return {
        "passed": False,
        "feedback": f"[STUB] Answer check for exercise '{exercise_id}' — Phase 2 will fill this in.",
        "hints": ["This is a placeholder hint."],
    }


# PHASE 2 TOOL DEFINITIONS
# These describe the tools to Claude in the format the API expects.
# When Claude sees these definitions, it can decide to "call" a tool
# by outputting a special tool_use block instead of plain text.
TOOLS = [
    {
        "name": "get_lesson",
        "description": "Retrieve a structured lesson on a specific coding topic. Use this when the student asks to learn about a topic from scratch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The coding topic to teach, e.g. 'for loops', 'dictionaries', 'functions'",
                }
            },
            "required": ["topic"],
        },
    },
    {
        "name": "generate_exercise",
        "description": "Generate a hands-on coding exercise for a topic at the student's level. Use this when the student wants practice or asks for an exercise.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to practice, e.g. 'variables', 'lists'",
                },
                "level": {
                    "type": "string",
                    "enum": ["beginner", "intermediate", "advanced"],
                    "description": "The difficulty level for the exercise",
                },
            },
            "required": ["topic"],
        },
    },
    {
        "name": "check_answer",
        "description": "Check a student's code answer to an exercise and provide feedback. Use this when the student submits code for evaluation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The student's Python code to evaluate",
                },
                "exercise_id": {
                    "type": "string",
                    "description": "The ID of the exercise being answered",
                },
            },
            "required": ["code", "exercise_id"],
        },
    },
]


# ─── CHAT INPUT & RESPONSE ───────────────────────────────────────────────────
# `st.chat_input` renders the text box at the bottom of the screen.
# It returns None until the user hits Enter, then returns their message.

if prompt := st.chat_input("Ask Sage anything — what would you like to learn?"):

    # 1. Add the user's message to our conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Display the user's message immediately (don't wait for the response)
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Call the Claude API
    # We send the ENTIRE messages list — that's how Claude "remembers" the chat.
    # The API is stateless (it forgets everything between calls), so we must
    # always pass the full history ourselves.
    with st.chat_message("assistant"):
        with st.spinner("Sage is thinking..."):
            response = client.messages.create(
                model="claude-haiku-4-5",   # Fast and affordable model
                max_tokens=2048,            # Maximum length of Claude's reply
                system=SYSTEM,             # The cached system prompt (tutor instructions)
                messages=st.session_state.messages,  # Full conversation history
                # Phase 2: Uncomment the line below to enable tool use
                # tools=TOOLS,
            )

        # 4. Extract the text reply from the response
        # response.content is a list — for plain text, we want the first item's .text
        reply = response.content[0].text

        # 5. Display the reply
        st.markdown(reply)

        # 6. Track token usage (visible in the sidebar — see below)
        usage = response.usage
        st.session_state.total_input_tokens += usage.input_tokens
        if hasattr(usage, "cache_read_input_tokens"):
            st.session_state.total_cache_read_tokens += usage.cache_read_input_tokens

    # 7. Add Claude's reply to history so the next message includes it
    st.session_state.messages.append({"role": "assistant", "content": reply})


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
# The sidebar shows stats and controls. It's a great place for "meta" features.

with st.sidebar:
    st.header("Session Info")

    # Show conversation length
    user_msg_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.metric("Messages sent", user_msg_count)

    # Show token usage — this is how you see prompt caching working!
    # After the first message, "Cache reads" should rise while "Input tokens"
    # stays roughly the same (the system prompt is being served from cache).
    st.metric("Total input tokens", st.session_state.total_input_tokens)
    st.metric("Cache read tokens", st.session_state.total_cache_read_tokens)

    st.divider()

    # Clear conversation button
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_input_tokens = 0
        st.session_state.total_cache_read_tokens = 0
        st.rerun()  # Re-run the script to refresh the UI

    st.divider()
    st.caption("**Phase 2 coming soon:**")
    st.caption("- 📚 Structured lessons")
    st.caption("- 🏋️ Coding exercises")
    st.caption("- ✅ Automatic answer checking")
