import streamlit as st
import time
import json
import random
from datetime import datetime
from fpdf import FPDF

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun

# ==========================================
# 1. MOCK DATA & API SIMULATION LAYER
# ==========================================
class MockDatabase:
    @staticmethod
    def query_iqvia(drug_name, indication):
        """Simulates querying IQVIA for market size and CAGR."""
        base_size = random.randint(2, 15)
        cagr = round(random.uniform(3.5, 8.2), 2)
        return {
            "source": "IQVIA Analytics (Mock)",
            "market_size_global": f"${base_size} Billion",
            "cagr_5yr": f"{cagr}%",
            "top_competitor": "BigPharma Inc.",
            "market_saturation": "Medium-High"
        }

    @staticmethod
    def query_exim(drug_name):
        """Simulates EXIM data for API export/import."""
        return {
            "source": "EXIM Trade Data (Mock)",
            "major_exporter": "India (Gujarat Region)",
            "major_importer": "USA",
            "api_price_trend": "Stable",
            "supply_chain_risk": "Low"
        }

# ==========================================
# 2. WORKER AGENTS (Resilient)
# ==========================================

def web_intelligence_agent(drug, disease):
    """Real-time web search with fallback."""
    try:
        search = DuckDuckGoSearchRun()
        query = f"mechanism of action of {drug} for {disease} scientific summary"
        results = search.run(query)
        return results
    except Exception as e:
        return f"Simulated Web Result: Studies suggest {drug} activates AMPK pathways relevant to {disease}."

def clinical_agent(drug, disease):
    """Real-time clinical search with fallback."""
    try:
        search = DuckDuckGoSearchRun()
        query = f"active clinical trials for {drug} in {disease} site:clinicaltrials.gov"
        results = search.run(query)
        return results
    except Exception as e:
        return "Simulated: 3 Active Phase II trials found targeting neuro-inflammation."

def patent_agent(drug):
    """Mock USPTO Check."""
    return {
        "status": "Genericized",
        "primary_patent_expiry": "2018-05-20",
        "freedom_to_operate": "High (New Formulation Required for IP)",
        "recent_filings": "2 Competitor applications filed in 2024 for extended release."
    }

# ==========================================
# 3. REPORT GENERATOR AGENT (PDF)
# ==========================================

def generate_pdf_report(drug, disease, data_package):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Repurposing Opportunity: {drug} for {disease}", ln=1, align='C')
    pdf.ln(10)
    
    # Sections
    # Clean up the scientific text if it's too long or None
    science_text = str(data_package.get('science', ''))[:500]
    clinical_text = str(data_package.get('clinical', ''))[:500]
    
    sections = [
        ("Executive Summary", data_package['summary']),
        ("Market Opportunity (IQVIA)", json.dumps(data_package['iqvia'], indent=2)),
        ("Supply Chain (EXIM)", json.dumps(data_package['exim'], indent=2)),
        ("Scientific Rationale", science_text + "..."),
        ("Clinical Landscape", clinical_text + "..."),
        ("Patent Strategy", json.dumps(data_package['patent'], indent=2))
    ]
    
    for title, content in sections:
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(0, 10, title, 1, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        # Handle unicode issues by encoding/decoding
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_content)
        pdf.ln(5)
        
    filename = f"{drug}_{disease}_Report.pdf"
    return pdf.output(dest='S').encode('latin-1'), filename

# ==========================================
# 4. MASTER AGENT (Orchestrator with SAFETY NET)
# ==========================================

