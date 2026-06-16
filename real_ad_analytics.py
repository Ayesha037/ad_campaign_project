import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Ad Campaign Analytics", layout="wide", page_icon="📊")

st.title("📊 Ad Campaign Performance Dashboard")
st.markdown("---")

# ── File Upload ──────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is None:
    st.info("👆 Please upload your `global_ads_performance_dataset.csv` to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ── Data Prep ─────────────────────────────────────────────────────────────────
df["date"] = pd.to_datetime(df["date"])

df.rename(columns={
    "ad_spend": "spend",
    "CPA":      "cpa",
    "CTR":      "ctr_raw",
    "CPC":      "cpc_raw",
    "ROAS":     "roas_raw",
}, inplace=True)

df["ctr"]             = (df["clicks"] / df["impressions"] * 100).round(2)
df["roas"]            = (df["revenue"] / df["spend"]).round(2)
df["cpl"]             = (df["spend"] / df["conversions"]).round(2)
df["cpc"]             = (df["spend"] / df["clicks"]).round(2)
df["conversion_rate"] = (df["conversions"] / df["clicks"] * 100).round(2)
df["month"]           = df["date"].dt.to_period("M")

def performance_label(roas):
    if roas >= 8.0:   return "Excellent"
    elif roas >= 4.0: return "Strong"
    elif roas >= 2.0: return "Moderate"
    else:             return "Underperforming"

df["status"] = df["roas"].apply(performance_label)

# ── Summaries ────────────────────────────────────────────────────────────────
platform_summary = df.groupby("platform").agg(
    campaigns         = ("spend",       "count"),
    total_spend       = ("spend",       "sum"),
    total_revenue     = ("revenue",     "sum"),
    total_clicks      = ("clicks",      "sum"),
    total_impressions = ("impressions", "sum"),
    total_conversions = ("conversions", "sum"),
    avg_roas          = ("roas",        "mean"),
    avg_ctr           = ("ctr",         "mean"),
    avg_cpl           = ("cpl",         "mean"),
).round(2)
platform_summary["true_roas"] = (platform_summary["total_revenue"] / platform_summary["total_spend"]).round(2)

campaign_summary = df.groupby("campaign_type").agg(
    total_spend       = ("spend",       "sum"),
    total_revenue     = ("revenue",     "sum"),
    total_conversions = ("conversions", "sum"),
    avg_roas          = ("roas",        "mean"),
    avg_ctr           = ("ctr",         "mean"),
    avg_cpl           = ("cpl",         "mean"),
).round(2).sort_values("avg_roas", ascending=False)

country_summary = df.groupby("country").agg(
    total_spend   = ("spend",   "sum"),
    total_revenue = ("revenue", "sum"),
    avg_roas      = ("roas",    "mean"),
    avg_ctr       = ("ctr",     "mean"),
    avg_cpl       = ("cpl",     "mean"),
).round(2)
country_summary["true_roas"] = (country_summary["total_revenue"] / country_summary["total_spend"]).round(2)
country_summary = country_summary.sort_values("true_roas", ascending=False)

industry_summary = df.groupby("industry").agg(
    total_spend       = ("spend",       "sum"),
    total_revenue     = ("revenue",     "sum"),
    avg_roas          = ("roas",        "mean"),
    avg_ctr           = ("ctr",         "mean"),
    avg_cpl           = ("cpl",         "mean"),
    total_conversions = ("conversions", "sum"),
).round(2).sort_values("avg_roas", ascending=False)

monthly = df.groupby("month").agg(
    total_spend   = ("spend",   "sum"),
    total_revenue = ("revenue", "sum"),
    avg_roas      = ("roas",    "mean"),
    avg_ctr       = ("ctr",     "mean"),
).round(2)
monthly.index = monthly.index.astype(str)

# ── KPI Cards ────────────────────────────────────────────────────────────────
total_spend       = df["spend"].sum()
total_revenue     = df["revenue"].sum()
total_conversions = df["conversions"].sum()
overall_roas      = round(total_revenue / total_spend, 2)
overall_ctr       = round(df["clicks"].sum() / df["impressions"].sum() * 100, 2)
overall_cpl       = round(total_spend / total_conversions, 2)

st.subheader("📈 Account Summary")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Spend",       f"${total_spend:,.0f}")
c2.metric("Total Revenue",     f"${total_revenue:,.0f}")
c3.metric("Overall ROAS",      f"{overall_roas}x")
c4.metric("Overall CTR",       f"{overall_ctr}%")
c5.metric("Total Conversions", f"{total_conversions:,}")
c6.metric("Avg CPL",           f"${overall_cpl:,.2f}")

st.markdown("---")

# ── Style ─────────────────────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
platform_colors = {
    "Google Ads": "#185FA5",
    "TikTok Ads": "#2D9E75",
    "Meta Ads":   "#993C1D",
}

# ── Chart 1: ROAS by Platform ─────────────────────────────────────────────────
st.subheader("📊 ROAS by Platform")
fig1, ax1 = plt.subplots(figsize=(8, 5))
platforms = platform_summary.index.tolist()
roas_vals = platform_summary["true_roas"].tolist()
colors    = [platform_colors.get(p, "#888") for p in platforms]
bars = ax1.bar(platforms, roas_vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars, roas_vals):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
             f"{val}x", ha="center", va="bottom", fontsize=12, fontweight="bold")
