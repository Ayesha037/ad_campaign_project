
import pandas as pd                 
import numpy as np                   
import matplotlib.pyplot as plt      
import matplotlib.ticker as mticker 
from datetime import date           
import os                            
import warnings                      
warnings.filterwarnings("ignore")   
 
df = pd.read_csv("global_ads_performance_dataset.csv")


print("=" * 65)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 65)
print(f"  Total rows      : {len(df)}")                       
print(f"  Total columns   : {len(df.columns)}")              
print(f"  Platforms       : {', '.join(df['platform'].unique())}")
print(f"  Campaign types  : {', '.join(df['campaign_type'].unique())}")
print(f"  Industries      : {', '.join(df['industry'].unique())}")
print(f"  Countries       : {', '.join(df['country'].unique())}")
print(f"  Date range      : {df['date'].min()}  to  {df['date'].max()}")
print(f"  Missing values  : {df.isnull().sum().sum()}")      

df["date"] = pd.to_datetime(df["date"])


df.rename(columns={
    "ad_spend": "spend",  
    "CPA":      "cpa",     
    "CTR":      "ctr_raw", 
    "CPC":      "cpc_raw",
    "ROAS":     "roas_raw",
}, inplace=True)

df["ctr"] = (df["clicks"] / df["impressions"] * 100).round(2)


df["roas"] = (df["revenue"] / df["spend"]).round(2)


df["cpl"] = (df["spend"] / df["conversions"]).round(2)


df["cpc"] = (df["spend"] / df["clicks"]).round(2)


df["conversion_rate"] = (df["conversions"] / df["clicks"] * 100).round(2)


df["month"] = df["date"].dt.to_period("M")

print("\nKPIs calculated successfully: CTR, ROAS, CPL, CPC, Conversion Rate")


def performance_label(roas):
   
    if roas >= 8.0:
        return "Excellent"       
    elif roas >= 4.0:
        return "Strong"          
    elif roas >= 2.0:
        return "Moderate"         
    else:
        return "Underperforming" 


df["status"] = df["roas"].apply(performance_label)


status_counts = df["status"].value_counts()
print("\nPerformance distribution across 1800 campaigns:")
for status, count in status_counts.items():
    pct = round(count / len(df) * 100, 1)
    print(f"  {status:<20}: {count} campaigns ({pct}%)")



print("\n")
print("=" * 65)
print("PERFORMANCE BY PLATFORM")
print("=" * 65)


platform_summary = df.groupby("platform").agg(
    campaigns         = ("spend",           "count"),   
    total_spend       = ("spend",           "sum"),     
    total_revenue     = ("revenue",         "sum"),
    total_clicks      = ("clicks",          "sum"),
    total_impressions = ("impressions",     "sum"),
    total_conversions = ("conversions",     "sum"),
    avg_roas          = ("roas",            "mean"),   
    avg_ctr           = ("ctr",             "mean"),
    avg_cpl           = ("cpl",             "mean"),
).round(2)


platform_summary["true_roas"] = (
    platform_summary["total_revenue"] / platform_summary["total_spend"]
).round(2)

print(platform_summary[["campaigns","total_spend","total_revenue","true_roas","avg_ctr","avg_cpl"]].to_string())


print("\n")
print("=" * 65)
print("PERFORMANCE BY CAMPAIGN TYPE")
print("=" * 65)

campaign_summary = df.groupby("campaign_type").agg(
    total_spend       = ("spend",       "sum"),
    total_revenue     = ("revenue",     "sum"),
    total_conversions = ("conversions", "sum"),
    avg_roas          = ("roas",        "mean"),
    avg_ctr           = ("ctr",         "mean"),
    avg_cpl           = ("cpl",         "mean"),
).round(2)

campaign_summary = campaign_summary.sort_values("avg_roas", ascending=False)
print(campaign_summary.to_string())

print("\n")
print("=" * 65)
print("PERFORMANCE BY COUNTRY")
print("=" * 65)

country_summary = df.groupby("country").agg(
    total_spend   = ("spend",   "sum"),
    total_revenue = ("revenue", "sum"),
    avg_roas      = ("roas",    "mean"),
    avg_ctr       = ("ctr",     "mean"),
    avg_cpl       = ("cpl",     "mean"),
).round(2)

country_summary["true_roas"] = (
    country_summary["total_revenue"] / country_summary["total_spend"]
).round(2)

country_summary = country_summary.sort_values("true_roas", ascending=False)
print(country_summary[["total_spend","total_revenue","true_roas","avg_ctr","avg_cpl"]].to_string())

print("\n")
print("=" * 65)
print("PERFORMANCE BY INDUSTRY")
print("=" * 65)

