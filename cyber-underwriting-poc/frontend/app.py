import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cyber Underwriting POC", layout="wide")

st.title("AI-Native Cyber Insurance Underwriting")

st.sidebar.title("Navigation")
st.sidebar.info("This demo uses a rule engine and optional AI summary to support underwriters.")

page = st.sidebar.radio("Go to", ["Home", "Company Assessment", "Risk Dashboard", "AI Underwriting Report"])

if page == "Home":
    st.write("This proof of concept demonstrates how AI can augment cyber insurance underwriting with explainable risk scoring.")

elif page == "Company Assessment":
    with st.form("assessment_form"):
        st.text_input("Company Name", key="company_name")
        st.text_input("Industry", key="industry")
        st.number_input("Revenue", min_value=0, value=120_000_000, key="revenue")
        st.number_input("Employee Count", min_value=0, value=600, key="employee_count")
        st.checkbox("MFA Enabled", value=False, key="mfa")
        st.checkbox("EDR Enabled", value=True, key="edr")
        st.selectbox("Backup Strategy", ["No", "Yes", "Immutable"], key="backup")
        st.checkbox("Phishing Training", value=False, key="phish")
        st.checkbox("Incident Response Plan", value=False, key="ir")
        st.checkbox("Patch Management", value=False, key="patch")
        st.checkbox("Encryption", value=True, key="enc")
        st.selectbox("Third Party Risk", ["Low", "Medium", "High"], key="tpr")
        st.checkbox("Previous Claims", value=True, key="claims")
        submitted = st.form_submit_button("Run Underwriting")

    if submitted:
        payload = {
            "company_name": st.session_state.company_name,
            "industry": st.session_state.industry,
            "revenue": int(st.session_state.revenue),
            "employee_count": int(st.session_state.employee_count),
            "mfa_enabled": st.session_state.mfa,
            "edr_enabled": st.session_state.edr,
            "backup_strategy": st.session_state.backup,
            "phishing_training": st.session_state.phish,
            "incident_response_plan": st.session_state.ir,
            "patch_management": st.session_state.patch,
            "encryption": st.session_state.enc,
            "third_party_risk": st.session_state.tpr,
            "previous_claims": st.session_state.claims,
        }
        response = requests.post(f"{API_BASE}/underwrite", json=payload, timeout=30)
        if response.ok:
            result = response.json()
            st.success("Underwriting completed")
            st.metric("Risk Score", result["risk_score"])
            st.metric("Risk Category", result["risk_category"])
            st.metric("Premium", f"${result['premium']}")
            st.write(result["ai_summary"])
        else:
            st.error(response.text)

elif page == "Risk Dashboard":
    st.write("Risk dashboard placeholder. The backend exposes underwriting results for future charting expansion.")

elif page == "AI Underwriting Report":
    st.write("AI-generated underwriting report placeholder")
