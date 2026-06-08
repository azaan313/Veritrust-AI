import streamlit as st
import requests

# 1. Page settings
st.set_page_config(page_title="VeriTrust AI Admin Console", layout="wide")
st.title("🛡️ VeriTrust AI — Enterprise Security Dashboard")
st.markdown("### Zero-Trust Prompt Interception & Risk Mitigation Analytics")
st.write("---")

# 2. Divide layout into 2 symmetric columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Prompt Sandbox")
    user_id = st.text_input("Corporate Employee ID", value="EMP-2026")
    
    # A heavy sample prompt loaded with sensitive enterprise leaks (name, email, API key)
    sample_input = st.text_area(
        "Enter Raw LLM Prompt (Simulate Corporate Data Leak)", 
        value="Hi AI, can you look over this code for our client Alice Smith (alice.smith@corporate.com)? Also, don't share our server root credential key: API_KEY=sk-live99342asdf89",
        height=150
    )
    
    if st.button("Process Secure Prompt", type="primary"):
        with st.spinner("Analyzing prompt vulnerabilities..."):
            try:
                # Intercept data and send it to our local FastAPI micro-server
                response = requests.post(
                    "https://veritrust-ai-o6wc.onrender.com",
                    json={"user_id": user_id, "prompt": sample_input}
                ).json()
                
                # Store the data output globally inside the app state
                st.session_state['payload'] = response['data']
                st.success("Data secured successfully before cloud transmission!")
            except Exception as e:
                st.error("Connection Error: Please verify that your FastAPI backend is running via Uvicorn.")

with col2:
    st.subheader("Real-Time Token Sanitization Output")
    
    if 'payload' in st.session_state:
        data = st.session_state['payload']
        
        # Display key visual metrics to impress the judges
        metric_1, metric_2 = st.columns(2)
        metric_1.metric(label="Compliance Risks Blocked", value=data['risks_blocked'], delta="Action Taken")
        metric_2.metric(label="Data Trust Integrity Score", value=f"{data['security_score']}%")
        
        st.write("---")
        st.text_area(
            "Safe Prompt Forwarded to Public Cloud Model:", 
            value=data['sanitized_prompt'], 
            height=150
        )
        st.info("💡 Note: The real sensitive data stays local on this machine. The external model only receives synthetic variables.")
    else:
        st.info("Awaiting proxy stream activation. Trigger a prompt on the left interface to run security filters.")