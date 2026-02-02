# AI-Powered DevOps Platform - Use Cases

## Overview
This document contains all use cases for the AI-Powered DevOps Platform. Each use case is numbered for easy reference and tracking.

---

## Category 1: Pipeline Generation

### UC-1.1: Generate Full GitLab Pipeline
**Description:** Generate a complete 8-stage GitLab CI/CD pipeline for a project.
**Input:** Technology type (java/python/node/golang/php/dotnet/rust)
**Output:** Complete `.gitlab-ci.yml` with all 8 stages (compile, build, test, sast, quality, security, push, notify)
**Example Prompt:** "Generate a full GitLab pipeline for my Java Spring Boot application"

### UC-1.2: Generate Custom Steps Pipeline
**Description:** Generate a GitLab pipeline with user-defined custom stages only.
**Input:** Technology type + List of desired stages
**Output:** `.gitlab-ci.yml` with only specified stages
**Example Prompt:** "Generate a pipeline with only build, nexus image push, and sonarqube stages"

### UC-1.3: Generate Minimal Pipeline
**Description:** Generate a minimal pipeline with only essential stages.
**Input:** Technology type
**Output:** `.gitlab-ci.yml` with compile, build, push stages only
**Example Prompt:** "Generate a minimal pipeline for quick deployments"

### UC-1.4: Generate Pipeline for Specific Branch Strategy
**Description:** Generate pipeline with branch-specific configurations.
**Input:** Technology type + Branch strategy (GitFlow/Trunk-based/Feature branches)
**Output:** `.gitlab-ci.yml` with branch rules and conditions
**Example Prompt:** "Generate a pipeline that only runs security scans on main branch"

### UC-1.5: Generate Multi-Module Pipeline
**Description:** Generate pipeline for multi-module/monorepo projects.
**Input:** Technology type + Module list
**Output:** `.gitlab-ci.yml` with parallel jobs for each module
**Example Prompt:** "Generate a pipeline for my monorepo with 3 microservices"

### UC-1.6: Generate Pipeline with Custom Variables
**Description:** Generate pipeline with user-defined CI/CD variables.
**Input:** Technology type + Variable definitions
**Output:** `.gitlab-ci.yml` with custom variables section
**Example Prompt:** "Generate a pipeline with custom DEPLOY_ENV and APP_VERSION variables"

### UC-1.7: Generate Pipeline from Existing Template
**Description:** Generate pipeline based on a template from the catalog.
**Input:** Template name/ID
**Output:** `.gitlab-ci.yml` based on selected template
**Example Prompt:** "Generate a pipeline using the spring-boot-microservice template"

### UC-1.8: Generate Pipeline with Conditional Stages
**Description:** Generate pipeline with stages that run based on conditions.
**Input:** Technology type + Conditions (file changes, variables, manual triggers)
**Output:** `.gitlab-ci.yml` with rules and conditions
**Example Prompt:** "Generate a pipeline where security scan only runs if pom.xml changes"

### UC-1.9: Generate Pipeline with Parallel Jobs
**Description:** Generate pipeline with parallel execution for faster builds.
**Input:** Technology type + Parallelization config
**Output:** `.gitlab-ci.yml` with parallel job definitions
**Example Prompt:** "Generate a pipeline with parallel test execution across 4 runners"

### UC-1.10: Generate Pipeline with Matrix Builds
**Description:** Generate pipeline for testing across multiple configurations.
**Input:** Technology type + Matrix variables (versions, environments)
**Output:** `.gitlab-ci.yml` with matrix job configurations
**Example Prompt:** "Generate a pipeline that tests on Java 11, 17, and 21"

---

## Category 2: Dockerfile Generation

### UC-2.1: Generate Dockerfile from Repository
**Description:** Analyze repository and generate appropriate Dockerfile.
**Input:** GitLab repository path/URL
**Output:** Multi-stage Dockerfile using Nexus registry images
**Example Prompt:** "This is my GitLab repo path: group/project, generate the Dockerfile"

