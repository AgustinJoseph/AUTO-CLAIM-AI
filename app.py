import streamlit as st
import pandas as pd
from main import process_claims

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AUTO-CLAIM AI",
    layout="centered"  # Keeps content centered and clean
)

# ---------------- SESSION STATE ----------------
if "results_df" not in st.session_state:
    st.session_state.results_df = None

# ==============================================================================
#                               HERO BANNER SECTION
# ==============================================================================
st.title("🚗 AUTO CLAIM AI")
st.write(
    "⚡ **Intelligent Decision Engine:** Instantly audit and triage car insurance claims "
    "by mapping incoming incident reports directly against standard policy exclusions."
)

st.divider()

# ==============================================================================
#                               INPUT WORKSPACE
# ==============================================================================
st.subheader("📁 Claim Processing Center")

# A spacious dropzone for data ingestion
uploaded_file = st.file_uploader(
    "Drag and drop your batch warranty claims file here (CSV format only)", 
    type=["csv"],
    label_visibility="collapsed" # Hides the label for a cleaner layout
)

df = None

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✨ Dataset successfully mounted to pipeline memory.")
        
        # Expandable preview to keep the workspace clean
        with st.expander("🔍 View Raw Dataset Preview", expanded=False):
            st.dataframe(df.head(), use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ Error parsing file structure: {e}")

st.write("") # Tiny spacer

# Big, native, prominent full-width action button
generate = st.button("🚀 EXECUTE MULTI-AGENT TRIAGE", use_container_width=True, type="primary")

# ---------------- PIPELINE RUNNER ----------------
if generate:
    if df is None:
        st.sidebar.warning("Please upload a CSV file first.")
    else:
        # Visual interactive log showing the multi-agent graph progression
        with st.status("🧠 Running Graph Network Workflows...", expanded=True) as status:
            st.write("📖 Reading policy parameters...")
            # Run the actual backend process
            st.session_state.results_df = process_claims(df)
            st.write("🛡️ Calculating risk scores...")
            st.write("📊 Evaluating claims logic...")
            status.update(label="✅ All agent processes finished!", state="complete")

# ==============================================================================
#                               OUTPUT DASHBOARD
# ==============================================================================
results_df = st.session_state.results_df

if results_df is not None:
    st.divider()
    st.header("📊 Evaluation Analytics")

    # Metrics Layout
    total = len(results_df)
    approve = (results_df["decision"] == "Approve claim").sum()
    reject = (results_df["decision"] == "Reject claim").sum()
    escalate = (results_df["decision"] == "Escalate to HITL").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 Total Batch Items", total)
    col2.metric("🟩 Approved", approve)
    col3.metric("🟥 Rejected", reject)
    col4.metric("🟨 Escalated (HITL)", escalate)

    st.write("") # Spacer

    # Organizing layout outputs beautifully into clean, interactive native Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Complete Pipeline Logs", "🎯 Triage Matrix", "🔍 Agent Trace Telemetry"])

    with tab1:
# Hide the raw dictionary/object column from the production data view
        display_df = results_df.drop(columns=["agent_trace"], errors="ignore")
        
        st.dataframe(display_df, use_container_width=True, height=350)
        
        # Download button directly embedded in the table view
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Batch Audit Report",
            data=csv,
            file_name="auto_claim_results.csv",
            mime="text/csv"
        )

    with tab2:
        # Minimalist specific table view for quick checks
        st.dataframe(
            results_df[["decision", "fraud_score", "policy_check"]],
            use_container_width=True,
            height=300
        )

    with tab3:
        # Dropdown selection to inspect individual rows
        idx = st.selectbox("Select specific claim instance index to audit:", results_df.index)
        trace = results_df.loc[idx, "agent_trace"]

        if trace:
            st.write("---")
            for t in trace:
                # Colorful, clear messaging blocks for agent conversation simulation
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(f"**Node Area: {t['agent']}**")
                    st.caption("Prompt Context Given:")
                    st.info(t["prompt"])
                    st.caption("Generated Analytical Conclusion:")
                    st.code(t["response"], language="text")
        else:
            st.warning("No tracking telemetry metadata discovered for this claim row.")

else:
    # A cleaner layout fallback state when the screen is empty
    st.write("")
    st.divider()
    st.markdown(
        "<center style='color:#6b7280; font-size:14px;'>"
        "📥 Awaiting dataset drop to initialize decision framework channels."
        "</center>", 
        unsafe_allow_html=True
    )