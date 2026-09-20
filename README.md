# Research Insight Synthesizer

Turns raw, messy user-research notes into structured product insight —
recurring themes, contradictions worth digging into, and the most specific
verbatim quotes.

## Why this exists

While doing user research for product management case studies, I kept
manually prompting ChatGPT/Claude the same way after every round of
interviews: paste the notes, ask it to cluster themes, flag contradictions,
and surface the sharpest quotes. This project turns that repeatable manual
habit into an actual tool.

## What it does

1. Paste raw research notes (interview summaries, call transcripts, support
   tickets, reviews) into the app.
2. It calls the Claude API with a structured prompt.
3. It returns three things:
   - **Themes** — recurring patterns, grounded in what people actually said
   - **Contradictions** — where users disagree with each other or with their
     own stated behavior (the most valuable, most-often-ignored signal)
   - **Key quotes** — the sharpest, most specific lines, not the vaguest ones

## Run it yourself

```bash
pip install streamlit anthropic
export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

## Stack

Python, Streamlit, Anthropic API (Claude).

## Author

Sneha Chikhalkar — [Portfolio](https://bit.ly/SnehaPMPortfolio) | [LinkedIn](http://www.linkedin.com/in/sneha-chikhalkar)