### UC-2.2: Generate Multi-Stage Dockerfile
**Description:** Generate optimized multi-stage Dockerfile.
**Input:** Technology type + Base image preferences
**Output:** Multi-stage Dockerfile with build and runtime stages
**Example Prompt:** "Generate a multi-stage Dockerfile for my Node.js app"

### UC-2.3: Generate Dockerfile with Security Best Practices
**Description:** Generate Dockerfile following security guidelines.
**Input:** Technology type
**Output:** Dockerfile with non-root user, minimal base image, no secrets
**Example Prompt:** "Generate a secure Dockerfile for production deployment"

### UC-2.4: Generate Dockerfile for Specific Runtime
**Description:** Generate Dockerfile for specific runtime/framework.
**Input:** Runtime details (Tomcat, Nginx, etc.)
**Output:** Dockerfile configured for specified runtime
**Example Prompt:** "Generate a Dockerfile for deploying WAR to Tomcat"

### UC-2.5: Generate Dockerfile with Health Checks
**Description:** Generate Dockerfile with HEALTHCHECK instruction.
**Input:** Technology type + Health endpoint
**Output:** Dockerfile with health check configuration
**Example Prompt:** "Generate a Dockerfile with health check on /actuator/health"

### UC-2.6: Optimize Existing Dockerfile
**Description:** Analyze and optimize an existing Dockerfile.
**Input:** Existing Dockerfile content
**Output:** Optimized Dockerfile with recommendations
**Example Prompt:** "Optimize this Dockerfile for smaller image size"

---

## Category 3: Repository Analysis & File Generation

### UC-3.1: Generate GitLab CI from Repository Path
**Description:** Analyze repository and generate appropriate CI/CD files.
**Input:** GitLab repository path
**Output:** `.gitlab-ci.yml` + Dockerfile
**Example Prompt:** "This is my GitLab repo path: mygroup/myproject, generate the gitlab file and dockerfile for it"

### UC-3.2: Detect Technology Stack
**Description:** Analyze repository to detect technology stack.
**Input:** GitLab repository path
**Output:** Technology detection report
**Example Prompt:** "What technology stack is used in this repository?"

### UC-3.3: Generate All DevOps Files
**Description:** Generate complete DevOps setup for a repository.
**Input:** GitLab repository path
**Output:** `.gitlab-ci.yml`, Dockerfile, docker-compose.yml, sonar-project.properties
**Example Prompt:** "Generate all DevOps files for my repository"

### UC-3.4: Analyze Repository Structure
**Description:** Analyze and report repository structure.
**Input:** GitLab repository path
**Output:** Structure analysis with recommendations
**Example Prompt:** "Analyze the structure of my repository and suggest improvements"

### UC-3.5: Generate Configuration Files
**Description:** Generate tool-specific configuration files.
**Input:** Repository path + Tool name
**Output:** Configuration file (sonar-project.properties, trivy.yaml, etc.)
**Example Prompt:** "Generate SonarQube configuration for my project"

---

## Category 4: Pipeline Sharing & Integration

### UC-4.1: Share Pipeline with All Tools
**Description:** Share generated pipeline configuration with all integrated tools.
**Input:** Generated `.gitlab-ci.yml`
**Output:** Confirmation of sharing with GitLab, SonarQube, Trivy, Nexus
**Example Prompt:** "Share this GitLab pipeline with all tools you generated"

### UC-4.2: Commit Pipeline to Repository
**Description:** Commit generated files directly to GitLab repository.
**Input:** Generated files + Repository path + Branch
**Output:** Commit created in GitLab
**Example Prompt:** "Commit this pipeline to my repository on feature/cicd branch"

### UC-4.3: Create Merge Request with Pipeline
**Description:** Create MR with generated pipeline files.
**Input:** Generated files + Repository path + Target branch
**Output:** Merge request created
**Example Prompt:** "Create a merge request with this pipeline targeting main branch"

### UC-4.4: Trigger Pipeline Execution
**Description:** Trigger pipeline execution after committing.
**Input:** Repository path + Branch
**Output:** Pipeline triggered, job URL returned
**Example Prompt:** "Trigger the pipeline on develop branch"

