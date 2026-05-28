import streamlit as st
import pandas as pd

from modules.insight_engine import generate_insights
from modules.simulator import simulate_improvement
from modules.data_generator import generate_data

st.set_page_config(layout="wide")

st.title("Intelligent Logistics Transformation Engine")

st.caption("Operational decision layer combining system signals and user behavior to drive actionable outcomes.")

# ---- DATA ----
if st.button("Generate New Data"):
    df = generate_data(100)
else:
    df = pd.read_excel("data/mock_data.xlsx")

# ---- AGGREGATION ----
region_summary = df.groupby("region").mean(numeric_only=True)
system_summary = df.groupby("system_name").mean(numeric_only=True)

insights = generate_insights(df)
top_issue = insights[0]

# ---- OPERATIONAL SITUATION ----
st.subheader("Operational Situation")

worst_region = region_summary["workflow_delay"].idxmax()
worst_delay = region_summary.loc[worst_region, "workflow_delay"]
worst_adoption = region_summary.loc[worst_region, "adoption_rate"]

col1, col2, col3 = st.columns(3)

col1.metric("Region with Highest Delay", worst_region)
col2.metric("Avg Delay", f"{worst_delay:.1f}")
col3.metric("Adoption Rate", f"{worst_adoption:.1f}")

# ---- REGION VIEW ----
st.subheader("Where is the problem coming from?")

def highlight_region(row):
    return ['background-color: #5c1f1f' if row.name == worst_region else '' for _ in row]

st.dataframe(region_summary.style.apply(highlight_region, axis=1))

# ---- SYSTEM DIAGNOSIS ----
st.subheader("System Diagnosis")

def highlight_system(df_):
    styles = pd.DataFrame('', index=df_.index, columns=df_.columns)

    max_error_idx = df_["error_rate"].idxmax()
    styles.loc[max_error_idx, "error_rate"] = 'background-color: #5c1f1f'

    max_latency_idx = df_["latency"].idxmax()
    styles.loc[max_latency_idx, "latency"] = 'background-color: #5c1f1f'

    return styles

st.dataframe(system_summary.style.apply(highlight_system, axis=None))

# ---- DECISION BREAKDOWN ----
st.subheader("Decision Breakdown")

st.markdown(f"""
### 📍 Focus Region: {top_issue['region']}

""")

col1, col2, col3 = st.columns(3)

col1.markdown("""
**Delay ↑ + Adoption ↓**

➡ Behavior Issue  
""")

col2.markdown("""
**Error Rate ↑**

➡ System Issue  
""")

col3.markdown("""
**Manual Overrides ↑**

➡ Process Issue  
""")

# ---- TRANSFORMATION STRATEGY ----
st.subheader("Transformation Strategy")

col1, col2 = st.columns(2)

col1.markdown("""
### Traditional Approach

• Training  
• Monitoring  
• Reactive fixes  

⬇  

**Limited Impact**
""")

col2.markdown("""
### Digital Approach

• Automation  
• Workflow Redesign  
• Smart Nudges  

⬇  

**Scalable Impact**
""")

# ---- SIMULATOR ----
st.subheader("Decision Impact Simulator")
st.caption("Simulating impact of real operational decisions")

action = st.selectbox(
    "Select Improvement Action",
    ["Improve Adoption", "Reduce Latency", "Reduce Errors"]
)

df_sim = simulate_improvement(df, action)

before = df["workflow_delay"].mean()
after = df_sim["workflow_delay"].mean()
improvement = ((before - after) / before) * 100

col1, col2 = st.columns(2)

col1.metric("Before (Delay)", f"{before:.1f}")
col2.metric("After (Delay)", f"{after:.1f}", f"{improvement:.1f}% improvement")

# ---- EXECUTION BOARD ----
st.subheader("Transformation Execution Board")

execution_data = []

for ins in insights[:3]:

    if ins["impact_score"] > 80:
        priority = "High"
    elif ins["impact_score"] > 65:
        priority = "Medium"
    else:
        priority = "Low"

    execution_data.append({
        "Region": ins["region"],
        "Problem": ins["issue"],
        "Action": ins["recommendation"],
        "Priority": priority,
        "Owner": "Ops / Product",
        "Status": "Not Started"
    })

execution_df = pd.DataFrame(execution_data)

def highlight_priority(df):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)

    for i, row in df.iterrows():
        if row["Priority"] == "High":
            styles.loc[i, "Priority"] = "background-color: #5c1f1f"
        elif row["Priority"] == "Medium":
            styles.loc[i, "Priority"] = "background-color: #5c3d1f"

    return styles
st.caption("From insight → action → ownership → measurable execution")
st.dataframe(execution_df.style.apply(highlight_priority, axis=None))

# ---- EXECUTION FLOW ----
st.subheader("Execution Flow")

st.markdown("""
### Detect → Validate → Assign → Execute → Monitor
""")

# ---- EXECUTION READY ----
st.subheader("Execution Ready")

st.code(f"""
Subject: Action Required – Delay Issue ({top_issue['region']})

Issue:
High workflow delay driven by low adoption.

Key Metrics:
Delay: {region_summary.loc[top_issue['region'], 'workflow_delay']:.1f}
Adoption: {region_summary.loc[top_issue['region'], 'adoption_rate']:.1f}

Action:
{top_issue['recommendation']}

Next Step:
Assign → Execute → Monitor

Prepared by: Transformation Engine
""")