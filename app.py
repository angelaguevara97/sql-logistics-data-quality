from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="SQL Logistics Data Quality Lab", page_icon="🔎", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1280px; padding-top: 2.5rem; padding-bottom: 3rem;}
[data-testid="stMetric"] {background:#f7f9fc; border:1px solid #e3e8ef; padding:16px; border-radius:14px;}
.small-note {color:#6b7280; font-size:.92rem;}
/* Keep long SQL readable without letting one query dominate the case study. */
[data-testid="stCodeBlock"] pre {max-height: 480px; overflow-y: auto;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_csv(name):
    return pd.read_csv(ROOT / "results" / name)

@st.cache_data
def load_sql(name):
    return (ROOT / "sql" / name).read_text()

profile = load_csv("01_data_profile.csv").iloc[0]
dupes = load_csv("02_duplicate_events.csv").iloc[0]
billing = load_csv("03_billing_reconciliation.csv").iloc[0]
locations = load_csv("04_location_quality.csv")
monthly = load_csv("05_monthly_trends.csv")

st.title("SQL Logistics Data Quality Lab")
st.caption("Interactive portfolio case study using entirely synthetic logistics and billing data. SQL remains the analytical centerpiece; Streamlit only presents the investigation.")

st.subheader("Investigation snapshot")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Raw intake rows", f"{int(profile.raw_rows):,}")
c2.metric("Distinct rental events", f"{int(profile.distinct_events):,}")
c3.metric("Identical replay events", f"{int(dupes.identical_replay_events):,}")
c4.metric("Events with core exceptions", "300")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Overcharged events", f"{int(billing.overcharged_events):,}")
c2.metric("Synthetic overcharge", f"${billing.overcharge_cents/100:,.0f}")
c3.metric("Billing discrepancy rate", f"{billing.discrepancy_pct_of_rate_matched_events:.2f}%")
c4.metric("Conflicting event IDs", f"{int(dupes.conflicting_event_ids):,}")

st.divider()
st.subheader("Choose a SQL investigation")
checks = {
    "Duplicate event detection": {
        "sql":"02_duplicate_events.sql",
        "summary":"Distinguishes identical retransmissions from conflicting versions of the same business event.",
    },
    "Billing reconciliation": {
        "sql":"03_billing_reconciliation.sql",
        "summary":"Compares billed amounts with expected charges based on rental duration and reference daily rates.",
    },
    "Location reference quality": {
        "sql":"04_location_quality.sql",
        "summary":"Classifies canonical matches, formatting aliases, missing locations, and unknown location references.",
    },
}
choice = st.selectbox("Data quality check", list(checks), label_visibility="collapsed")
st.write(checks[choice]["summary"])

left,right = st.columns([1.08,.92], gap="large")
with left:
    st.markdown("### SQL used")
    st.code(load_sql(checks[choice]["sql"]), language="sql", line_numbers=True)
    st.caption("Scroll inside the SQL panel to inspect the complete query.")

with right:
    st.markdown("### Findings")
    if choice == "Duplicate event detection":
        a,b = st.columns(2)
        a.metric("Repeated event IDs", f"{int(dupes.repeated_event_ids):,}")
        b.metric("Extra received rows", f"{int(dupes.extra_rows):,}")
        a.metric("Identical replays", f"{int(dupes.identical_replay_events):,}")
        b.metric("Conflicting IDs", f"{int(dupes.conflicting_event_ids):,}")
        st.success("The repeated records are identical replays, not conflicting business-event versions. Raw intake remains preserved while exact business-record copies can be collapsed for event-level analysis.")
    elif choice == "Billing reconciliation":
        a,b = st.columns(2)
        a.metric("Events reconciled", f"{int(billing.unique_events):,}")
        b.metric("Unmatched rates", f"{int(billing.unmatched_rate_events):,}")
        a.metric("Overcharged events", f"{int(billing.overcharged_events):,}")
        b.metric("Synthetic variance", f"${billing.overcharge_cents/100:,.0f}")
        st.warning("The USD 1,250 is synthetic billing variance under the project rules. It is not recovered revenue or realized savings.")
    else:
        chart_data = locations.copy()
        chart_data["label"] = chart_data.location_quality.str.replace("_"," ").str.title()
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("event_count:Q", title="Unique events"),
            y=alt.Y("label:N", sort="-x", title=None),
            tooltip=[alt.Tooltip("label:N", title="Classification"), alt.Tooltip("event_count:Q", title="Events", format=","), alt.Tooltip("pct_of_unique_events:Q", title="Percent", format=".2f")],
        ).properties(height=260)
        st.altair_chart(chart, use_container_width=True)
        st.dataframe(locations.rename(columns={"location_quality":"Classification","event_count":"Events","pct_of_unique_events":"Percent"}), hide_index=True, use_container_width=True)

st.divider()
st.subheader("Monthly exception trend")
st.write("Counts alone can mislead when monthly volume changes, so the investigation compares exception rates as well as totals.")
trend = monthly.copy()
trend["Month"] = pd.to_datetime(trend.event_month).dt.strftime("%b %Y")
line = alt.Chart(trend).mark_line(point=True).encode(
    x=alt.X("Month:N", sort=None, title=None),
    y=alt.Y("exception_pct:Q", title="Exception rate (%)", scale=alt.Scale(zero=False)),
    tooltip=["Month:N", alt.Tooltip("total_events:Q", title="Events", format=","), alt.Tooltip("any_exception_events:Q", title="Exception events", format=","), alt.Tooltip("exception_pct:Q", title="Exception rate", format=".2f")],
).properties(height=300)
st.altair_chart(line, use_container_width=True)

st.markdown("### Investigation workflow")
workflow = pd.DataFrame([
    ["1", "Preserve raw intake", "Keep source rows unchanged for traceability."],
    ["2", "Detect retransmissions", "Compare business fields before classifying repeated event IDs."],
    ["3", "Reconcile billing", "Join reference rates and calculate expected charges and variance."],
    ["4", "Validate references", "Separate formatting aliases from missing or unknown locations."],
    ["5", "Monitor trends", "Compare monthly counts and rates rather than counts alone."],
], columns=["Step","Control","Why it matters"])
st.dataframe(workflow, hide_index=True, use_container_width=True)

st.info("All company names, logistics events, rates, locations, billing amounts, and findings are synthetic. The project demonstrates explainable SQL and data-quality reasoning, not real employer performance.")
