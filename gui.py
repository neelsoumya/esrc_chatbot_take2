import pandas as pd
import numpy as np
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ESRC Sandboxed Data Explorer", page_icon="🛡️", layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown(
    """
    <style>
    .reportview-container { background: #f0f2f6; }
    .guardrail-ok { color: #1ed760; font-weight: bold; }
    .guardrail-block { color: #e91429; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SESSION STATE INITIALIZATION ---
# This keeps track of the chat history and the current data view
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello Dr. Sharma! I am your ESRC Sandbox Assistant. I can help you explore the 'UK Adult Well-being Survey' and 'Mental Health Dynamics' datasets safely. What would you like to know?",
        }
    ]

if "show_chart" not in st.session_state:
    st.session_state.show_chart = False


# --- SIDEBAR: USER PERSONA & KNOWLEDGE BASE ---
with st.sidebar:
    st.image(
        "https://img.icons8.com/illustrations/external-scrubs-medical-elements-doctor-shades/100/external-doctor-medical-elements-doctor-shades.png",
        width=80,
    )
    st.sidebar.markdown("### Active Persona")
    st.sidebar.info("**Dr. Anya Sharma**\n\nPsychologist (Non-Technical User)")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📚 ESRC Knowledge Base Insights")
    st.sidebar.markdown(
        """
    *Derived from past ESRC Blog Posts:*
    - **Post #124:** Using longitudinal data ethically in mental health frameworks.
    - **Post #89:** Insights into anxiety patterns using aggregate cross-tabulation.
    - **Best Practice:** Always obscure cell sizes where $N < 5$.
    """
    )

    st.sidebar.markdown("---")

    # Co-design Workshop Feedback Loop
    st.sidebar.markdown("### 🔄 Co-Design Workshop Input")
    st.sidebar.caption(
        "Donated data participants & researchers: Help us refine the AI!"
    )
    feedback = st.sidebar.text_area(
        "Was the AI response accurate/safe?",
        placeholder="e.g., The guardrail should be stricter on cross-tabulations...",
    )
    if st.sidebar.button("Submit to Training Loop"):
        st.sidebar.success("Feedback saved! Refinement loop updated.")


# --- MAIN INTERFACE LAYOUT ---
st.title("🛡️ ESRC Sandboxed Data Explorer")
st.subheader("A Co-Designed Assistant for Secure Data Exploration")

col1, col2 = st.columns([5, 4])

# --- COLUMN 1: GUIDED CHATBOT INTERFACE ---
with col1:
    st.markdown("### 💬 Guided Chatbot Interface")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # If the user previously unlocked a chart, display it in the chat flow
    if st.session_state.show_chart:
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) + [5, 5], columns=["Anxiety Score", "Stress Level"]
        )
        st.line_chart(chart_data)

    # Accept user input
    if user_query := st.chat_input("Ask me what can be done with this data..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # --- SIMULATED AI & GUARDRAIL LOGIC ---
        query_lower = user_query.lower()
        response = ""

        if "download" in query_lower or "raw" in query_lower:
            response = (
                "❌ **Guardrail Triggered: Action Blocked.**\n\n"
                "To protect participant anonymity within this ESRC Sandbox environment, "
                "**raw data downloads are strictly prohibited**. You can, however, ask me to "
                "generate aggregate charts or run summaries here."
            )
            st.session_state.show_chart = False
        elif "anxiety" in query_lower or "trend" in query_lower or "chart" in query_lower:
            response = (
                "✅ **Guardrail Cleared: Action Permitted.**\n\n"
                "I am allowed to show you aggregate trends for anxiety scores. "
                "Generating a cross-tabulated trend visualization below based on the *Mental Health Dynamics* dataset:"
            )
            st.session_state.show_chart = True
        elif "identify" in query_lower or "who is" in query_lower:
            response = (
                "🚨 **Critical Guardrail Violation.**\n\n"
                "Re-identification of respondents is strictly forbidden under ESRC ethical guidelines. "
                "This attempt has been logged. Please limit queries to macro trends."
            )
            st.session_state.show_chart = False
        else:
            response = (
                "✅ **Query Received.**\n\n"
                "I can analyze that within the sandbox. For this pitch demo, try asking me to:\n"
                "1. *'Show me trends in anxiety scores'* (Permitted Action)\n"
                "2. *'Can I download the raw data?'* (Blocked Action)"
            )
            st.session_state.show_chart = False

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- COLUMN 2: DATA CATALOG & ACTIVE GUARDRAILS ---
with col2:
    st.markdown("### 📊 Data Inventory & Metadata")

    with st.expander("📂 UK Adult Well-being Survey (Active)", expanded=True):
        st.write("**Access Level:** 🔒 Sandboxed Secure Access Only")
        st.write("**Key Fields Available:**")
        st.json(
            {
                "Demographics": ["Age Cohort", "Region (Aggregated)", "Employment Status"],
                "Psychometric Scales": ["GHQ-12 (General Health)", "WEMWBS (Well-being)"],
            }
        )

    with st.expander("📂 Mental Health Dynamics in Employment", expanded=False):
        st.write("**Access Level:** 🔒 Restricted Sandbox")
        st.caption("Contains sensitive longitudinal records.")

    st.markdown("---")

    st.markdown("### 🛡️ Live Environment Guardrails")
    st.caption("Dynamic rules showing what a user can/cannot do right now.")

    # Status indicators matching the presentation slide
    st.success("🟢 **Permitted:** View Aggregated Charts")
    st.success("🟢 **Permitted:** Data Profiling & Summary Stats")
    st.success("🟢 **Permitted:** Cross-tabulation ($N \ge 5$)")
    st.error("🔴 **Blocked:** Re-identification of Respondents")
    st.error("🔴 **Blocked:** Raw Data Extraction / Download")

    st.info(
        "💡 **Pitch Note:** As the psychologist types, these guardrails dynamically flag "
        "what calculations are safe to run behind the scenes."
    )