### UC-4.5: Share Pipeline Template to Catalog
**Description:** Save pipeline as reusable template in catalog.
**Input:** Pipeline content + Template name + Description
**Output:** Template saved to ChromaDB catalog
**Example Prompt:** "Save this pipeline as a template named 'java-microservice-full'"

---

## Category 5: Connectivity Testing

### UC-5.1: Check Connectivity with All Tools
**Description:** Test connectivity to all integrated platform tools.
**Input:** None (tests all)
**Output:** Connectivity status report for all tools
**Example Prompt:** "Check the connectivity with all tools"

### UC-5.2: Check Connectivity for Specific Tools
**Description:** Test connectivity to selected tools only.
**Input:** List of tools to test
**Output:** Connectivity status for specified tools
**Example Prompt:** "Check the connectivity for GitLab and SonarQube only"

### UC-5.3: Check GitLab Connectivity
**Description:** Test GitLab server and API connectivity.
**Input:** None
**Output:** GitLab connection status, API version, user info
**Example Prompt:** "Test GitLab connection"

### UC-5.4: Check SonarQube Connectivity
**Description:** Test SonarQube server connectivity.
**Input:** None
**Output:** SonarQube status, version, health
**Example Prompt:** "Test SonarQube connection"

### UC-5.5: Check Nexus Connectivity
**Description:** Test Nexus repository and Docker registry connectivity.
**Input:** None
**Output:** Nexus status, available repositories
**Example Prompt:** "Test Nexus connection"

### UC-5.6: Check Trivy Connectivity
**Description:** Test Trivy scanner server connectivity.
**Input:** None
**Output:** Trivy server status, version
**Example Prompt:** "Test Trivy scanner connection"

### UC-5.7: Check Ollama/LLM Connectivity
**Description:** Test Ollama LLM service connectivity.
**Input:** None
**Output:** Ollama status, available models
**Example Prompt:** "Test Ollama connection"

### UC-5.8: Check ChromaDB Connectivity
**Description:** Test ChromaDB vector database connectivity.
**Input:** None
**Output:** ChromaDB status, collection count
**Example Prompt:** "Test ChromaDB connection"

### UC-5.9: Check All Database Connections
**Description:** Test all database connections (PostgreSQL, Redis, ChromaDB).
**Input:** None
**Output:** Database connectivity report
**Example Prompt:** "Test all database connections"

### UC-5.10: Health Check Dashboard
**Description:** Display comprehensive health status of all services.
**Input:** None
**Output:** Dashboard view of all service health
**Example Prompt:** "Show platform health dashboard"

---

## Category 6: Nexus Registry Operations

### UC-6.1: List Available Docker Images
**Description:** List all Docker images available in Nexus registry.
**Input:** Optional filter/search query
**Output:** List of images with tags
**Example Prompt:** "List all Docker images in Nexus"

### UC-6.2: Search Docker Images
**Description:** Search for specific Docker images in Nexus.
**Input:** Search query (image name, tag)
**Output:** Matching images list
**Example Prompt:** "Search for Maven images in Nexus"

### UC-6.3: Get Image Details
**Description:** Get detailed information about a Docker image.
**Input:** Image name and tag
**Output:** Image details (size, layers, vulnerabilities)
**Example Prompt:** "Show details of eclipse-temurin:17 image"

### UC-6.4: Verify Image Availability
**Description:** Verify if required images exist in Nexus before pipeline generation.
**Input:** List of required images
**Output:** Availability status for each image
**Example Prompt:** "Verify if maven:3.9 and eclipse-temurin:17 are available"

### UC-6.5: Recommend Images for Technology
**Description:** Recommend appropriate Nexus images for a technology stack.
**Input:** Technology type
**Output:** Recommended images with justification
**Example Prompt:** "What images should I use for a Java 17 project?"

---

## Category 7: SonarQube Operations

### UC-7.1: Get Project Quality Status
**Description:** Get quality gate status for a project.
**Input:** Project key
**Output:** Quality gate status, metrics
**Example Prompt:** "What is the quality gate status for project X?"

