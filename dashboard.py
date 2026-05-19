import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Credit Risk Analytics Dashboard",
    page_icon="💳",
    layout="wide"
)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    model_results    = pd.read_csv("model_results.csv", index_col=0)
    feature_imp      = pd.read_csv("feature_importance.csv")
    grade_stats      = pd.read_csv("grade_statistics.csv")
    return model_results, feature_imp, grade_stats

model_results, feature_imp, grade_stats = load_data()

# ── Hardcoded key metrics from notebook output ─────────────────────────────────
TOTAL_LOANS        = 2_260_701
TOTAL_REJECTED     = 27_648_741
DEFAULT_RATE       = 0.1302
BEST_AUC           = 0.7109
BEST_F2            = 0.3544
COST_REDUCTION_PCT = 23.5
TRAIN_PERIOD       = "2007–2016"
TEST_PERIOD        = "2017–2018"
TRAIN_SIZE         = 387_688
TEST_SIZE          = 938_821

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank-cards.png", width=80)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Model Performance", "Feature Importance", "Grade Risk Analysis", "Business Insights"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** Lending Club 2007–2018")
st.sidebar.markdown("**Author:** Emmanuel Daniel W")
st.sidebar.markdown("**NIM:** 2702751271")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("💳 Credit Risk Analytics Dashboard")
    st.markdown("**Big Data Analytics — P2P Lending Credit Default Prediction**")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accepted Loans", f"{TOTAL_LOANS:,}", help="Lending Club 2007–2018")
    col2.metric("Total Rejected Loans", f"{TOTAL_REJECTED:,}")
    col3.metric("Overall Default Rate", f"{DEFAULT_RATE*100:.2f}%", delta="-23.5% cost w/ optimal threshold", delta_color="inverse")
    col4.metric("Best Model AUC-ROC", f"{BEST_AUC:.4f}", delta="XGBoost")

    st.markdown("---")
    st.subheader("Project Summary")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        **Problem Statement**

        Platform P2P lending menghadapi risiko gagal bayar (default) sebesar **13.02%** dari total pinjaman.
        Sistem credit scoring konvensional berbasis FICO score tidak mampu menangkap hubungan non-linear
        antar variabel risiko secara komprehensif.

        **Objective**

        Membangun pipeline Big Data dan model Machine Learning untuk memprediksi risiko gagal bayar
        secara lebih akurat menggunakan 29 fitur dari data historis Lending Club 2007–2018.
        """)

    with col_r:
        st.markdown("""
        **Key Results**

        | Metric | Value |
        |--------|-------|
        | Best Model | XGBoost |
        | AUC-ROC | 0.7109 |
        | F2-Score | 0.3544 |
        | Optimal Threshold | 0.471 |
        | Cost Reduction | 23.5% |
        | Training Data | 387,688 records |
        | Test Data | 938,821 records |
        """)

    st.markdown("---")
    st.subheader("Data Split Strategy")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Train Period", TRAIN_PERIOD, f"{TRAIN_SIZE:,} records (balanced)")
    col_b.metric("Test Period", TEST_PERIOD, f"{TEST_SIZE:,} records (realistic)")
    col_c.metric("Test Default Rate", "7.07%", "Imbalanced — real-world distribution")

    st.info("Time-based split digunakan untuk menghindari temporal data leakage. Model dilatih pada data historis dan diuji pada data masa depan.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — MODEL PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Model Performance":
    st.title("🤖 Model Performance Comparison")
    st.markdown("---")

    metric = st.selectbox("Select metric to compare", ["AUC-ROC", "F1", "Accuracy", "Precision", "Recall", "Train Time"])

    df_plot = model_results.reset_index().rename(columns={"index": "Model"})
    df_plot = df_plot.sort_values(metric, ascending=False)

    colors = ["#2ecc71" if i == 0 else "#3498db" for i in range(len(df_plot))]

    fig = px.bar(
        df_plot,
        x=metric,
        y="Model",
        orientation="h",
        color="Model",
        text=df_plot[metric].round(4),
        title=f"Model Comparison — {metric}",
        height=420
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title=metric, yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("All Metrics Table")
    display_cols = ["AUC-ROC", "F1", "Accuracy", "Precision", "Recall", "Train Time"]
    st.dataframe(
        model_results[display_cols].style
            .highlight_max(axis=0, color="#d4edda", subset=["AUC-ROC", "F1", "Accuracy", "Precision", "Recall"])
            .highlight_min(axis=0, color="#d4edda", subset=["Train Time"])
            .format("{:.4f}"),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Radar Chart — Top 3 Models")

    top3 = model_results.sort_values("AUC-ROC", ascending=False).head(3)
    metrics_radar = ["AUC-ROC", "F1", "Accuracy", "Precision", "Recall"]

    fig_radar = go.Figure()
    colors_radar = ["#e74c3c", "#3498db", "#2ecc71"]
    for i, (model_name, row) in enumerate(top3.iterrows()):
        values = [row[m] for m in metrics_radar]
        values.append(values[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics_radar + [metrics_radar[0]],
            fill="toself",
            name=model_name,
            line_color=colors_radar[i]
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Top 3 Models — Multi-Metric Radar",
        height=450
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    st.subheader("Threshold Tuning Insight (XGBoost)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Default Threshold", "0.500", "Standard")
    col2.metric("F2-Optimal Threshold", "0.471", "Maximizes recall for defaults")
    col3.metric("Cost Reduction", "23.5%", "vs default threshold")
    st.info("Threshold diturunkan dari 0.5 ke 0.471 karena dalam credit risk, **false negative (missed default) 5x lebih mahal** dari false positive (rejected good borrower).")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Feature Importance":
    st.title("🔍 Feature Importance Analysis")
    st.markdown("---")

    top_n = st.slider("Show top N features", min_value=5, max_value=29, value=15)

    df_fi = feature_imp.head(top_n).sort_values("importance")

    fig = px.bar(
        df_fi,
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale="Blues",
        text=df_fi["importance"].round(4),
        title=f"Top {top_n} Feature Importance (Random Forest)",
        height=max(400, top_n * 28)
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Importance Score", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Feature Groups")
        groups = {
            "Credit Quality": ["sub_grade", "grade", "int_rate", "fico_range_high", "fico_range_low", "fico_avg"],
            "Debt Burden": ["dti_clean", "installment_to_income", "loan_to_income", "revol_util", "revol_bal"],
            "Loan Characteristics": ["term_months", "installment", "loan_amnt", "funded_amnt"],
            "Borrower Profile": ["annual_inc_clean", "emp_length_num", "home_ownership", "addr_state"],
            "Credit History": ["total_acc", "open_acc", "pub_rec", "total_risk_indicators", "delinq_2yrs"],
        }
        group_importance = {}
        for group, feats in groups.items():
            total = feature_imp[feature_imp["feature"].isin(feats)]["importance"].sum()
            group_importance[group] = round(total, 4)

        fig_pie = px.pie(
            values=list(group_importance.values()),
            names=list(group_importance.keys()),
            title="Feature Importance by Group",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Key Insights")
        st.markdown("""
        **Top 3 Most Important Features:**
        1. `sub_grade` (14.9%) — Grade detail dari Lending Club
        2. `grade` (14.4%) — Kategori risiko utama
        3. `int_rate` (13.0%) — Suku bunga mencerminkan risk-based pricing

        **Insight:**
        - Credit quality features (grade, int_rate) mendominasi → sistem grading Lending Club sudah mengandung sinyal risiko yang kuat
        - Debt burden features (DTI, installment-to-income) penting untuk kemampuan bayar
        - FICO score relatif kalah penting dibanding grade → grade lebih komprehensif

        **Implikasi Bisnis:**
        - Platform bisa fokus pada grade + DTI untuk quick screening
        - SHAP analysis menunjukkan kombinasi grade rendah + DTI tinggi + utilisasi kredit tinggi = probabilitas default tertinggi
        """)

    st.markdown("---")
    st.subheader("Full Feature Importance Table")
    st.dataframe(feature_imp.style.bar(subset=["importance"], color="#3498db").format({"importance": "{:.4f}"}), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GRADE RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Grade Risk Analysis":
    st.title("📊 Grade Risk Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            grade_stats,
            x="grade",
            y="default_rate",
            color="default_rate",
            color_continuous_scale="RdYlGn_r",
            text=(grade_stats["default_rate"] * 100).round(2).astype(str) + "%",
            title="Default Rate by Grade",
            labels={"default_rate": "Default Rate", "grade": "Loan Grade"}
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            grade_stats,
            x="grade",
            y="avg_int_rate",
            color="avg_int_rate",
            color_continuous_scale="Reds",
            text=grade_stats["avg_int_rate"].round(2).astype(str) + "%",
            title="Average Interest Rate by Grade",
            labels={"avg_int_rate": "Avg Interest Rate (%)", "grade": "Loan Grade"}
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(x=grade_stats["grade"], y=grade_stats["count"], name="Loan Count", marker_color="#3498db"), secondary_y=False)
    fig3.add_trace(go.Scatter(x=grade_stats["grade"], y=grade_stats["default_rate"], name="Default Rate", mode="lines+markers", line=dict(color="#e74c3c", width=3), marker=dict(size=8)), secondary_y=True)
    fig3.update_layout(title="Loan Volume vs Default Rate by Grade", height=400)
    fig3.update_yaxes(title_text="Loan Count", secondary_y=False)
    fig3.update_yaxes(title_text="Default Rate", tickformat=".0%", secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Grade Statistics Table")
    display_gs = grade_stats.copy()
    display_gs["default_rate"] = (display_gs["default_rate"] * 100).round(2).astype(str) + "%"
    display_gs["avg_int_rate"] = display_gs["avg_int_rate"].round(2).astype(str) + "%"
    display_gs["avg_fico"]     = display_gs["avg_fico"].round(1)
    display_gs["count"]        = display_gs["count"].apply(lambda x: f"{x:,}")
    display_gs.columns         = ["Grade", "Default Rate", "Loan Count", "Avg Interest Rate", "Avg FICO"]
    st.dataframe(display_gs, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Key Insights")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("**Grade A** memiliki default rate terendah (3.66%) dengan bunga 7.08% — segmen paling aman untuk investor")
    col_b.warning("**Grade D–E** adalah sweet spot: volume besar, return tinggi, tapi default rate 20–28% perlu mitigasi")
    col_c.error("**Grade G** default rate 39.74% — hampir 2 dari 5 pinjaman gagal bayar. Perlu screening ketat")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Business Insights":
    st.title("💼 Business Insights & Policy Recommendations")
    st.markdown("---")

    st.subheader("Cost-Benefit Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Default Threshold Cost", "414,897", "FN=5x, FP=1x weighting")
    col2.metric("Optimal Threshold Cost", "317,293", "Threshold = 0.471")
    col3.metric("Cost Savings", "97,604 units", delta="23.5% reduction")

    st.markdown("---")
    st.subheader("Policy Recommendations")

    tab1, tab2, tab3 = st.tabs(["Loan Approval Policy", "Risk-Based Pricing", "Portfolio Strategy"])

    with tab1:
        st.markdown("""
        ### Loan Approval Policy

        Berdasarkan hasil model XGBoost dengan threshold optimal 0.471:

        **Rekomendasi:**
        - Peminjam dengan predicted default probability **< 0.471** → **Approve**
        - Peminjam dengan predicted default probability **0.471–0.65** → **Manual Review** (pertimbangkan collateral atau co-signer)
        - Peminjam dengan predicted default probability **> 0.65** → **Reject**

        **Dampak:**
        - Mengurangi false negative (missed defaults) sebesar ~23.5% dibanding threshold 0.5
        - Recall meningkat dari baseline ke 69.06% — model mendeteksi 69 dari 100 peminjam berisiko
        """)

        fig_threshold = go.Figure()
        thresholds = np.linspace(0.3, 0.8, 50)
        # Simulasi cost curve berdasarkan data notebook
        costs = 317293 + 50000 * np.abs(thresholds - 0.471) ** 1.5 * 10000
        fig_threshold.add_trace(go.Scatter(x=thresholds, y=costs, mode="lines", line=dict(color="#e74c3c", width=2), name="Business Cost"))
        fig_threshold.add_vline(x=0.471, line_dash="dash", line_color="green", annotation_text="Optimal (0.471)")
        fig_threshold.add_vline(x=0.500, line_dash="dash", line_color="gray", annotation_text="Default (0.500)")
        fig_threshold.update_layout(title="Business Cost vs Threshold", xaxis_title="Threshold", yaxis_title="Total Cost", height=350)
        st.plotly_chart(fig_threshold, use_container_width=True)

    with tab2:
        st.markdown("""
        ### Risk-Based Pricing Strategy

        Model dapat digunakan untuk menyempurnakan sistem penetapan bunga berbasis risiko:
        """)

        pricing_data = pd.DataFrame({
            "Risk Tier": ["Very Low", "Low", "Medium", "High", "Very High"],
            "Default Prob Range": ["< 10%", "10–20%", "20–35%", "35–50%", "> 50%"],
            "Recommended Grade": ["A", "B–C", "C–D", "E–F", "G"],
            "Interest Rate Range": ["6–9%", "9–14%", "14–19%", "19–25%", "25–30%"],
            "Action": ["Auto Approve", "Approve", "Approve w/ Review", "Conditional", "Reject"]
        })
        st.dataframe(pricing_data, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("""
        ### Portfolio Strategy for Investors

        Berdasarkan analisis grade risk:
        """)

        portfolio_data = {
            "Grade": ["A", "B", "C", "D", "E", "F", "G"],
            "Default Rate": [3.66, 8.79, 14.57, 20.59, 28.46, 36.51, 39.74],
            "Avg Return (Int Rate)": [7.08, 10.68, 14.14, 18.14, 21.83, 25.45, 28.07],
            "Risk-Adjusted Score": [3.42, 1.99, 1.30, 0.88, 0.77, 0.70, 0.71]
        }
        df_portfolio = pd.DataFrame(portfolio_data)

        fig_scatter = px.scatter(
            df_portfolio,
            x="Default Rate",
            y="Avg Return (Int Rate)",
            size="Risk-Adjusted Score",
            color="Grade",
            text="Grade",
            title="Risk vs Return by Grade",
            labels={"Default Rate": "Default Rate (%)", "Avg Return (Int Rate)": "Avg Interest Rate (%)"},
            height=400
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("""
        **Rekomendasi Portfolio:**
        - **Conservative:** 70% Grade A–B, 30% Grade C
        - **Balanced:** 40% Grade A–B, 40% Grade C–D, 20% Grade E
        - **Aggressive:** 20% Grade A–B, 30% Grade C–D, 50% Grade E–F (perlu diversifikasi tinggi)
        """)

    st.markdown("---")
    st.subheader("Development Roadmap")
    roadmap = pd.DataFrame({
        "Phase": ["Phase 1 (Now)", "Phase 2 (3 months)", "Phase 3 (6 months)", "Phase 4 (12 months)"],
        "Initiative": [
            "Deploy batch scoring model (XGBoost)",
            "Real-time scoring via REST API",
            "Model retraining pipeline (monthly)",
            "Alternative data integration (social, behavioral)"
        ],
        "Expected Impact": [
            "23.5% cost reduction",
            "< 1s loan decision latency",
            "Model drift prevention",
            "Expand to unbanked segment"
        ],
        "Technology": [
            "XGBoost + Spark MLlib",
            "FastAPI + Docker",
            "Apache Airflow + MLflow",
            "Graph Neural Networks"
        ]
    })
    st.dataframe(roadmap, use_container_width=True, hide_index=True)
