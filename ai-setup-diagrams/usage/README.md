# AI-Powered DevOps Platform - Architecture Diagrams

## Overview
This folder contains 47 SVG architecture diagrams documenting the AI-Powered DevOps Platform.

## Diagram Categories

### 1. High-Level Architecture (3 diagrams)
| File | Description |
|------|-------------|
| `platform-master-architecture.svg` | Complete platform overview with all components |
| `ai-devops-platform-layers.svg` | Layered architecture view (UI, API, Services, Data) |
| `system-context-diagram.svg` | External actors and system boundaries |

### 2. Infrastructure & Platform (7 diagrams)
| File | Description |
|------|-------------|
| `docker-compose-services.svg` | All 22 Docker Compose services |
| `network-topology.svg` | Network connections between services |
| `data-storage-architecture.svg` | Databases, caches, and storage systems |
| `monitoring-observability-stack.svg` | Prometheus, Grafana, Loki, Jaeger stack |
| `docker-volumes-storage.svg` | All 24 named volumes and bind mounts |
| `docker-network-topology.svg` | platform-net bridge network with IPs |
| `dns-port-resolution.svg` | Complete DNS names and port mappings |

### 3. Data Flows (5 diagrams)
| File | Description |
|------|-------------|
| `rag-pipeline-flow.svg` | RAG retrieval and generation flow |
| `pipeline-generation-flow.svg` | CI/CD pipeline generation process |
| `user-request-flow.svg` | End-to-end user request handling |
| `ci-cd-data-flow.svg` | Data flow through CI/CD stages |
| `feedback-learning-loop.svg` | Continuous improvement cycle |

### 4. Backend Services (4 diagrams)
| File | Description |
|------|-------------|
| `devops-tools-backend-api.svg` | DevOps Tools API endpoints (:8003) |
| `modernization-api-architecture.svg` | Modernization API structure (:8002) |
| `rag-generator-api.svg` | RAG Generator API (:8080) |
| `api-integration-patterns.svg` | API communication patterns |

### 5. AI/LLM & RAG (6 diagrams)
| File | Description |
|------|-------------|
| `ollama-llm-architecture.svg` | Ollama LLM service architecture |
| `chromadb-collections-detail.svg` | ChromaDB vector collections |
| `embedding-retrieval-flow.svg` | Embedding and retrieval process |
| `model-configuration.svg` | LLM model configurations |
| `chromadb-data-sources.svg` | Data sources feeding ChromaDB |
| `pipeline-tools-chromadb-integration.svg` | Tools and ChromaDB integration |

### 6. Tool Architecture (5 diagrams)
| File | Description |
|------|-------------|
| `openwebui-tools-overview.svg` | OpenWebUI tools summary |
| `pipeline-generator-tool.svg` | Pipeline generation tool details |
| `commit-deploy-tool.svg` | GitLab commit and deploy tool |
| `fix-pipeline-tool.svg` | Pipeline error fixing tool |
| `nexus-explorer-tool.svg` | Nexus registry explorer tool |

### 7. Integration Diagrams (5 diagrams)
| File | Description |
|------|-------------|
| `gitlab-integration-flow.svg` | GitLab API integration |
| `sonarqube-integration-flow.svg` | SonarQube quality integration |
| `trivy-integration-flow.svg` | Trivy security scanning integration |
| `splunk-integration-flow.svg` | Splunk HEC logging integration |
| `nexus-integration-flow.svg` | Nexus repository integration |

### 8. Security & Compliance (3 diagrams)
| File | Description |
|------|-------------|
| `security-scanning-flow.svg` | Security scanning pipeline |
| `authentication-authorization.svg` | Auth mechanisms |
| `secrets-management.svg` | Secrets and credentials handling |

### 9. Pipeline Execution (3 diagrams)
| File | Description |
|------|-------------|
| `gitlab-runner-execution.svg` | GitLab Runner execution flow |
| `8-stage-pipeline-detail.svg` | Detailed 8-stage pipeline |
| `pipeline-artifacts-flow.svg` | Artifact management flow |

### 10. Catalog & Templates (2 diagrams)
| File | Description |
|------|-------------|
| `template-catalog-structure.svg` | Template catalog organization |
| `golden-rules-architecture.svg` | Golden rules enforcement |

### 11. Connection Testing (1 diagram)
| File | Description |
|------|-------------|
| `connection-testing-matrix.svg` | Frontend to backend connectivity matrix |

### 12. Legacy/Early Diagrams (3 diagrams)
| File | Description |
|------|-------------|
| `devops-architecture.svg` | Early architecture draft |
| `cicd-generation-flow-v2.svg` | CI/CD generation flow v2 |
| `repo-detection-architecture.svg` | Repository detection system |

---

## Quick Reference

### Key URLs (External Access)
| Service | URL | Purpose |
|---------|-----|---------|
| Open WebUI | http://localhost:3000 | AI Chat Interface |
| GitLab | http://localhost:8929 | Source Code Management |
| Nexus Registry | http://localhost:5001 | Docker Registry |
| Nexus UI | http://localhost:8081 | Artifact Management |
| SonarQube | http://localhost:9002 | Code Quality |
| Grafana | http://localhost:3002 | Dashboards |
| Prometheus | http://localhost:9090 | Metrics |

### Key Internal DNS Names
| Service | DNS Name | Port |
|---------|----------|------|
| PostgreSQL | postgres | 5432 |
| Redis | redis | 6379 |
| Ollama | ollama | 11434 |
| ChromaDB | chromadb | 8000 |
| GitLab | gitlab-server | 80 |

---

## Usage Tips

1. **View in Browser**: Open any SVG file directly in a web browser for best quality
2. **Embed in Docs**: SVGs can be embedded in Confluence, Notion, or Markdown files
3. **Edit**: Use tools like Inkscape, Figma, or any SVG editor to modify
4. **Print**: SVGs scale to any size without losing quality

## Diagram Style Guide
- Background: `#0a0a0f` (dark)
- Header gradient: `#1a1a2e` to `#16213e`
- Success/Connected: `#00b894` (green)
- Warning/Optional: `#ffd93d` (yellow)
- Error/Critical: `#d63031` (red)
- Future/Planned: `#6c5ce7` (purple)
