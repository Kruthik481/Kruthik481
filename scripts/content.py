"""Every word and number on the profile. Figures are checkable in the linked repositories."""

from dataclasses import dataclass

GITHUB = "https://github.com/Kruthik481"

LINKS = {
    "portfolio": "https://kruthik-n.vercel.app",
    "linkedin": "https://www.linkedin.com/in/kruthik-n-8a22b62a5",
    "email": "mailto:kruthikn05@gmail.com",
    "x": "https://x.com/OcraKruthik",
}

# (key, value) rows of the whoami card, in groups separated by a rule.
WHOAMI: tuple[tuple[tuple[str, str], ...], ...] = (
    (
        ("role", "AI/ML Engineer"),
        ("focus", "Applied LLMs · Agentic Systems"),
        ("based", "Bengaluru, India · UTC+5:30"),
    ),
    (
        ("stack", "Python · C++"),
        ("agents", "planning · tool use · human-in-the-loop"),
        ("retrieval", "FAISS · BM25 · rank fusion · embeddings"),
        ("models", "Groq · Ollama · gpt-oss · Llama"),
        ("ml", "scikit-learn · Stable-Baselines3 · Gymnasium"),
        ("services", "FastAPI · WebSockets · Celery · PostgreSQL"),
        ("interfaces", "React · TypeScript · Vite"),
        ("ship", "Docker · GitHub Actions · Vercel · Render"),
    ),
    (
        ("shipped", "4 systems · 3 live demos · 485 tests"),
        ("proof", "97% straight-through, 0 wrong postings"),
    ),
)
STATUS = "open to AI/ML engineering roles"


@dataclass(frozen=True)
class Project:
    slug: str
    name: str
    kind: str
    context: str
    lines: tuple[str, ...]  # tagline, pre-wrapped to fit the card
    metric: str
    metric_label: tuple[str, ...]
    stack: tuple[str, ...]
    repo: str
    live: str | None = None


PROJECTS = (
    Project(
        slug="zentinel",
        name="Zentinel",
        kind="Multi-agent orchestration",
        context="Personal project · 2026",
        lines=(
            "A supervisor plans each request as a graph of subtasks.",
            "Specialist agents run them with real tools, and a person",
            "approves the steps that matter.",
        ),
        metric="0",
        metric_label=("secrets reachable from code its agents", "write: it runs in a no-network microVM"),
        stack=("FastAPI", "Groq", "Vercel Sandbox", "React"),
        repo=f"{GITHUB}/zentinel",
        live="https://zentinel.onrender.com",
    ),
    Project(
        slug="recon",
        name="Reconciliation Agent",
        kind="Payments, built to abstain",
        context="Razorpay AI Buildathon 2026",
        lines=(
            "Rules clear the mechanical breaks; a model with read-only",
            "tools takes the rest; a gate recomputes every number",
            "before anything is posted.",
        ),
        metric="97%",
        metric_label=("cleared straight through across 500 cases,", "with 0 incorrect postings"),
        stack=("Python", "LLM tool use", "Rules engine", "Evals"),
        repo=f"{GITHUB}/razorpay-recon-agent",
    ),
    Project(
        slug="stacksense",
        name="StackSense",
        kind="Retrieval over codebases",
        context="Personal project · 2026",
        lines=(
            "Ask a repository questions in plain English. Meaning and",
            "exact-name search are fused, then the files each match",
            "depends on are pulled in.",
        ),
        metric="211",
        metric_label=("tests behind a pipeline you can try live,", "on StackSense's own source"),
        stack=("FAISS", "BM25", "FastAPI", "Ollama"),
        repo=f"{GITHUB}/stacksense",
        live="https://stacksense-eight.vercel.app",
    ),
    Project(
        slug="alphaforge",
        name="AlphaForge",
        kind="Reinforcement learning for markets",
        context="Personal project · 2026",
        lines=(
            "A PPO agent learns a trading policy in a custom Gymnasium",
            "environment; a Markowitz optimiser finds the max-Sharpe",
            "portfolio. Results reported as they came out.",
        ),
        metric="+19.8%",
        metric_label=("best test run, against +21.5% for", "buy-and-hold. The write-up says so."),
        stack=("PPO", "Gymnasium", "Celery", "React"),
        repo=f"{GITHUB}/AlphaForge",
        live="https://alpha-forge-vert.vercel.app",
    ),
)

# Three rules the work above follows, each with the evidence for it.
PRINCIPLES = (
    ("Rules before models", "86% of reconciliation breaks never reach an LLM."),
    ("Verify, then act", "Every model verdict is recomputed before it counts."),
    ("Publish the misses", "Failed runs sit in the repo next to the good ones."),
)
