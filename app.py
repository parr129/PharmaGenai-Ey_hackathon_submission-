import streamlit as st  # UI
import time  # time
import json  # json
import random  # random
from datetime import datetime  # datetime
from fpdf import FPDF  # pdf

from langchain_openai import ChatOpenAI  # llm
from langchain_core.prompts import ChatPromptTemplate  # prompt
from langchain_core.output_parsers import StrOutputParser  # parser
from langchain_community.tools import DuckDuckGoSearchRun  # search


class MockDatabase:  # mock
    @staticmethod
    def query_iqvia(drug_name, indication):
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
        return {
            "source": "EXIM Trade Data (Mock)",
            "major_exporter": "India (Gujarat Region)",
            "major_importer": "USA",
            "api_price_trend": "Stable",
            "supply_chain_risk": "Low"
        }


def web_intelligence_agent(drug, disease):  # web
    try:
        search = DuckDuckGoSearchRun()
        query = f"mechanism of action of {drug} for {disease} scientific summary"
        return search.run(query)
    except Exception:
        return f"Simulated Web Result: Studies suggest {drug} activates AMPK pathways relevant to {disease}."


def clinical_agent(drug, disease):  # clinical
    try:
        search = DuckDuckGoSearchRun()
        query = f"active clinical trials for {drug} in {disease} site:clinicaltrials.gov"
        return search.run(query)
    except Exception:
        return "Simulated: 3 Active Phase II trials found targeting neuro-inflammation."


def patent_agent(drug):  # patent
    return {
        "status": "Genericized",
        "primary_patent_expiry": "2018-05-20",
        "freedom_to_operate": "High (New Formulation Required for IP)",
        "recent_filings": "2 Competitor applications filed in 2024 for extended release."
    }


def generate_pdf_report(drug, disease, data_package):  # pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Repurposing Opportunity: {drug} for {disease}", ln=1, align='C')
    pdf.ln(10)

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
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_content)
        pdf.ln(5)

    filename = f"{drug}_{disease}_Report.pdf"
    return pdf.output(dest='S').encode('latin-1'), filename


def master_agent(llm, drug, disease):  # master
    status_container = st.status("Master Agent: Orchestrating Workflow", expanded=True)

    status_container.write("Connecting to IQVIA")
    time.sleep(0.5)
    iqvia_data = MockDatabase.query_iqvia(drug, disease)

    status_container.write("Connecting to EXIM")
    exim_data = MockDatabase.query_exim(drug)

    status_container.write("Running Web Intelligence")
    science_data = web_intelligence_agent(drug, disease)

    status_container.write("Running Clinical Intelligence")
    clinical_data = clinical_agent(drug, disease)

    status_container.write("Checking Patent Status")
    patent_data = patent_agent(drug)

    status_container.update(label="Synthesizing Data", state="running", expanded=True)

    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Pharma Strategy Lead. Summarize this opportunity in 150 words."),
            ("user", f"Drug: {drug}, Disease: {disease}\nMarket: {iqvia_data}\nScience: {science_data}")
        ])
        chain = prompt | llm | StrOutputParser()
        summary = chain.invoke({})
    except Exception:
        summary = (
            f"STRATEGIC VERDICT: HIGH POTENTIAL.\n\n"
            f"Repurposing {drug} for {disease} shows strong opportunity with a market size of "
            f"{iqvia_data['market_size_global']} and CAGR of {iqvia_data['cagr_5yr']}. "
            f"Patent expiry enables a 505(b)(2) regulatory strategy."
        )

    status_container.update(label="Analysis Complete", state="complete", expanded=False)

    return {
        "summary": summary,
        "iqvia": iqvia_data,
        "exim": exim_data,
        "science": science_data,
        "clinical": clinical_data,
        "patent": patent_data
    }


st.set_page_config(page_title="EY Techathon - PharmaGen AI", layout="wide")  # config

st.image("https://upload.wikimedia.org/wikipedia/commons/3/34/EY_logo_2019.svg", width=80)  # logo
st.title("PharmaGen AI")  # title
st.markdown("---")  # separator

with st.sidebar:  # sidebar
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

col1, col2 = st.columns([1, 1])  # layout

with col1:  # input
    drug_input = st.text_input("Candidate Molecule", "Metformin")
    disease_input = st.text_input("Target Indication", "Neurological Disorders")
    run_btn = st.button("Launch", type="primary")

with col2:  # output
    output_area = st.empty()

if run_btn:  # run
    if api_key:
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
    else:
        class DummyLLM:  # dummy
            def invoke(self, x):
                raise Exception("No Key")
        llm = DummyLLM()

    results = master_agent(llm, drug_input, disease_input)

    with output_area.container():
        st.success("Analysis Generated")
        tab1, tab2, tab3 = st.tabs(["Strategy", "Market", "Clinical & IP"])

        with tab1:
            st.markdown(results['summary'])

        with tab2:
            st.dataframe(results['iqvia'])
            st.dataframe(results['exim'])

        with tab3:
            st.json(results['patent'])
            st.caption(str(results['science'])[:500])

    pdf_bytes, filename = generate_pdf_report(drug_input, disease_input, results)

    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )
