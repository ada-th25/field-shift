# AI usage

This project was built with generative AI as a development assistant
throughout the hackathon. This file is the honest account of where it
was used, by each team member, for judging and for anyone reading the
repo.

## Declaration of Generative AI Tools

Generative AI models were used as developer tools during software
implementation, across both the backend/algorithm and the frontend/game.
This usage was restricted to:

- Code Generation & Modularisation: Drafting code, modularising scripts,
  and creating visualisation tools.
- Debugging & API Integration: Troubleshooting execution errors,
  optimisation, and assisting with using/accessing datasets with APIs.
- Implementation Brainstorming: Exploring algorithms and workflow design
  possibilities.
- Frontend-backend integration: Connecting the game's interface with the
  backend functionality and crop recommendation system.

Generated code was manually reviewed, modified, and integrated by the
authors.

## Tsuyu — Backend and algorithm

**AI tools used:** Claude Code, Sonnet 5 (Anthropic)

### Where it helped
- **Crop dataset** (`data/crops.json`) — Claude cross-checked FAO-56,
  GRDC and USDA NASS figures and flagged where published numbers
  disagreed across studies. Those caveats are recorded in the dataset's
  own `source` fields.
- **Documentation** (`docs/`) — drafted from the working code and
  checked against it, not written speculatively ahead of the
  implementation.
- **Tests** (`backend/tests/`) — regression tests written alongside each
  feature as it was built.

### What stayed human
Every substantive decision (which crops to add, which risks to surface,
how a rotation should be scored, what the demo should teach a judge etc.)
was made by the team. Claude drafted and implemented; it did not choose
the project's scope, sources, or claims.

## Humayra — Game development and integration

**AI tools used:** ChatGPT (OpenAI) and Claude (Anthropic)

**Claude:**
- Assisted with the initial creation and development of the Harvest
  Heroes application.
- Generated the game's code and functionality based on prompts, ideas,
  and instructions provided by Humayra.
- Helped translate the proposed game concept into an interactive
  application.

**ChatGPT:**
- Assisted with integrating the existing backend into the frontend
  application.
- Helped connect the game's interface with the backend functionality and
  crop recommendation system.
- Provided implementation guidance and coding assistance during the
  integration process.

### What stayed human
Humayra provided the prompts and creative direction for the AI-assisted
game development. AI generated the game's implementation based on those
instructions.

## Original artwork — Airan

The following visual assets were manually drawn by our team member
**Airan**, using Procreate, and were not AI-generated:

- Crop illustrations used throughout the application.
- Monster illustrations featured in the Farming Journal.

## Transparency statement

We acknowledge the use of generative AI in building Harvest Heroes. AI
was used as a software development tool, while the project's creative
direction, original illustrations, and team contributions were provided
by human team members. This declaration documents the AI tools and
contributions identified by the team.