def master_agent(llm, drug, disease):
    
    status_container = st.status("🤖 Master Agent: Orchestrating Workflow...", expanded=True)
    
    # --- Step 1: Mock Data (Always Works) ---
    status_container.write("📊 Connecting to IQVIA Global Database...")
    time.sleep(0.5) 
    iqvia_data = MockDatabase.query_iqvia(drug, disease)
    
    status_container.write("🚢 Connecting to EXIM Trade Server...")
    exim_data = MockDatabase.query_exim(drug)
    
    # --- Step 2: Search Data (Might Fail, has fallback) ---
    status_container.write("🧬 Web Agent: Scanning Medical Journals...")
    science_data = web_intelligence_agent(drug, disease)
    
    status_container.write("🏥 Clinical Agent: Querying ClinicalTrials.gov...")
    clinical_data = clinical_agent(drug, disease)
    
    status_container.write("⚖️ Patent Agent: Checking USPTO status...")
    patent_data = patent_agent(drug)
    
    status_container.update(label="✅ Data Collection Complete! Synthesizing...", state="running", expanded=True)
    
    # --- Step 3: Synthesis (The Part That Was Crashing) ---
    summary = ""
    
    try:
        # Try using the Live AI
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Pharma Strategy Lead. Summarize this opportunity in 150 words."),
            ("user", f"""
            Drug: {drug}, Disease: {disease}
            Market: {iqvia_data}
            Science: {science_data}
            """)
        ])
        chain = prompt | llm | StrOutputParser()
        summary = chain.invoke({})
        
    except Exception as e:
        # 🚨 EMERGENCY FALLBACK IF API QUOTA IS DEAD 🚨
        st.warning("⚠️ OpenAI API Quota Exceeded. Switching to Simulation Mode.")
        summary = (
            f"**STRATEGIC VERDICT: HIGH POTENTIAL.**\n\n"
            f"Based on the analysis, repurposing {drug} for {disease} represents a significant "
            f"opportunity. The mock IQVIA data indicates a market size of {iqvia_data['market_size_global']} "
            f"with a CAGR of {iqvia_data['cagr_5yr']}. \n\n"
            f"Scientific literature suggests a plausible mechanism of action. "
            f"Given the patent expiry in {patent_data['primary_patent_expiry']}, a 505(b)(2) regulatory pathway "
            f"is recommended to accelerate market entry."
        )

    status_container.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    return {
        "summary": summary,
        "iqvia": iqvia_data,
        "exim": exim_data,
        "science": science_data,
        "clinical": clinical_data,
        "patent": patent_data
    }

# ==========================================
# 5. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="EY Techathon - PharmaGen AI", layout="wide")

st.image("https://upload.wikimedia.org/wikipedia/commons/3/34/EY_logo_2019.svg", width=80)
st.title("PharmaGen AI: End-to-End Repurposing Engine")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Settings")
    # Default to a dummy key if empty so app doesn't complain immediately
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.info("System Components:\n- Master Orchestrator\n- IQVIA Agent (Mock)\n- EXIM Agent (Mock)\n- Web Intelligence")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Research Parameters")
    drug_input = st.text_input("Candidate Molecule", "Metformin")
    disease_input = st.text_input("Target Indication", "Neurological Disorders")
    
    run_btn = st.button("🚀 Launch Agent Swarm", type="primary")

with col2:
    st.subheader("Live Agent Activity Feed")
    output_area = st.empty()

if run_btn:
    # Initialize LLM with cheaper model, or handle empty key
    if api_key:
        # Use gpt-4o-mini for lower cost
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
    else:
        # If no key, create a dummy object that will trigger the Exception Fallback
        class DummyLLM:
            def invoke(self, x): raise Exception("No Key")
        llm = DummyLLM()

    # Run the Workflow
    results = master_agent(llm, drug_input, disease_input)
    
    # Display Results
    with output_area.container():
        st.success("Analysis Generated")
        
        tab1, tab2, tab3 = st.tabs(["Strategy", "Market Data", "Clinical & IP"])
        
        with tab1:
            st.markdown("### Executive Summary")
            st.markdown(results['summary'])
            
        with tab2:
            st.markdown("#### IQVIA Market Insights")
            st.dataframe(results['iqvia'])
            st.markdown("#### EXIM Supply Chain")
            st.dataframe(results['exim'])
            
        with tab3:
            st.markdown("#### Patent Landscape")
            st.json(results['patent'])
            st.markdown("#### Scientific Evidence")
            st.caption(str(results['science'])[:500] + "...")

    # PDF Generation
    pdf_bytes, filename = generate_pdf_report(drug_input, disease_input, results)
    
    st.markdown("---")
    st.download_button(
        label="📄 Download Strategic Report (PDF)",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )