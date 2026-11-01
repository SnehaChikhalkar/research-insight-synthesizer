import streamlit as st
from google import genai

st.set_page_config(page_title="Research Insight Synthesizer", page_icon="🔍", layout="wide")

# ---------- API key: use the secret if set, else ask in the sidebar ----------
secret_key = None
try:
    secret_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    secret_key = None

with st.sidebar:
    st.header("Setup")
    if secret_key:
        st.success("API key loaded. You can use the app directly.")
        api_key = secret_key
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get a free key at aistudio.google.com",
        )
    st.divider()
    st.markdown(
        "**Why this project:** built for a PM internship application that asked for "
        "something 'that works, polish optional.' This automates a manual "
        "research-synthesis workflow I already used across three product case studies."
    )

# ---------- Main page ----------
st.title("🔍 Research Insight Synthesizer")
st.caption("Paste raw research notes (interviews, feedback, observations) and get structured insights.")

notes = st.text_area("Paste raw research notes here", height=300)

PROMPT = """You are a senior product research analyst.
From the raw research notes below, produce a structured synthesis in Markdown:

## Key Themes
(3-5 themes, each with a one-line explanation)

## User Pain Points
(bullet list, most severe first)

## Key Insights
(non-obvious takeaways, each backed by evidence from the notes)

## Opportunities / Recommended Next Steps
(prioritized, actionable)

## Open Questions
(what the notes do not answer yet)

Only use information present in the notes. Do not invent facts.

NOTES:
{notes}
"""

col1, col2 = st.columns([1, 3])
with col1:
    run = st.button("Synthesize", type="primary", use_container_width=True)
with col2:
    st.caption("Uses Google Gemini (free tier)")

if run:
    if not api_key:
        st.warning("Add your Gemini API key in the sidebar first.")
    elif not notes.strip():
        st.warning("Paste some research notes first.")
    else:
        try:
            with st.spinner("Synthesizing..."):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=PROMPT.format(notes=notes),
                )
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("Built by Sneha Chikhalkar")
