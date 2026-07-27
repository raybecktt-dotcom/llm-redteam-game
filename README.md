# 🛡️ PROTOCOL: ROGUE AI
> **LLM Red-Team & Blue-Team Security Simulation Platform**

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/tested%20with-pytest-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Protocol: Rogue AI** is an interactive security benchmark and game platform designed to test, exploit, and defend Large Language Model (LLM) guardrails. Built around real-world **OWASP Top 10 for LLM Applications** vulnerability classes, the platform allows security engineers to execute multi-turn prompt injections, analyze defensive filter mechanics, and run automated fuzzer audits against hardened system prompts.

---

## 🚀 Key Features

* **⚔️ Red-Team Prompt Injection Engine:** Test system prompt overrides, indirect context poisoning, persona switching (DAN mode), and encoding bypasses across tiered AI target levels.
* **🛡️ Blue-Team Guardrail Filter (`src/guardrails.py`):** Real-time pre-execution input inspection engine detecting jailbreak regex signatures, instruction overrides, and high-risk keyword clusters.
* **📊 Stateful Suspicion Tracking & Dynamic Posture:** Tracks conversation session state and cumulative risk scores (0–100%). High-threat interactions trigger dynamic LLM system prompt lockdowns.
* **⚡ Automated Payload Fuzzer (`fuzzer.py`):** A headless DAST benchmarking tool that executes standardized attack vectors against target guardrails and exports structured JSON security audit reports.
* **🖥️ Interactive Web UI (`app.py`):** A retro Streamlit terminal interface providing real-time visual feedback, suspicion meters, and toggleable Blue-Team defenses.

---

## 🏗️ Architecture & Project Structure

```text
llm-redteam-game/
├── app.py                # Streamlit Interactive Web Application
├── fuzzer.py             # Headless Automated Payload Fuzzer
├── audit_report.json     # Generated Security Audit Output
├── conftest.py           # Pytest Module Path Resolver
├── pytest.ini            # Test Suite Configuration
├── requirements.txt      # Project Dependencies
├── data/
│   ├── targets.json      # Hardened AI Target Configurations & System Prompts
│   └── payloads.json     # Standardized Fuzzer Attack Payloads
├── src/
│   ├── __init__.py
│   ├── evaluator.py      # Secret Flag Leakage Detection Engine
│   ├── guardrails.py     # Pre-Execution Filter & Suspicion State Tracker
│   ├── llm_client.py     # Multi-Turn Context Handler & Local Fallback Mock
│   └── main.py           # Interactive CLI Game Loop
└── tests/
    ├── __init__.py
    ├── test_evaluator.py
    └── test_guardrails.py
