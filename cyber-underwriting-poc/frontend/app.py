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
    
    st.subheader("Quick Start")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("📋 **Company Assessment**\n\nEvaluate cyber security posture and generate risk scores.")
    
    with col2:
        st.info("📊 **Risk Dashboard**\n\nView historical underwriting results and metrics.")
    
    with col3:
        st.info("📄 **AI Report**\n\nRead detailed AI-generated analysis and recommendations.")
    
    with col4:
        st.info("🏠 **Home**\n\nNavigate back to overview anytime.")
    
    st.divider()
    
    st.subheader("How It Works")
    st.markdown("""
    1. **Assessment**: Answer questions about your company's cyber security controls
    2. **Risk Scoring**: The system applies a rule engine to calculate risk (0-100)
    3. **Premium Calculation**: Based on risk score and company profile
    4. **AI Summary**: Optional AI-generated executive summary (requires API key)
    5. **Dashboard**: View all historical assessments and trends
    """)
    
    st.divider()
    
    st.subheader("Key Features")
    st.markdown("""
    - ✅ Rule-based risk engine with explainable scoring
    - ✅ Machine learning classification (Critical/High/Medium/Low)
    - ✅ AI-generated executive summaries (optional)
    - ✅ Historical data tracking and analysis
    - ✅ Insurance premium calculation
    """)

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
    st.header("Risk Dashboard")
    st.write("Historical underwriting results and risk analysis.")
    
    try:
        response = requests.get(f"{API_BASE}/results", timeout=10)
        if response.ok:
            results = response.json()
            if results:
                # Display as table
                st.subheader("All Underwriting Results")
                
                # Prepare data for display
                display_data = []
                for result in results:
                    display_data.append({
                        "Company": result["company_name"],
                        "Industry": result["industry"],
                        "Risk Score": result["risk_score"],
                        "Risk Level": result["risk_level"],
                        "Premium": f"${result['premium']:.2f}",
                    })
                
                st.dataframe(display_data, use_container_width=True)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Assessments", len(results))
                with col2:
                    avg_risk = sum(r["risk_score"] for r in results) / len(results)
                    st.metric("Avg Risk Score", f"{avg_risk:.1f}")
                with col3:
                    total_premium = sum(r["premium"] for r in results)
                    st.metric("Total Premium", f"${total_premium:,.2f}")
                with col4:
                    critical_count = len([r for r in results if r["risk_level"] == "Critical"])
                    st.metric("Critical Cases", critical_count)
            else:
                st.info("No underwriting results yet. Create one from Company Assessment.")
        else:
            st.error("Failed to fetch results")
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

elif page == "AI Underwriting Report":
    st.header("AI Underwriting Report")
    st.write("Detailed AI-generated underwriting reports and analysis.")
    
    try:
        response = requests.get(f"{API_BASE}/results", timeout=10)
        if response.ok:
            results = response.json()
            if results:
                # Let user select a company to view detailed report
                company_options = {f"{r['company_name']} ({r['industry']})": r['id'] for r in results}
                selected_company = st.selectbox("Select Company", list(company_options.keys()))
                
                if selected_company:
                    result_id = company_options[selected_company]
                    detail_response = requests.get(f"{API_BASE}/results/{result_id}", timeout=10)
                    
                    if detail_response.ok:
                        result = detail_response.json()
                        
                        # Display key metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Risk Score", result["risk_score"])
                        with col2:
                            st.metric("Risk Level", result["risk_level"])
                        with col3:
                            st.metric("Premium", f"${result['premium']:.2f}")
                        
                        # Display AI Summary
                        st.subheader("Executive Summary")
                        st.write(result["ai_summary"])
                        
                        # Display Recommendations
                        st.subheader("Recommendations")
                        if result["recommendations"]:
                            recommendations = result["recommendations"].split("; ")
                            for rec in recommendations:
                                if rec.strip():
                                    st.write(f"• {rec.strip()}")
                        else:
                            st.info("No recommendations available")
            else:
                st.info("No underwriting results yet. Create one from Company Assessment.")
        else:
            st.error("Failed to fetch results")
    except Exception as e:
        st.error(f"Error loading report: {str(e)}")