industry_summary = df.groupby("industry").agg(
    total_spend       = ("spend",       "sum"),
    total_revenue     = ("revenue",     "sum"),
    avg_roas          = ("roas",        "mean"),
    avg_ctr           = ("ctr",         "mean"),
    avg_cpl           = ("cpl",         "mean"),
    total_conversions = ("conversions", "sum"),
).round(2)

industry_summary = industry_summary.sort_values("avg_roas", ascending=False)
print(industry_summary.to_string())

print("\n")
print("=" * 65)
print("MONTHLY TREND — ROAS & SPEND")
print("=" * 65)

monthly = df.groupby("month").agg(
    total_spend   = ("spend",   "sum"),
    total_revenue = ("revenue", "sum"),
    avg_roas      = ("roas",    "mean"),
    avg_ctr       = ("ctr",     "mean"),
).round(2)

monthly.index = monthly.index.astype(str)
print(monthly.to_string())

print("\n")
print("=" * 65)
print("AUTOMATED INSIGHTS & RECOMMENDATIONS")
print("=" * 65)

total_spend       = df["spend"].sum()
total_revenue     = df["revenue"].sum()
total_conversions = df["conversions"].sum()
overall_roas      = round(total_revenue / total_spend, 2)
overall_ctr       = round(df["clicks"].sum() / df["impressions"].sum() * 100, 2)
overall_cpl       = round(total_spend / total_conversions, 2)

print(f"\n ACCOUNT SUMMARY:")
print(f"   Total Spend       : ${total_spend:,.0f}")
print(f"   Total Revenue     : ${total_revenue:,.0f}")
print(f"   Overall ROAS      : {overall_roas}x")
print(f"   Overall CTR       : {overall_ctr}%")
print(f"   Total Conversions : {total_conversions:,}")
print(f"   Avg CPL           : ${overall_cpl:,.2f}")

best_platform  = platform_summary["true_roas"].idxmax()   
worst_platform = platform_summary["true_roas"].idxmin()   

print(f"\n PLATFORM INSIGHTS:")
print(f"   Best platform  : {best_platform} (ROAS: {platform_summary.loc[best_platform, 'true_roas']}x)")
print(f"   Worst platform : {worst_platform} (ROAS: {platform_summary.loc[worst_platform, 'true_roas']}x)")
print(f"   Recommendation : Shift budget from {worst_platform} → {best_platform}")

best_type  = campaign_summary["avg_roas"].idxmax()
worst_type = campaign_summary["avg_roas"].idxmin()
print(f"\n CAMPAIGN TYPE INSIGHTS:")
print(f"   Best type  : {best_type} (avg ROAS: {campaign_summary.loc[best_type, 'avg_roas']}x)")
print(f"   Worst type : {worst_type} (avg ROAS: {campaign_summary.loc[worst_type, 'avg_roas']}x)")

best_country  = country_summary["true_roas"].idxmax()
worst_country = country_summary["true_roas"].idxmin()
print(f"\n COUNTRY INSIGHTS:")
print(f"   Highest ROAS country : {best_country} ({country_summary.loc[best_country, 'true_roas']}x)")
print(f"   Lowest ROAS country  : {worst_country} ({country_summary.loc[worst_country, 'true_roas']}x)")

best_industry = industry_summary["avg_roas"].idxmax()
print(f"\n INDUSTRY INSIGHTS:")
print(f"   Best industry : {best_industry} (avg ROAS: {industry_summary.loc[best_industry, 'avg_roas']}x)")


os.makedirs("ad_analytics_output", exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")   

platform_colors = {
    "Google Ads": "#185FA5",   
    "TikTok Ads": "#2D9E75",  
    "Meta Ads":   "#993C1D",   
}

fig, ax = plt.subplots(figsize=(8, 5))

platforms  = platform_summary.index.tolist()          
roas_vals  = platform_summary["true_roas"].tolist()   
colors     = [platform_colors.get(p, "#888") for p in platforms] 

bars = ax.bar(platforms, roas_vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5)

for bar, val in zip(bars, roas_vals):
    
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,             
            f"{val}x",                         
            ha="center", va="bottom",         
            fontsize=12, fontweight="bold")


ax.axhline(y=4, color="red", linestyle="--", linewidth=1.2, label="Benchmark (4x ROAS)")
ax.set_ylabel("ROAS (Return on Ad Spend)")
ax.set_title("ROAS by Platform", fontweight="bold", fontsize=14)
ax.legend()
ax.set_ylim(0, max(roas_vals) * 1.25)    
plt.tight_layout()
plt.savefig("ad_analytics_output/chart1_roas_by_platform.png", dpi=150)
plt.close()   
print("\nChart 1 saved: ROAS by Platform")


fig, ax = plt.subplots(figsize=(8, 5))

camp_ctr = campaign_summary["avg_ctr"].sort_values(ascending=True)