ax1.axhline(y=4, color="red", linestyle="--", linewidth=1.2, label="Benchmark (4x ROAS)")
ax1.set_ylabel("ROAS")
ax1.set_title("ROAS by Platform", fontweight="bold", fontsize=14)
ax1.legend()
ax1.set_ylim(0, max(roas_vals) * 1.25)
plt.tight_layout()
st.pyplot(fig1)

# ── Chart 2: CTR by Campaign Type ────────────────────────────────────────────
st.subheader("🖱️ CTR by Campaign Type")
fig2, ax2 = plt.subplots(figsize=(8, 5))
camp_ctr = campaign_summary["avg_ctr"].sort_values(ascending=True)
ax2.barh(camp_ctr.index, camp_ctr.values, color="#185FA5", edgecolor="white")
for i, val in enumerate(camp_ctr.values):
    ax2.text(val + 0.02, i, f"{val}%", va="center", fontsize=10)
ax2.set_xlabel("Average CTR (%)")
ax2.set_title("Click-Through Rate by Campaign Type", fontweight="bold", fontsize=14)
ax2.axvline(x=camp_ctr.mean(), color="orange", linestyle="--",
            label=f"Average ({camp_ctr.mean():.2f}%)")
ax2.legend()
plt.tight_layout()
st.pyplot(fig2)

# ── Chart 3: Spend vs Revenue by Industry ────────────────────────────────────
st.subheader("🏭 Spend vs Revenue by Industry")
fig3, ax3 = plt.subplots(figsize=(10, 5))
industries = industry_summary.index.tolist()
x     = np.arange(len(industries))
width = 0.35
ax3.bar(x - width/2, industry_summary["total_spend"],   width, label="Total Spend",   color="#AACBE8", edgecolor="white")
ax3.bar(x + width/2, industry_summary["total_revenue"], width, label="Total Revenue", color="#185FA5", edgecolor="white")

def money_fmt(x, pos):
    if x >= 1_000_000: return f"${x/1_000_000:.1f}M"
    elif x >= 1_000:   return f"${x/1_000:.0f}K"
    return f"${x:.0f}"

ax3.yaxis.set_major_formatter(mticker.FuncFormatter(money_fmt))
ax3.set_xticks(x)
ax3.set_xticklabels(industries, rotation=20, ha="right", fontsize=10)
ax3.set_title("Spend vs Revenue by Industry", fontweight="bold", fontsize=14)
ax3.legend()
plt.tight_layout()
st.pyplot(fig3)

