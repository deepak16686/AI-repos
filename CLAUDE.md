# CLAUDE.md - AI-Repos Codebase Guide

## Project Overview

This is a **documentation and reference repository** for an enterprise-grade AI-Powered DevOps Platform. It contains architecture diagrams (SVG), use-case documentation, and AI-agent contribution guidelines. There is no application source code, build system, or test suite in this repository.

The documented platform automates CI/CD pipeline generation, Dockerfile creation, repository analysis, and DevOps tool integration using LLMs and RAG (Retrieval-Augmented Generation).

## Repository Structure

```
AI-repos/
├── CLAUDE.md                         # This file - AI assistant guide
├── README.md                         # Minimal project description
├── .claude/
│   └── settings.local.json           # Claude Code permission settings
├── .github/
│   └── copilot-instructions.md       # AI agent contribution guidelines
├── ai-setup-diagrams/                # 46 SVG architecture & flow diagrams
│   ├── platform-master-architecture.svg
│   ├── system-context-diagram.svg
│   ├── pipeline-generation-flow.svg
│   ├── rag-pipeline-flow.svg
│   ├── docker-compose-services.svg
│   ├── ... (46 files total)
│   └── user-request-flow.svg
└── ai-setup-usage/
    └── platform-usecases.md          # 85 use cases across 16 categories
```

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | High-level repository description |
| `.github/copilot-instructions.md` | Guidelines for AI agent contributions, naming conventions, architecture overview |
| `ai-setup-usage/platform-usecases.md` | 85 documented use cases in 16 categories (pipeline generation, Dockerfile generation, security scanning, etc.) |
| `.claude/settings.local.json` | Whitelisted Bash permissions for Claude Code (Docker, Git, curl, etc.) |

## Development Workflow

### No Build/Test/Lint System

This is a documentation-only repo. There are no:
- Build commands (`npm`, `make`, `gradle`, etc.)
- Test suites or test runners
- Linters or formatters
- CI/CD pipelines for this repo itself

### Git Workflow

- **Remote:** Proxied via `127.0.0.1:46500`
- **Branching:** Feature branches prefixed with `claude/` for AI-assisted work
- **Commits:** Signed with SSH key; co-authored by Claude when AI-assisted

### Adding Content

- **Diagrams:** Place SVG files in `ai-setup-diagrams/`. Use descriptive kebab-case names (e.g., `pipeline-generation-flow.svg`).
- **Documentation:** Place markdown files in `ai-setup-usage/`. Follow the use-case format in `platform-usecases.md` (numbered categories, structured fields: Description, Input, Output, Example Prompt).
- **New projects:** Each project should be self-contained in its own folder with its own README.

## Documented Platform Architecture

The diagrams and use cases describe an AI-powered DevOps platform with these components:

### Core Services
- **DevOps Tools Backend** - Python API that orchestrates all platform operations
- **Ollama** - Local LLM inference engine
- **Open WebUI** - Chat frontend for interacting with the platform
- **ChromaDB** - Vector database for RAG-based pipeline template retrieval

### Integrated DevOps Tools
| Tool | Purpose | Internal Hostname |
|------|---------|-------------------|
| GitLab | Source control & CI/CD | `gitlab-server` |
| SonarQube | Code quality analysis | `ai-sonarqube:9000` |
| Nexus | Artifact & Docker registry | `ai-nexus:8081` (registry on `:5001`) |
| Trivy | Container security scanning | `trivy-server:8080` |
| Prometheus | Metrics collection | `prometheus:9090` |
| Grafana | Metrics dashboards | `grafana:3000` |
| Loki | Log aggregation | `loki:3100` |
| Jaeger | Distributed tracing | `jaeger:16686` |
| Splunk | Enterprise logging | `splunk:8089` |
| Redis | Caching & sessions | `redis:6379` |
| PostgreSQL | Persistent storage | `ai-postgres:5432` |
| MinIO | S3-compatible object storage | `minio:9000` |
| Redmine | Issue/ticket tracking | `redmine:3000` |

### Key Platform Capabilities (Use Case Categories)
1. **Pipeline Generation** (UC-1) - AI-generated GitLab CI/CD pipelines (8-stage: compile, build, test, SAST, quality, security, push, notify)
2. **Dockerfile Generation** (UC-2) - Repository analysis and multi-stage Dockerfile creation
3. **Repository Analysis** (UC-3) - Technology detection and project structure analysis
4. **Pipeline Sharing** (UC-4) - Template catalog stored in ChromaDB
5. **Connectivity Testing** (UC-5) - Health checks across all platform services
6. **Nexus Operations** (UC-6) - Registry management and artifact operations
7. **SonarQube Operations** (UC-7) - Quality gate and analysis management
8. **Trivy Security** (UC-8) - Vulnerability scanning and reporting
9. **GitLab Operations** (UC-9) - Project, pipeline, and runner management
10. **Pipeline Troubleshooting** (UC-10) - Failed pipeline diagnosis and fixes
11. **Template Management** (UC-11) - CRUD operations on pipeline templates
12. **Monitoring** (UC-12) - Prometheus/Grafana metrics and alerting
13. **Configuration Management** (UC-13) - Platform-wide configuration
14. **Golden Rules & Compliance** (UC-14) - Enforced standards and best practices
15. **Batch Operations** (UC-15) - Multi-project pipeline operations
16. **Help & Documentation** (UC-16) - Platform self-documentation

## Conventions for AI Assistants

### General Rules
- Treat each folder as an independent unit unless documented otherwise
- Check for a README in each project folder before making changes
- Match the existing style and conventions of whatever you're modifying
- Use descriptive, kebab-case naming for files and folders
- Document any new workflows, dependencies, or integration points you introduce

### Diagram Conventions
- All architecture diagrams are SVG format in `ai-setup-diagrams/`
- Diagrams cover: architecture layers, data flows, integration patterns, network topology, tool-specific details
- When referencing diagrams, use the filename (e.g., `platform-master-architecture.svg`)

### Documentation Conventions
- Use cases follow a structured format: **Description**, **Input**, **Output**, **Example Prompt**
- Use cases are numbered hierarchically: `UC-{category}.{number}` (e.g., UC-1.3)
- Categories are numbered sequentially starting from 1

### Security Notes
- The `.claude/settings.local.json` contains hardcoded credentials (GitLab tokens, Nexus passwords) - these are for a local development environment only
- Never commit real production credentials to this repository
- No `.gitignore` exists - be careful not to add sensitive files
