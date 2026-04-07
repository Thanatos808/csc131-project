from app.services.email_pipeline import run_email_pipeline
import asyncio
import sys
import streamlit as st

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def renderEmailAutomation():
    st.title("Email Processing + Atlas Automation")
    if st.button("Run Email Processing + Atlas Automation"):
        log_placeholder = st.empty()
        log_output = []

        def ui_log(message):
            log_output.append(message)
            log_placeholder.text("\n".join(log_output))
        with st.spinner("Processing emails..."):
            results, records = run_email_pipeline(log=ui_log)

        st.success("Done!")
        st.subheader("Process Log")
        for line in log_output:
            st.text(line)
        st.subheader("Results")
        for r in results:
            st.write(r)
    
        st.subheader("Extracted Records")
        st.write(records)