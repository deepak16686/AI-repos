# Quick Reference Card

## Service Health Checks

```bash
# AI/LLM Services
curl http://localhost:11434/api/tags          # Ollama
curl http://localhost:8000/api/v1/heartbeat   # ChromaDB

# DevOps Tools
curl http://localhost:8929/api/v4/projects    # GitLab (needs token)
curl http://localhost:8081/service/rest/v1/status  # Nexus
curl http://localhost:9002/api/system/status  # SonarQube
curl http://localhost:8083/healthz            # Trivy

# Monitoring
curl http://localhost:9090/-/healthy          # Prometheus
curl http://localhost:3002/api/health         # Grafana
curl http://localhost:3100/ready              # Loki

# APIs
curl http://localhost:8002/api/v1/health      # Modernization API
curl http://localhost:8003/health             # DevOps Tools API
```

## Docker Commands

```bash
# Check all containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Network inspection
docker network inspect platform-net

# View logs
docker logs platform-gitlab -f --tail 100
docker logs platform-ollama -f --tail 100

# Test internal connectivity
docker exec platform-open-webui curl http://ollama:11434/api/tags
docker exec platform-open-webui curl http://chromadb:8000/api/v1/heartbeat
```

## Port Mapping Summary

| Host Port | Service | Internal Port |
|-----------|---------|---------------|
| 3000 | Open WebUI | 8080 |
| 5001 | Nexus Registry | 5001 |
| 5432 | PostgreSQL | 5432 |
| 6379 | Redis | 6379 |
| 8000 | ChromaDB | 8000 |
| 8002 | Modernization API | 8000 |
| 8003 | DevOps Tools API | 8003 |
| 8081 | Nexus UI | 8081 |
| 8083 | Trivy | 8080 |
| 8929 | GitLab | 80 |
| 9000 | MinIO API | 9000 |
| 9001 | MinIO Console | 9001 |
| 9002 | SonarQube | 9000 |
| 9090 | Prometheus | 9090 |
| 3002 | Grafana | 3000 |
| 3100 | Loki | 3100 |
| 11434 | Ollama | 11434 |
| 16686 | Jaeger | 16686 |

## Golden Rules

1. **Private Registry ONLY**: All Docker images from `localhost:5001`
2. **8-Stage Pipeline**: compile → build → test → sast → quality → security → push → notify
3. **Multi-Stage Builds**: Always use multi-stage Dockerfiles
4. **Security Defaults**: Non-root user, no hardcoded secrets, Trivy scan mandatory