# ── Chart 4: ROAS by Country ──────────────────────────────────────────────────
st.subheader("🌍 ROAS by Country")
fig4, ax4 = plt.subplots(figsize=(9, 5))
country_roas = country_summary["true_roas"].sort_values(ascending=False)
avg_roas_c   = country_roas.mean()
bar_colors   = ["#2D9E75" if v >= avg_roas_c else "#993C1D" for v in country_roas.values]
bars4 = ax4.bar(country_roas.index, country_roas.values, color=bar_colors, edgecolor="white")
for bar, val in zip(bars4, country_roas.values):
    ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f"{val}x", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax4.axhline(y=avg_roas_c, color="navy", linestyle="--",
            label=f"Average ROAS ({avg_roas_c:.2f}x)")
ax4.set_ylabel("ROAS")
ax4.set_title("ROAS by Country  (green = above avg, red = below avg)", fontweight="bold", fontsize=13)
ax4.legend()
plt.tight_layout()
st.pyplot(fig4)

# ── Chart 5: Monthly ROAS Trend ───────────────────────────────────────────────
st.subheader("📅 Monthly ROAS Trend")
fig5, ax5 = plt.subplots(figsize=(11, 5))
ax5.plot(monthly.index, monthly["avg_roas"], marker="o", linewidth=2,
         color="#185FA5", markersize=6, label="Avg ROAS")
ax5.axhspan(4, 8, alpha=0.08, color="green", label="Target zone (4–8x)")
ax5.set_xlabel("Month")
ax5.set_ylabel("Average ROAS")
ax5.set_title("Monthly ROAS Trend", fontweight="bold", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=8)
ax5.legend()
plt.tight_layout()
st.pyplot(fig5)

st.markdown("---")

# ── Insights ──────────────────────────────────────────────────────────────────
st.subheader("💡 Automated Insights & Recommendations")

best_platform  = platform_summary["true_roas"].idxmax()
worst_platform = platform_summary["true_roas"].idxmin()
best_type      = campaign_summary["avg_roas"].idxmax()
worst_type     = campaign_summary["avg_roas"].idxmin()
best_country   = country_summary["true_roas"].idxmax()
worst_country  = country_summary["true_roas"].idxmin()
best_industry  = industry_summary["avg_roas"].idxmax()

col1, col2 = st.columns(2)
with col1:
    st.info(f"**🏆 Best Platform:** {best_platform} (ROAS: {platform_summary.loc[best_platform, 'true_roas']}x)\n\n"
            f"**⚠️ Worst Platform:** {worst_platform} (ROAS: {platform_summary.loc[worst_platform, 'true_roas']}x)\n\n"
            f"**💡 Tip:** Shift budget from {worst_platform} → {best_platform}")
    st.info(f"**🏆 Best Campaign Type:** {best_type} (ROAS: {campaign_summary.loc[best_type, 'avg_roas']}x)\n\n"
            f"**⚠️ Worst Campaign Type:** {worst_type} (ROAS: {campaign_summary.loc[worst_type, 'avg_roas']}x)")
with col2:
    st.info(f"**🌍 Highest ROAS Country:** {best_country} ({country_summary.loc[best_country, 'true_roas']}x)\n\n"
            f"**🌍 Lowest ROAS Country:** {worst_country} ({country_summary.loc[worst_country, 'true_roas']}x)")
    st.info(f"**🏭 Best Industry:** {best_industry} (avg ROAS: {industry_summary.loc[best_industry, 'avg_roas']}x)")

st.markdown("---")

# ── Data Tables ───────────────────────────────────────────────────────────────
st.subheader("📋 Detailed Tables")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["By Platform", "By Campaign Type", "By Country", "By Industry", "Monthly Trend"])
with tab1: st.dataframe(platform_summary)
with tab2: st.dataframe(campaign_summary)
with tab3: st.dataframe(country_summary)
with tab4: st.dataframe(industry_summary)
with tab5: st.dataframe(monthly)

# ── Top 20 ────────────────────────────────────────────────────────────────────
st.subheader("🥇 Top 20 Campaigns by ROAS")
top20 = df.nlargest(20, "roas")[["date","platform","campaign_type","industry",
                                  "country","spend","revenue","roas","ctr","cpl","status"]]
st.dataframe(top20)

st.markdown("---")
st.caption(f"Analysis complete · {len(df):,} rows · 5 charts · Report date: {date.today()}")