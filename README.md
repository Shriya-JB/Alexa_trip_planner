# Trip Orchestrator — Alexa+ Agent Skill (Hackathon Project)

An Alexa+ Agent Skill that orchestrates your trip planning end-to-end — turning a vague goal into flights, stays, and a day-by-day itinerary through natural conversation.

## What it does

Instead of manually searching flights, hotels, and building an itinerary separately, this project exposes a single conversational tool — `plan_trip` — that an AI agent like Alexa+ can call. Behind the scenes, it automatically:

1. Searches real flight offers via the Duffel API
2. Searches hotel options for the destination
3. Builds a day-by-day itinerary combining the best flight and hotel

All of this happens through one natural request, like *"Plan me a 4-day trip to New York."*

## How it's built

- **MCP (Model Context Protocol) server** written in Python, exposing tools an AI agent can call
- **Duffel API** (test mode) for real flight search data
- Mocked hotel data (no reliable free hotel API exists, so realistic sample data is used instead)
- A lightweight **Flask web app** simulating the Alexa+ conversation experience as a chat interface, for demo purposes

## Tools exposed by the MCP server

- `search_flights` — real flight search via Duffel
- `search_hotels` — mocked hotel search
- `build_itinerary` — generates a day-by-day plan
- `plan_trip` — the orchestrator: chains all three together into one complete trip plan

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Why this approach

Full Alexa+ device publishing requires developer account approval and skill certification, which wasn't feasible within the hackathon timeline. This project instead demonstrates the full working orchestration logic via a real MCP server, with a simulated conversational interface standing in for the Alexa+ voice experience.
