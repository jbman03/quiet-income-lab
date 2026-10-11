# Run a Private AI Assistant on Your Own PC (No Subscription)
> How to get a local AI model, your own documents, and a daily brief on your phone for $0 a month.

You don't need a monthly AI subscription to get a useful assistant. A regular Windows PC with 16 GB of RAM can run a capable AI model locally, answer questions about your own documents, and push a short brief to your phone every morning. Nothing leaves your house unless you choose.

This is the setup I run at home. Here's the overview.

## The four free pieces

- **Ollama** runs the AI model on your PC. A 4-billion-parameter model like qwen3:4b is a good all-rounder and works without a graphics card.
- **AnythingLLM** gives you a chat window over your own files. Make one "workspace" per area of life (family, work, side business) so answers stay on topic.
- **ntfy** sends free push notifications to your phone. No account needed. Your private topic name works like a password.
- **A small script** gathers facts (weather, your to-do list), asks the local model to summarize them, and pushes the result to your phone. Windows Task Scheduler runs it every morning.

## What it's good at (and what it isn't)

Small local models are great at **summarizing facts you hand them**: "here's the weather and my list, what matters today?" They're bad at knowing things on their own, and they will confidently make things up if you let them.

Three habits fix most of that:

1. Give the model the facts in the prompt and say "use only the facts above".
2. Tell it what to do when information is missing: "if the list is empty, say so, never invent tasks."
3. Use AnythingLLM's **Query** mode for document questions, so answers come only from your files.

## What it costs to run

The software is free. The only cost is electricity while the PC is on. On a PC without a graphics card, a short morning brief takes about 20 to 60 seconds to generate, which is fine for something that runs once a day.

## Privacy checklist

- Keep everything local: Ollama and AnythingLLM Desktop don't need the cloud.
- Use a long random ntfy topic and never post it.
- Don't put passwords, card numbers or ID scans into any AI workspace.
- To reach it from your phone away from home, use Tailscale (free) instead of opening ports on your router.

<div class="cta">The full step-by-step guide, including the ready-to-run morning brief script, is here: <a href="https://jbman03gmail.gumroad.com/l/ziccnx">Your Own Private AI Assistant, Weekend Setup Guide</a>. Prefer to have it done for you? <a href="https://jbman03gmail.gumroad.com/l/jxapmn">Book a 90-minute setup session</a>.</div>
