<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Sans&weight=600&size=30&duration=3200&pause=900&color=3D7EFF&center=true&vCenter=true&width=760&lines=AI+%2B+Full-Stack+Engineer;RAG+%C2%B7+Agents+%C2%B7+Evals+%C2%B7+FastAPI+%C2%B7+React;I+build+AI+systems+and+prove+they+work" alt="AI + Full-Stack Engineer" />

<br/>

**I don't ship AI that "seems to work." I score it against a held-out answer key and publish the number.**

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/REPLACE-WITH-YOUR-LINKEDIN)
[![Gmail](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kruthikn05@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Kruthik481)

<img src="https://komarev.com/ghpvc/?username=Kruthik481&style=flat-square&color=3d7eff&label=profile+views" alt="profile views" />

</div>

---

## About

I build AI systems end to end — the retrieval layer, the agent loop, the FastAPI service around it, and the React dashboard on top — and then I measure them.

That last part is the whole point. My reconciliation agent clears **97% of payment breaks straight through at 100% precision, with zero incorrect postings**, scored against an answer key the system never sees. My code assistant ships **152 passing tests**. Every repo runs CI. When something fails, it goes in a `FAILURES.md` rather than quietly out of the changelog.

Most of my work sits where **applied AI meets financial systems**: reinforcement learning for trading policies, portfolio optimisation, settlement reconciliation.

---

## Tech Stack

**AI / ML**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=flat-square&logo=meta&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=lightning&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white)
![Gymnasium](https://img.shields.io/badge/Gymnasium-0081A5?style=flat-square&logo=openaigym&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

**Backend**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-010101?style=flat-square&logo=socketdotio&logoColor=white)

**Frontend**

![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?style=flat-square&logo=reactquery&logoColor=white)

**Data & Infra**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

---

## Featured Work

| Project | What it is | Measured result |
| :--- | :--- | :--- |
| **[razorpay-recon-agent](https://github.com/Kruthik481/razorpay-recon-agent)** | Payment reconciliation. Deterministic rules clear the mechanical breaks; an LLM is spent only on the ambiguous tail. Confirmed exceptions become new rules. | **97% straight-through, 100% precision, 0 incorrect postings** |
| **[stacksense](https://github.com/Kruthik481/stacksense)** | RAG code assistant. FAISS + BM25 fused by Reciprocal Rank Fusion, then a dependency graph injects each file's imports and dependents into context. | **152 tests passing**, fully local via Ollama |
| **[AlphaForge](https://github.com/Kruthik481/AlphaForge)** | Quant platform. A PPO agent learns a trading policy in a custom Gymnasium env; Markowitz optimisation finds the max-Sharpe portfolio. | Sharpe / Sortino / max-drawdown, **[live demo](https://alpha-forge-vert.vercel.app)** |
| **[zentinel](https://github.com/Kruthik481/zentinel)** | Multi-agent orchestration. A supervisor decomposes work into a DAG, routes subtasks to specialist agents with tools, and escalates to a human when unsure. | Concurrent DAG execution, human-in-the-loop |

<details>
<summary><b>Why these are worth a closer look</b></summary>

<br/>

**razorpay-recon-agent** — Built for the Razorpay AI Buildathon, AI Finance Controller track. The interesting decision is what the model *isn't* allowed to do: the system clears *matching* problems on its own and never clears a *money* problem. Of the 15 cases that still reach a human, 5 are genuinely undecidable (two settlements sharing one bank reference — no model can fix missing information) and 10 are real cash differences that a human *should* see. Runs end to end with no API key and no network.

**stacksense** — Hybrid retrieval, because vector search alone misses exact identifiers and keyword search alone misses intent. RRF fuses both rankings, then the dependency graph widens context so the LLM sees not just the relevant file but what it imports and what imports it.

**AlphaForge** — PPO training takes 30–90s, so it runs as a Celery job against Redis while the API returns immediately and the React dashboard polls. Risk is measured with Sharpe, Sortino and max drawdown, not raw returns.

**zentinel** — Llama 3.3 70B plans and synthesises; Llama 3.1 8B specialists execute with tools (web search, code execution, file ops) in a bounded loop. Live execution traces stream over WebSockets.

</details>

---

## GitHub

<div align="center">

<!-- github-readme-stats' public instance is chronically rate-limited (503s), so
     these use github-profile-summary-cards, which responds reliably. -->
<img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Kruthik481&theme=github_dark" alt="Profile summary" />

<br/>

<img height="200" src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Kruthik481&theme=github_dark" alt="Stats" />
<img height="200" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=Kruthik481&theme=github_dark" alt="Languages by repo" />

<br/>

<img height="200" src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Kruthik481&theme=github_dark" alt="Most committed languages" />
<img height="200" src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=Kruthik481&theme=github_dark&utcOffset=5.5" alt="Productive time" />

<br/><br/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Kruthik481&hide_border=true&background=0D1117&stroke=3D7EFF&ring=3D7EFF&fire=3D7EFF&currStreakLabel=3D7EFF&sideNums=C9D1D9&sideLabels=C9D1D9&dates=8B949E" alt="Streak" />

<br/><br/>

<img src="https://raw.githubusercontent.com/Kruthik481/Kruthik481/refs/heads/output/snake.svg" alt="Contribution snake" />

</div>

---

## Currently

- Extending the reconciliation agent's review loop so every human-confirmed exception is promoted into a reusable rule
- Getting AlphaForge's backend hosted so the live demo runs the full stack, not just the frontend
- Reading about retrieval evaluation — measuring recall@k properly instead of eyeballing answers

---

<div align="center">

### Let's talk

Open to **AI Engineer**, **Full-Stack Engineer**, and **Backend Engineer** roles.

[![LinkedIn](https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/REPLACE-WITH-YOUR-LINKEDIN)
[![Gmail](https://img.shields.io/badge/kruthikn05@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kruthikn05@gmail.com)

</div>
