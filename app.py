"""
Research Insight Synthesizer
-----------------------------
Turns raw, messy user-research notes (interview transcripts, support tickets,
call summaries) into structured product insight: recurring themes,
contradictions worth digging into, and the most specific verbatim quotes.

Why this exists: when doing PM case-study research, I kept manually prompting
ChatGPT/Claude the same way after every round of interviews. This turns that
repeatable manual workflow into an actual tool instead of a habit.

Run locally:
    pip install streamlit anthropic
    export ANTHROPIC_API_KEY=your_key_here
    streamlit run app.py

Or deploy free on Streamlit Community Cloud (share.streamlit.io) connected
to a GitHub repo containing this file + requirements.txt.
"""

import streamlit as st
from anthropic import Anthropic
import json

st.set_page_config(page_title="Research Insight Synthesizer", page_icon="🔍", layout="centered")

st.title("🔍 Research Insight Synthesizer")
st.markdown(
    """
    Paste raw, messy user research below — interview notes, call transcripts,
    support tickets, review dumps. This tool does what I used to do manually
    before every PRD: cluster the noise into themes, flag contradictions worth
    digging into, and pull out the most specific quotes — because exact user
    language usually reveals the real problem better than my own paraphrasing.
    """
)

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Anthropic API Key", type="password", help="Get one at console.anthropic.com")
    st.markdown("---")
    st.markdown(
        "**Why this project:** built for a PM internship application that "
        "asked for something 'that works, polish optional.' This automates a "
        "manual research-synthesis workflow I already used across three "
        "product case studies."
    )

notes = st.text_area(
    "Paste raw research notes here",
    height=280,
    placeholder="e.g. 10 interview summaries, support tickets, App Store reviews, call notes...",
)

SYSTEM_PROMPT = """You are a sharp product research analyst. Given raw, unstructured \
user research notes, produce a structured synthesis with exactly three sections:

1. THEMES: 3-6 recurring patterns across the notes, each as a short bolded \
label followed by a one-sentence explanation grounded in what people actually said.
2. CONTRADICTIONS: Points where users disagree with each other or where \
stated opinions conflict with described behavior. These are the most \
valuable signal — flag them explicitly, don't smooth them over.
3. KEY QUOTES: 3-5 short, verbatim-style quotes (paraphrase only if no \
direct line exists) that are the most specific and revealing — prefer a \
sharp, concrete complaint over a vague, polite one.

Be concise. Do not pad with generic PM language. Ground every point in the \
actual text provided; do not invent findings not supported by the notes."""


def synthesize(api_key: str, raw_notes: str) -> str:
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Raw research notes:\n\n{raw_notes}"}],
    )
    return "".join(block.text for block in response.content if hasattr(block, "text"))


col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("Synthesize", type="primary", use_container_width=True)
with col2:
    st.caption("Uses claude-sonnet-4-5 via the Anthropic API")

if run:
    if not api_key:
        st.warning("Add your Anthropic API key in the sidebar first.")
    elif not notes.strip():
        st.warning("Paste some research notes first.")
    else:
        with st.spinner("Synthesizing..."):
            try:
                result = synthesize(api_key, notes)
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption(
    "Built by Sneha Chikhalkar · [Portfolio](https://bit.ly/SnehaPMPortfolio) · "
    "[GitHub](https://github.com/SnehaChikhalkar)"
)
