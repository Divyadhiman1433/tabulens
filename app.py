from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from tabulens import DatasetAnalyzer

ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "data" / "campus_energy_sample.csv"

st.set_page_config(page_title="TabuLens", page_icon="◫", layout="wide")
st.markdown(
    """
    <style>
    :root { --ink:#18181b; --muted:#71717a; --line:#e4e4e7; --paper:#fafafa; --accent:#0f766e; }
    .stApp { background: var(--paper); color: var(--ink); }
    h1, h2, h3 { color: var(--ink); letter-spacing: -0.02em; }
    [data-testid="stMetric"] { border-top: 2px solid var(--ink); padding-top: 0.65rem; }
    [data-testid="stSidebar"] { background: #f4f4f5; border-right: 1px solid var(--line); }
    .note { border-left: 3px solid var(--accent); padding: .75rem 1rem; color: var(--muted); background: white; }
    .small { color: var(--muted); font-size: .92rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_sample() -> pd.DataFrame:
    return pd.read_csv(SAMPLE)


def load_uploaded(file: BytesIO) -> pd.DataFrame:
    return pd.read_csv(file)


st.title("TabuLens")
st.caption("A beginner-friendly dataset readiness assistant")

with st.sidebar:
    st.header("Dataset")
    source = st.radio("Choose a source", ["Campus energy sample", "Upload a CSV"])
    uploaded = st.file_uploader("CSV file", type=["csv"], disabled=source != "Upload a CSV")
    st.divider()
    st.markdown("**What the app checks**")
    st.markdown("Missing values  ·  duplicate rows  ·  column types  ·  constant columns  ·  unusual numeric records")

if source == "Upload a CSV" and uploaded is not None:
    frame = load_uploaded(uploaded)
elif source == "Upload a CSV":
    st.info("Upload a CSV file or switch to the sample dataset.")
    st.stop()
else:
    frame = load_sample()

try:
    analyzer = DatasetAnalyzer(frame)
except ValueError as error:
    st.error(str(error))
    st.stop()

profile = analyzer.profile()
overview, cleaning, anomalies, learning = st.tabs(["Overview", "Clean", "Anomalies", "How it works"])

with overview:
    st.subheader("Dataset overview")
    a, b, c, d, e = st.columns(5)
    a.metric("Quality score", f"{profile.quality_score}/100")
    b.metric("Rows", f"{profile.rows:,}")
    c.metric("Columns", profile.columns)
    d.metric("Missing cells", profile.missing_cells)
    e.metric("Duplicate rows", profile.duplicate_rows)
    st.markdown(
        '<div class="note">The score is a transparent summary. Missing cells, duplicate rows and constant '
        "columns reduce it; the original data is never changed.</div>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("#### Column readiness")
        st.dataframe(analyzer.column_report(), width="stretch", hide_index=True)
    with right:
        st.markdown("#### Missing values by column")
        missing = analyzer.column_report().query("missing > 0")
        if missing.empty:
            st.success("No missing values were found.")
        else:
            figure = px.bar(
                missing,
                x="missing",
                y="column",
                orientation="h",
                color_discrete_sequence=["#0f766e"],
                labels={"missing": "Missing cells", "column": ""},
            )
            figure.update_layout(
                height=330,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="#fafafa",
                paper_bgcolor="#fafafa",
            )
            st.plotly_chart(figure, width="stretch")
    st.markdown("#### Data preview")
    st.dataframe(frame.head(12), width="stretch", hide_index=True)

with cleaning:
    st.subheader("Create a cleaned copy")
    st.write(
        "The original upload stays unchanged. Select simple, explainable operations and download the cleaned "
        "result as a new CSV file."
    )
    col1, col2 = st.columns(2)
    drop_duplicates = col1.checkbox("Remove duplicate rows", value=True)
    fill_missing = col2.checkbox(
        "Fill missing values",
        value=True,
        help="Numeric columns use the median. Other columns use the most common value.",
    )
    cleaned = analyzer.clean(drop_duplicates=drop_duplicates, fill_missing=fill_missing)
    cleaned_profile = DatasetAnalyzer(cleaned).profile()
    a, b, c = st.columns(3)
    a.metric("Rows after cleaning", len(cleaned), delta=len(cleaned) - len(frame))
    b.metric(
        "Missing cells",
        cleaned_profile.missing_cells,
        delta=cleaned_profile.missing_cells - profile.missing_cells,
    )
    c.metric(
        "Quality score",
        f"{cleaned_profile.quality_score}/100",
        delta=cleaned_profile.quality_score - profile.quality_score,
    )
    st.dataframe(cleaned.head(15), width="stretch", hide_index=True)
    st.download_button(
        "Download cleaned CSV",
        cleaned.to_csv(index=False).encode("utf-8"),
        file_name="tabulens_cleaned.csv",
        mime="text/csv",
        type="primary",
    )

with anomalies:
    st.subheader("Screen unusual numeric records")
    st.write(
        "Isolation Forest gives each row an anomaly score. A flagged row is a review suggestion, not proof that "
        "the record is wrong."
    )
    expected_percent = st.slider(
        "Expected unusual rows",
        min_value=1,
        max_value=15,
        value=5,
        step=1,
        format="%d%%",
    )
    contamination = expected_percent / 100
    try:
        anomaly_frame = analyzer.detect_anomalies(contamination=contamination)
        numeric = list(frame.select_dtypes(include="number").columns)
        x_column = st.selectbox("Horizontal axis", numeric, index=0)
        y_column = st.selectbox("Vertical axis", numeric, index=min(1, len(numeric) - 1))
        flagged = int(anomaly_frame["is_anomaly"].sum())
        st.metric("Rows suggested for review", flagged)
        figure = px.scatter(
            anomaly_frame,
            x=x_column,
            y=y_column,
            color="is_anomaly",
            color_discrete_map={False: "#a1a1aa", True: "#be123c"},
            hover_data=["anomaly_score"],
            labels={"is_anomaly": "Review"},
        )
        figure.update_layout(height=430, plot_bgcolor="#fafafa", paper_bgcolor="#fafafa")
        st.plotly_chart(figure, width="stretch")
        st.dataframe(anomaly_frame.head(12), width="stretch", hide_index=True)
    except ValueError as error:
        st.warning(str(error))

with learning:
    st.subheader("How the app works")
    st.markdown(
        """
        1. **Read the CSV:** Pandas converts the file into a DataFrame.
        2. **Profile the columns:** The app counts types, missing values, unique values and duplicates.
        3. **Create a cleaned copy:** Duplicate rows can be removed, numeric gaps use the median,
        and text gaps use the mode.
        4. **Screen anomalies:** Isolation Forest isolates records that differ from the majority of
        numeric observations.
        5. **Export the result:** The cleaned DataFrame is written back to CSV without modifying the uploaded file.
        """
    )
    st.markdown(
        '<p class="small">The quality score and anomaly flags are aids for review. They do not replace '
        "knowledge of the dataset or its subject.</p>",
        unsafe_allow_html=True,
    )
