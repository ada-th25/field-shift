# AI usage

This project was built with generative AI as a development
assistant throughout the hackathon. This file is the honest account of
where it was used, for judging and for anyone reading the repo. 

### Declaration of Generative AI Tools

Generative AI models were used as developer tools during software implementation. This usage was restricted to:

- Code Generation & Modularisation: Drafting code, modularising scripts, and creating visualisation tools.
- Debugging & API Integration: Troubleshooting execution errors, optimisation, and assisting with using/accessing datasets with APIs.
- Implementation Brainstorming: Exploring algorithms and workflow design possibilities.

Generated codes were manually reviewed, modified, and integrated by the authors.

## Tools
- Claude Code, Sonnet 5 (Anthropic)

## Where it helped
- **Crop dataset** (`data/crops.json`) — Claude cross-checked FAO-56, GRDC and USDA NASS figures and flagged where published numbers disagreed across studies. Those caveats are recorded in the dataset's own `source` fields.
- **Documentation** (`docs/`) — drafted from the working code and checked
against it, not written speculatively ahead of the implementation.
- **Tests** (`backend/tests/`) — regression tests written alongside each
feature as it was built.

## What stayed human
Every substantive decision (which crops to add, which risks to surface,
how a rotation should be scored, what the demo should teach a judge etc.) was
made by the team. Claude drafted and implemented; it did not choose the
project's scope, sources, or claims.