### UC-7.2: List Code Issues
**Description:** List code issues found by SonarQube.
**Input:** Project key + Optional severity filter
**Output:** List of issues with details
**Example Prompt:** "Show critical issues in my project"

### UC-7.3: Get Code Coverage
**Description:** Get code coverage metrics for a project.
**Input:** Project key
**Output:** Coverage percentage, uncovered lines
**Example Prompt:** "What is the code coverage for my project?"

### UC-7.4: Compare Quality Between Branches
**Description:** Compare code quality between two branches.
**Input:** Project key + Branch names
**Output:** Comparison report
**Example Prompt:** "Compare quality between main and develop branches"

### UC-7.5: Get Technical Debt
**Description:** Get technical debt estimate for a project.
**Input:** Project key
**Output:** Technical debt in time/effort
**Example Prompt:** "How much technical debt does my project have?"

---

## Category 8: Trivy Security Operations

### UC-8.1: Scan Docker Image
**Description:** Scan a Docker image for vulnerabilities.
**Input:** Image name and tag
**Output:** Vulnerability report
**Example Prompt:** "Scan my-app:latest for vulnerabilities"

### UC-8.2: Scan Repository
**Description:** Scan a Git repository for vulnerabilities.
**Input:** Repository path
**Output:** Vulnerability report for dependencies
**Example Prompt:** "Scan my repository for security issues"

### UC-8.3: Generate SBOM
**Description:** Generate Software Bill of Materials for an image.
**Input:** Image name and tag
**Output:** SBOM in CycloneDX/SPDX format
**Example Prompt:** "Generate SBOM for my application image"

### UC-8.4: Get Vulnerability Summary
**Description:** Get summary of vulnerabilities by severity.
**Input:** Image or repository
**Output:** Summary count by severity level
**Example Prompt:** "Give me a vulnerability summary for my image"

### UC-8.5: Check for Critical Vulnerabilities
**Description:** Quick check for critical/high vulnerabilities.
**Input:** Image or repository
**Output:** Boolean result with critical issue list
**Example Prompt:** "Are there any critical vulnerabilities in my image?"

---

## Category 9: GitLab Operations

### UC-9.1: List Projects
**Description:** List all accessible GitLab projects.
**Input:** Optional group filter
**Output:** List of projects with details
**Example Prompt:** "List all my GitLab projects"

### UC-9.2: Get Pipeline Status
**Description:** Get status of recent pipelines.
**Input:** Project path
**Output:** Pipeline status, jobs, duration
**Example Prompt:** "What is the status of my latest pipeline?"

### UC-9.3: Get Failed Job Logs
**Description:** Retrieve logs from failed pipeline jobs.
**Input:** Project path + Pipeline ID
**Output:** Job logs with error details
**Example Prompt:** "Show me the logs of the failed job"

### UC-9.4: Retry Failed Pipeline
**Description:** Retry a failed pipeline.
**Input:** Project path + Pipeline ID
**Output:** New pipeline triggered
**Example Prompt:** "Retry the failed pipeline"

### UC-9.5: Cancel Running Pipeline
**Description:** Cancel a running pipeline.
**Input:** Project path + Pipeline ID
**Output:** Pipeline cancelled confirmation
**Example Prompt:** "Cancel the running pipeline"

### UC-9.6: List Branches
**Description:** List all branches in a project.
**Input:** Project path
**Output:** List of branches with last commit
**Example Prompt:** "List all branches in my project"

### UC-9.7: Get Merge Request Status
**Description:** Get status of merge requests.
**Input:** Project path + Optional MR ID
**Output:** MR status, approvals, pipeline status
**Example Prompt:** "What is the status of my open merge requests?"

---

## Category 10: Pipeline Troubleshooting

### UC-10.1: Fix Pipeline Errors
**Description:** Analyze and fix pipeline errors.
**Input:** Error message or failed pipeline ID
**Output:** Fixed pipeline configuration
**Example Prompt:** "Fix this pipeline error: image not found"

