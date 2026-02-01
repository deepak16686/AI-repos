# Copilot Instructions for AI Repos

This repository is a collection of AI helper projects and experiments. The structure and conventions are minimal, but follow these guidelines for effective AI agent contributions:

## Big Picture Architecture
- The repo is organized as a flat collection of projects and experiments. Each project is self-contained.
- There is no monolithic application or shared framework; treat each folder as an independent unit unless otherwise documented.
- Cross-project dependencies are rare. If present, they will be documented in the respective project's README or code comments.

## Developer Workflows
- There is no global build or test system. Each project may have its own build/test instructions in its README or source files.
- Always check for a README.md in the root or project folders for specific setup, build, or run instructions.
- Common commands (if present) are documented per project. Do not assume npm, Python, or other tool usage unless explicitly stated.

## Project-Specific Conventions
- Naming: Projects and files use descriptive names related to their AI functionality or experiment purpose.
- Documentation: Key patterns, data flows, and integration points are described in README.md files or inline comments.
- Experiments may use unconventional structures; follow the documented approach in each folder.

## Integration Points & Dependencies
- External dependencies (libraries, APIs) are declared per project, typically in requirements.txt, package.json, or similar files.
- Integration with external services (APIs, models) is project-specific. Refer to the relevant README or code for details.

## Examples & Patterns
- For new projects, follow the structure and documentation style of existing folders.
- If adding to an existing project, match its conventions and update its README.md as needed.
- Example: If a project uses a custom script for training, document the command and expected outputs in its README.md.

## Key Files
- [README.md](../../README.md): High-level overview of the repository.
- Project-level README.md files: Essential for understanding individual projects.

## How to Contribute as an AI Agent
- Before making changes, review the relevant README.md and source files for project-specific instructions.
- Document any new workflows, dependencies, or integration points you introduce.
- If unsure about conventions, mimic the style and structure of existing projects.

---

*Update this file as new conventions or workflows emerge. Ask for feedback if any section is unclear or incomplete.*
