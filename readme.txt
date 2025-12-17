PharmaGen AI – Agentic Intelligence for Drug Repurposing

Demo Video:
(https://drive.google.com/file/d/1ayOzmOagxb6d8gOtbc9X3kbs6_tpHFqF/view
)

Sample PDF Output:
(https://drive.google.com/file/d/17FXpavjIGk6ungP044fst8bAxvU7mlmB/view
)

EY Techathon 6.0 Submission
Team Name: keshavpareek2022
Author: Keshav Pareek
Date: 09-11-2025

Overview

PharmaGen AI is an agentic AI-powered drug repurposing platform designed to reduce early-stage pharmaceutical research time from months to minutes. It autonomously evaluates scientific validity, clinical feasibility, patent freedom-to-operate, and commercial viability for repurposing existing drugs to new indications.

Unlike traditional chatbots, PharmaGen AI follows a Master–Worker multi-agent architecture, where specialized AI agents work in parallel to deliver a comprehensive Go / No-Go strategic report.

Problem Statement

The pharmaceutical industry faces a critical bottleneck in drug repurposing:

Data scattered across PubMed, ClinicalTrials.gov, USPTO, and market intelligence platforms (IQVIA)
Manual synthesis takes 2–3 months per molecule
High R&D cost spent on non-viable candidates

Target Users

Portfolio Strategy Managers
R&D Scientists
Business Development Leads

Industry

Pharmaceuticals & Life Sciences (B2B – Enterprise R&D)

Solution

PharmaGen AI provides a single unified interface where users input:

Drug Name + Target Disease

The system autonomously:

Gathers data from multiple sources

Analyzes biological mechanisms

Cross-checks clinical trials and patents

Evaluates market potential

Generates a downloadable PDF strategic report

Agentic Architecture

Master–Worker Model

Master Agent

Parses user intent
Orchestrates sub-agent execution
Aggregates final insights

Worker Agents

Agent Responsibility
Scientific Agent Validates biological & mechanistic plausibility
Clinical Agent Scans active & completed clinical trials
Patent Agent Evaluates IP landscape & freedom-to-operate
Market Agent Assesses commercial viability & demand

Agents run in parallel, drastically reducing turnaround time.

End-to-End Workflow

User Query
↓
Master Agent (Orchestrator)
↓
Parallel Worker Agents (Scientific | Clinical | Patent | Market)
↓
JSON Data Ingestion
↓
LLM-based Synthesis
↓
Streamlit Dashboard + PDF Report

Example Use Case

Scenario:

Can Metformin be repurposed for Neurological Disorders?

Without PharmaGen AI:

Manual search across 5+ platforms
Weeks of effort

With PharmaGen AI:

Single query
Automated data synthesis
Strategic report generated in < 60 seconds

Impact Metrics

Time Reduction: ~4 weeks → < 5 minutes
Coverage: 100% automated cross-referencing (Patents vs Clinical Trials)
Cost Savings: Significant reduction in R&D man-hours
Scalability: New data sources added by introducing a new agent only

Technology Stack

Frontend

Streamlit (Python)

Orchestration

LangChain
LangGraph

Intelligence

OpenAI GPT-4o

Tools & Integrations

DuckDuckGo Search (Web)
BioPython (PubMed)
FPDF (PDF Generation)
Mock IQVIA / EXIM Database APIs

Key Features

Live Clinical Trial Search
Agent-based Parallel Reasoning
Automated PDF Strategy Report
Mock Integration with Paid Pharma Databases
Modular & Extensible Architecture

Demo & Outputs

Demo Video:
https://drive.google.com/file/d/1ayOzmOagxb6d8gOtbc9X3kbs6_tpHFqF/view

Sample PDF Output:
https://drive.google.com/file/d/17FXpavjIGk6ungP044fst8bAxvU7mlmB/view

Scalability & Robustness

Agent-based modular design
Easy integration of new sources (e.g., FDA Orange Book)
API-simulation-first approach for stability
Enterprise-ready architecture

Final Outcome

PharmaGen AI transforms drug repurposing from a fragmented, manual workflow into a fast, intelligent, and scalable decision-support system, enabling pharma teams to focus on high-impact therapeutic opportunities.

Acknowledgements

EY Techathon 6.0 – Pharmaceutical Challenge

Thank You