### UC-10.2: Fix Nexus Image Issues
**Description:** Fix issues related to missing Nexus images.
**Input:** Pipeline with image errors
**Output:** Corrected pipeline with valid Nexus images
**Example Prompt:** "The pipeline fails because maven:3.9 is not in Nexus"

### UC-10.3: Debug Pipeline Stage
**Description:** Add debugging to a specific pipeline stage.
**Input:** Pipeline + Stage name
**Output:** Pipeline with debug commands added
**Example Prompt:** "Add debugging to the build stage"

### UC-10.4: Analyze Pipeline Performance
**Description:** Analyze pipeline execution time and suggest optimizations.
**Input:** Project path
**Output:** Performance report with recommendations
**Example Prompt:** "Why is my pipeline taking so long?"

### UC-10.5: Fix SonarQube Stage Issues
**Description:** Fix issues in SonarQube analysis stage.
**Input:** Error details
**Output:** Corrected SonarQube configuration
**Example Prompt:** "SonarQube stage is failing with authentication error"

---

## Category 11: Template Management

### UC-11.1: List Available Templates
**Description:** List all pipeline templates in the catalog.
**Input:** Optional technology filter
**Output:** List of templates with descriptions
**Example Prompt:** "Show all available pipeline templates"

### UC-11.2: Get Template Details
**Description:** Get detailed information about a template.
**Input:** Template name/ID
**Output:** Template content, variables, usage examples
**Example Prompt:** "Show details of the spring-boot template"

### UC-11.3: Create Custom Template
**Description:** Create a new pipeline template.
**Input:** Pipeline content + Metadata
**Output:** Template saved to catalog
**Example Prompt:** "Save this pipeline as a custom template"

### UC-11.4: Update Template
**Description:** Update an existing template.
**Input:** Template ID + New content
**Output:** Template updated
**Example Prompt:** "Update the spring-boot template with new stages"

### UC-11.5: Delete Template
**Description:** Delete a template from catalog.
**Input:** Template ID
**Output:** Template deleted confirmation
**Example Prompt:** "Delete the deprecated template"

### UC-11.6: Export Template
**Description:** Export template for sharing.
**Input:** Template ID
**Output:** Template file (YAML/JSON)
**Example Prompt:** "Export the spring-boot template"

### UC-11.7: Import Template
**Description:** Import template from file.
**Input:** Template file
**Output:** Template imported to catalog
**Example Prompt:** "Import this template file"

---

## Category 12: Monitoring & Observability

### UC-12.1: View Pipeline Metrics
**Description:** View metrics for pipeline executions.
**Input:** Project path + Time range
**Output:** Metrics dashboard (success rate, duration, etc.)
**Example Prompt:** "Show pipeline metrics for last 30 days"

### UC-12.2: View Platform Logs
**Description:** View logs from platform services.
**Input:** Service name + Time range
**Output:** Log entries
**Example Prompt:** "Show logs from the modernization API"

### UC-12.3: View Distributed Traces
**Description:** View request traces across services.
**Input:** Trace ID or request details
**Output:** Trace visualization
**Example Prompt:** "Show trace for my last pipeline generation request"

### UC-12.4: Get Alert Status
**Description:** Get current alert status from monitoring.
**Input:** None
**Output:** Active alerts list
**Example Prompt:** "Are there any active alerts?"

### UC-12.5: View Resource Usage
**Description:** View resource usage of platform services.
**Input:** Optional service filter
**Output:** CPU, memory, disk usage
**Example Prompt:** "Show resource usage for all services"

---

## Category 13: Configuration Management

### UC-13.1: Update Tool Configuration
**Description:** Update configuration for integrated tools.
**Input:** Tool name + Configuration values
**Output:** Configuration updated
**Example Prompt:** "Update the GitLab URL configuration"

### UC-13.2: Add New Tool Integration
**Description:** Add a new tool to the platform.
**Input:** Tool details (URL, credentials, type)
**Output:** Tool added and tested
**Example Prompt:** "Add a new SonarQube server"

### UC-13.3: Remove Tool Integration
**Description:** Remove an integrated tool.
**Input:** Tool name/ID
**Output:** Tool removed
**Example Prompt:** "Remove the old SonarQube server"

