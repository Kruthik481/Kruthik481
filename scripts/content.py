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
        ("role", "Full-Stack / Backend Engineer"),
        ("focus", "APIs · Real-time Systems · LLM Infra"),
        ("based", "Bengaluru, India · UTC+5:30"),
    ),
    (
        ("languages", "Python · TypeScript · Go · C++"),
        ("backend", "FastAPI · Fastify · Go · Socket.IO"),
        ("data", "PostgreSQL · Redis · Redis Streams · Redpanda"),
        ("realtime", "WebSockets · SSE · consumer groups"),
        ("frontend", "Next.js · React · Tailwind · Motion"),
        ("llm", "gpt-oss · Groq · OpenRouter · agents · RAG"),
        ("ml", "scikit-learn · SciPy · Stable-Baselines3"),
        ("ship", "Docker · GitHub Actions · Vercel · Render"),
    ),
    (
        ("shipped", "8 systems · 7 live demos"),
        ("proof", "race-tested matching, budgets and ledgers"),
    ),
)
STATUS = "open to full-stack & backend roles"


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
        slug="gateway",
        name="LLM Gateway",
        kind="LLM infrastructure",
        context="Personal project · 2026",
        lines=(
            "An OpenAI-compatible gateway: issued keys, per-key rate",
            "limits, daily token budgets, a cache, and Groq to",
            "OpenRouter fallback before the first token.",
        ),
        metric="30",
        metric_label=("of 50 parallel requests admitted on a", "budget that fits 30: one Lua script"),
        stack=("FastAPI", "Redis Lua", "Postgres", "Next.js"),
        repo=f"{GITHUB}/llm-gateway",
        live="https://llm-gateway-five.vercel.app",
    ),
    Project(
        slug="streamguard",
        name="StreamGuard",
        kind="Stream processing",
        context="Personal project · 2026",
        lines=(
            "Card-fraud scoring over a partitioned stream. Kill a",
            "worker mid-run: survivors reclaim its partitions in",
            "order, and nothing is lost or scored twice.",
        ),
        metric="1,000",
        metric_label=("tx scored while a worker dies every", "50 ms: same alerts as one worker"),
        stack=("Go", "Redis Streams", "Redpanda", "Postgres"),
        repo=f"{GITHUB}/streamguard",
        live="https://streamguard-pied.vercel.app",
    ),
    Project(
        slug="movienight",
        name="Movie Night Matcher",
        kind="Real-time multiplayer",
        context="Personal project · 2026",
        lines=(
            "Friends swipe one shared movie deck in real time; the",
            "first film everyone likes wins. Row locks keep two",
            "last-second likes from losing the match.",
        ),
        metric="0",
        metric_label=("matches lost to concurrent final likes;", "3 of 3 lost without the lock"),
        stack=("Fastify", "Socket.IO", "Prisma", "Next.js"),
        repo=f"{GITHUB}/movie-night-matcher",
        live="https://movie-night-matcher-eta.vercel.app",
    ),
    Project(
        slug="significant",
        name="Significant",
        kind="Experiment statistics",
        context="Personal project · 2026",
        lines=(
            "A/B test readouts you can defend: the split is checked",
            "first, CUPED tightens the interval, and the p-value",
            "stays valid however often you peek.",
        ),
        metric="12k",
        metric_label=("of 40,000 users were enough to stop", "the checkout test safely"),
        stack=("FastAPI", "NumPy", "SciPy", "Next.js"),
        repo=f"{GITHUB}/significant",
        live="https://significant-lyart.vercel.app",
    ),
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
    ("Prove the race", "Concurrency bugs get a failing test before a fix."),
    ("Fail closed", "No Redis, no limits: the gateway answers 503."),
    ("Publish the misses", "Failed runs sit in the repo next to the good ones."),
)
