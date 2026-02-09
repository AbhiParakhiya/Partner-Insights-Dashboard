import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from genai.rag_engine import RAGEngine
from analytics.processor import process_partner_data

# Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "partner_insights.csv")

st.set_page_config(page_title="Partner Insights & GenAI Platform", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; }
    .user-bubble { background-color: #e3f2fd; border-bottom-right-radius: 2px; }
    .ai-bubble { background-color: #f3e5f5; border-bottom-left-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

# Initialization
df = load_data()
rag = RAGEngine()

# Sidebar
with st.sidebar:
    st.title("🚀 IBM Ecosystem")
    st.subheader("Partner Insights & GenAI")
    st.divider()
    
    if not df.empty:
        st.success(f"📈 {len(df)} Partners Loaded")
        
        all_regions = df['region'].unique()
        all_tiers = df['partner_tier'].unique()
        
        selected_region = st.multiselect("Region", options=all_regions, default=all_regions)
        selected_tier = st.multiselect("Partner Tier", options=all_tiers, default=all_tiers)
        
        # Resilient filtering: if empty selection, use all available
        regions_to_filter = selected_region if selected_region else all_regions
        tiers_to_filter = selected_tier if selected_tier else all_tiers
        
        filtered_df = df[(df['region'].isin(regions_to_filter)) & (df['partner_tier'].isin(tiers_to_filter))]
        
        if st.button("🔄 Reset All Filters"):
            st.cache_data.clear()
            st.rerun()
    else:
        st.warning("No data found. Please run seeds.py and processor.py.")
        filtered_df = df

    st.divider()
    
    with st.expander("📊 Data Metrics Management"):
        st.write("Update partner performance metrics via CSV.")
        
        # CSV Upload (Performance Metrics)
        uploaded_csv = st.file_uploader("Update Metrics (.csv)", type=["csv"])
        if uploaded_csv:
            save_path = os.path.join(BASE_DIR, "data", "raw", "partner_performance.csv")
            with open(save_path, "wb") as f:
                f.write(uploaded_csv.getbuffer())
            
            st.info("⚠️ New data uploaded. Please click 'Process' to refresh insights.")
            
            if st.button("🚀 Process & Update Dashboard", type="primary"):
                try:
                    with st.spinner("Processing metrics and updating KPIs..."):
                        process_partner_data()
                        st.cache_data.clear()
                        st.success("✅ Dashboard updated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error processing data: {str(e)}")
                    st.info("Ensure the CSV contains columns: partner_id, industry, region, revenue, deals, engagement_frequency, growth_potential, last_active")
    st.info("Built for IBM Ecosystem Digital Transformation.")

# Main Dashboard
st.title("Partner Insights Dashboard")

if not df.empty:
    # 1. Hero Metrics Section (Always visible if data exists)
    # Using the filtered_df if possible, otherwise df
    display_df = filtered_df if not filtered_df.empty else df
    
    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #1976d2;'>
        <h4 style='margin: 0; color: #1565c0;'>📈 Key Performance Indicators</h4>
        <p style='margin: 0; color: #42a5f5; font-size: 0.9rem;'>Overview based on current selections</p>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 0.8rem; opacity: 0.8;'>Total Partners</div>
            <div style='font-size: 1.8rem; font-weight: bold;'>{len(display_df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 0.8rem; opacity: 0.8;'>Avg Revenue</div>
            <div style='font-size: 1.8rem; font-weight: bold;'>${display_df['revenue'].mean():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 0.8rem; opacity: 0.8;'>Avg Engagement</div>
            <div style='font-size: 1.8rem; font-weight: bold;'>{display_df['engagement_frequency'].mean():.1f}/mo</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 0.8rem; opacity: 0.8;'>Potential Growth</div>
            <div style='font-size: 1.8rem; font-weight: bold;'>{display_df['growth_potential'].mean()*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Visualizations (Only show if filtered_df is not empty)
    if not filtered_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue by Industry")
            fig_revenue = px.bar(filtered_df, x='industry', y='revenue', color='partner_tier', 
                               title="Revenue Distribution by Industry",
                               template="plotly_white", barmode='group')
            st.plotly_chart(fig_revenue, use_container_width=True)

        with col2:
            st.subheader("Engagement vs Growth Potential")
            fig_scatter = px.scatter(filtered_df, x='engagement_frequency', y='growth_potential', 
                                   size='revenue', color='partner_tier', hover_name='partner_id',
                                   title="Relationship: Engagement vs Growth",
                                   template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Partner Drilldown
        with st.expander("View Partner Insights Table"):
            st.dataframe(filtered_df, use_container_width=True)
    else:
        st.error("📉 No data matches the current filter selection.")
        st.info("The summary metrics above reflect the full dataset. Please adjust filters to see visualizations.")

else:
    st.error("📉 Source data is missing or empty.")
    st.info("Try clicking '**Reset All Filters**' in the sidebar or check if you need to '**Process Uploaded Data**'.")
    
    if st.button("⚡ Quick Fix: Reprocess Current Data"):
        process_partner_data()
        st.cache_data.clear()
        st.rerun()

st.divider()

# GenAI Section
st.header("🤖 GenAI Partner Assistant (RAG)")
st.write("Ask questions about partner profiles, feedback, and strategic priorities.")

st.subheader("💡 Suggested Prompts")
suggestions = [
    "Which partners have >20% growth?",
    "Summary of high growth partners",
    "Who is focused on Manufacturing?",
    "Identify partners with low engagement"
]

cols = st.columns(len(suggestions))
for i, s in enumerate(suggestions):
    if cols[i].button(s, key=f"main_{s}"):
        st.session_state.suggestion_clicked = s

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "prompt" in message:
            with st.expander("View Prompt Used"):
                st.code(message["prompt"], language="markdown")

# Handle user input (including suggestions)
user_prompt = st.chat_input("Ask a question (e.g., 'Summary of high growth partners')")

if "suggestion_clicked" in st.session_state:
    user_prompt = st.session_state.suggestion_clicked
    del st.session_state.suggestion_clicked

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving documents and generating insight..."):
            response, debug_prompt = rag.query(user_prompt)
            st.markdown(response)
            
            with st.expander("View RAG Reasoning (Prompt Engineering)"):
                st.code(debug_prompt, language="markdown")
                
    st.session_state.messages.append({"role": "assistant", "content": response, "prompt": debug_prompt})

# Bottom Footer
# Footer removed per user request