### UC-13.4: Export Configuration
**Description:** Export platform configuration.
**Input:** None
**Output:** Configuration file
**Example Prompt:** "Export platform configuration"

### UC-13.5: Import Configuration
**Description:** Import platform configuration.
**Input:** Configuration file
**Output:** Configuration applied
**Example Prompt:** "Import this configuration file"

---

## Category 14: Golden Rules & Compliance

### UC-14.1: Validate Pipeline Against Rules
**Description:** Validate pipeline against golden rules.
**Input:** Pipeline content
**Output:** Validation report
**Example Prompt:** "Does this pipeline follow the golden rules?"

### UC-14.2: Check Registry Compliance
**Description:** Check if pipeline uses only approved registries.
**Input:** Pipeline content
**Output:** Compliance status
**Example Prompt:** "Does this pipeline use only Nexus registry?"

### UC-14.3: Generate Compliant Pipeline
**Description:** Generate pipeline that follows all compliance rules.
**Input:** Technology type
**Output:** Fully compliant pipeline
**Example Prompt:** "Generate a compliant pipeline for my Java project"

### UC-14.4: List Golden Rules
**Description:** List all active golden rules.
**Input:** None
**Output:** List of rules with descriptions
**Example Prompt:** "What are the golden rules for pipelines?"

### UC-14.5: Add Custom Rule
**Description:** Add a custom compliance rule.
**Input:** Rule definition
**Output:** Rule added
**Example Prompt:** "Add a rule that requires security scanning"

---

## Category 15: Batch Operations

### UC-15.1: Generate Pipelines for Multiple Projects
**Description:** Generate pipelines for multiple projects at once.
**Input:** List of project paths
**Output:** Pipelines generated for all projects
**Example Prompt:** "Generate pipelines for all projects in my group"

### UC-15.2: Update All Pipelines
**Description:** Update pipelines across multiple projects.
**Input:** Update specification + Project filter
**Output:** All matching pipelines updated
**Example Prompt:** "Update all pipelines to use the new Trivy version"

### UC-15.3: Scan All Projects
**Description:** Run security scan on all projects.
**Input:** Optional project filter
**Output:** Consolidated scan report
**Example Prompt:** "Scan all my projects for vulnerabilities"

### UC-15.4: Generate Report for All Projects
**Description:** Generate consolidated report for multiple projects.
**Input:** Report type + Project list
**Output:** Consolidated report
**Example Prompt:** "Generate quality report for all my microservices"

---

## Category 16: Help & Documentation

### UC-16.1: Get Help for Command
**Description:** Get help for a specific command or feature.
**Input:** Command/feature name
**Output:** Help documentation
**Example Prompt:** "How do I generate a custom pipeline?"

### UC-16.2: List Available Commands
**Description:** List all available commands.
**Input:** None
**Output:** Command list with descriptions
**Example Prompt:** "What commands are available?"

### UC-16.3: Show Examples
**Description:** Show usage examples for a feature.
**Input:** Feature name
**Output:** Example prompts and outputs
**Example Prompt:** "Show examples of pipeline generation"

### UC-16.4: Get Platform Status
**Description:** Get overall platform status and version.
**Input:** None
**Output:** Platform info, version, status
**Example Prompt:** "What version of the platform is this?"

---

## Quick Reference - Common Use Cases

| UC ID | Use Case | Example Prompt |
|-------|----------|----------------|
| UC-1.1 | Full pipeline | "Generate full pipeline for Java" |
| UC-1.2 | Custom stages | "Generate pipeline with build and push only" |
| UC-3.1 | From repo | "Generate CI/CD for mygroup/myproject" |
| UC-4.1 | Share pipeline | "Share pipeline with all tools" |
| UC-5.1 | Test all | "Check connectivity with all tools" |
| UC-5.2 | Test specific | "Check GitLab and SonarQube only" |
| UC-6.1 | List images | "List Nexus images" |
| UC-10.1 | Fix errors | "Fix this pipeline error" |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-02-01 | Initial use case documentation |

---

*Total Use Cases: 85*
*Categories: 16*