ax.barh(camp_ctr.index, camp_ctr.values, color="#185FA5", edgecolor="white")

for i, val in enumerate(camp_ctr.values):
    ax.text(val + 0.02, i, f"{val}%", va="center", fontsize=10)

ax.set_xlabel("Average CTR (%)")
ax.set_title("Click-Through Rate by Campaign Type", fontweight="bold", fontsize=14)
ax.axvline(x=camp_ctr.mean(), color="orange", linestyle="--",
           label=f"Average ({camp_ctr.mean():.2f}%)")
ax.legend()
plt.tight_layout()
plt.savefig("ad_analytics_output/chart2_ctr_by_campaign_type.png", dpi=150)
plt.close()
print("Chart 2 saved: CTR by Campaign Type")

fig, ax = plt.subplots(figsize=(10, 5))

industries = industry_summary.index.tolist()
x = np.arange(len(industries))   
width = 0.35                 

bars1 = ax.bar(x - width/2, industry_summary["total_spend"],   width,
               label="Total Spend",   color="#AACBE8", edgecolor="white")
bars2 = ax.bar(x + width/2, industry_summary["total_revenue"], width,
               label="Total Revenue", color="#185FA5", edgecolor="white")

def money_fmt(x, pos):
    
    if x >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    elif x >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"

ax.yaxis.set_major_formatter(mticker.FuncFormatter(money_fmt))

ax.set_xticks(x)
ax.set_xticklabels(industries, rotation=20, ha="right", fontsize=10)
ax.set_title("Spend vs Revenue by Industry", fontweight="bold", fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig("ad_analytics_output/chart3_spend_vs_revenue_industry.png", dpi=150)
plt.close()
print("Chart 3 saved: Spend vs Revenue by Industry")

fig, ax = plt.subplots(figsize=(9, 5))

country_roas = country_summary["true_roas"].sort_values(ascending=False)

avg_roas = country_roas.mean()
bar_colors = ["#2D9E75" if v >= avg_roas else "#993C1D" for v in country_roas.values]

bars = ax.bar(country_roas.index, country_roas.values, color=bar_colors,
              edgecolor="white", linewidth=1)

for bar, val in zip(bars, country_roas.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            f"{val}x", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.axhline(y=avg_roas, color="navy", linestyle="--", linewidth=1.2,
           label=f"Average ROAS ({avg_roas:.2f}x)")
ax.set_ylabel("ROAS")
ax.set_title("ROAS by Country  (green = above avg, red = below avg)",
             fontweight="bold", fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig("ad_analytics_output/chart4_roas_by_country.png", dpi=150)
plt.close()
print("Chart 4 saved: ROAS by Country")

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(monthly.index, monthly["avg_roas"],
        marker="o",          
        linewidth=2,
        color="#185FA5",
        markersize=6,
        label="Avg ROAS")

ax.axhspan(4, 8, alpha=0.08, color="green", label="Target zone (4–8x)")

ax.set_xlabel("Month")
ax.set_ylabel("Average ROAS")
ax.set_title("Monthly ROAS Trend", fontweight="bold", fontsize=14)

plt.xticks(rotation=45, ha="right", fontsize=8)
ax.legend()
plt.tight_layout()
plt.savefig("ad_analytics_output/chart5_monthly_roas_trend.png", dpi=150)
plt.close()
print("Chart 5 saved: Monthly ROAS Trend")


today      = date.today().strftime("%Y-%m-%d")
excel_path = f"ad_analytics_output/ad_performance_report_{today}.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

    df[["date","platform","campaign_type","industry","country",
        "impressions","clicks","ctr","spend","cpc","conversions",
        "cpl","conversion_rate","revenue","roas","status"]].to_excel(
        writer, sheet_name="Full Data", index=False
    )

    platform_summary.to_excel(writer, sheet_name="By Platform")

    campaign_summary.to_excel(writer, sheet_name="By Campaign Type")

    country_summary.to_excel(writer, sheet_name="By Country")

    industry_summary.to_excel(writer, sheet_name="By Industry")

    monthly.to_excel(writer, sheet_name="Monthly Trend")

    top20 = df.nlargest(20, "roas")[["date","platform","campaign_type",
                                      "industry","country","spend",
                                      "revenue","roas","ctr","cpl","status"]]
    top20.to_excel(writer, sheet_name="Top 20 by ROAS", index=False)

print(f"\nExcel report saved: {excel_path}")

print("\n")
print("=" * 65)
print("ANALYSIS COMPLETE")
print("=" * 65)
print(f"  Rows analysed    : {len(df):,}")
print(f"  Charts generated : 5")
print(f"  Excel sheets     : 7")
print(f"  Output folder    : ad_analytics_output/")
print(f"  Report file      : ad_performance_report_{today}.xlsx")
print("=" * 65)