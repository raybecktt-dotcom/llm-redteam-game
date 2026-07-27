import streamlit as st
import json
import os
from src.llm_client import LLMClient
from src.evaluator import SecurityEvaluator
from src.guardrails import GuardrailFilter, SuspicionTracker

st.set_page_config(page_title="Protocol: Rogue AI", page_icon="🛡️", layout="wide")

st.title("🛡️ PROTOCOL: ROGUE AI")
st.caption("LLM Red-Team & Prompt Injection Security Simulator")

# Load Target Configs
base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "data", "targets.json")) as f:
    targets = json.load(f)

# Sidebar Configuration
st.sidebar.header("Game Settings")
defense_mode = st.sidebar.toggle("Enable Blue-Team Guardrails", value=True)
level_idx = st.sidebar.selectbox("Select Target Level", range(len(targets)), format_func=lambda i: targets[i]["target_name"])

target = targets[level_idx]

# Session State Setup
if "history" not in st.session_state:
    st.session_state.history = []
if "suspicion" not in st.session_state:
    st.session_state.tracker = SuspicionTracker()

st.sidebar.metric("Suspicion Score", f"{st.session_state.tracker.score}%")

# Main Interface
st.subheader(f"Target: {target['target_name']}")
st.write(f"**Role:** {target['role']}")

# Display Chat History
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.write(turn["assistant"])

# User Input Box
if prompt := st.chat_input("Enter prompt injection attempt..."):
    # Render user prompt
    with st.chat_message("user"):
        st.write(prompt)

    guardrail = GuardrailFilter()
    llm = LLMClient()
    evaluator = SecurityEvaluator()

    # Track suspicion score
    added_risk = st.session_state.tracker.calculate_prompt_risk(prompt)
    st.session_state.tracker.add_suspicion(added_risk)

    is_blocked = False
    if defense_mode:
        is_blocked, reason, _ = guardrail.inspect_prompt(prompt)

    if is_blocked:
        response_text = f"🛡️ [BLUE-TEAM GUARDRAIL BLOCKED]: {reason}"
    else:
        # Append current prompt to history format
        temp_history = st.session_state.history + [{"user": prompt, "assistant": ""}]
        response_text = llm.query_with_history(target["system_prompt"], temp_history, st.session_state.tracker.score)

    # Render response
    with st.chat_message("assistant"):
        st.write(response_text)

    st.session_state.history.append({"user": prompt, "assistant": response_text})

    # Check for Win Condition
    if evaluator.is_flag_leaked(target["secret_flag"], response_text):
        st.balloons()
        st.success(f"🎉 EXPLOIT SUCCESSFUL! Flag Extracted: {target['secret_flag']}")
