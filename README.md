# 📊 Ad Campaign Performance Analytics Dashboard

> **A full-stack data analytics dashboard built with Python & Streamlit — analyzing 1,800+ global ad campaigns across platforms, industries, and countries to surface actionable marketing insights.**

🔗 **[Live Demo → Try it Now](https://adcampaignproject-zv64ginbqxbrkvf2yffdlj.streamlit.app/)**

---

## 🚀 What This Does

This dashboard takes raw ad campaign data and transforms it into a complete performance intelligence tool — the kind of report a media buyer or growth team would pay thousands for.

Upload your CSV and instantly get:

- ✅ KPI cards (ROAS, CTR, CPL, Total Spend, Revenue, Conversions)
- ✅ Platform-level ROAS comparison (Google Ads vs Meta vs TikTok)
- ✅ Campaign type CTR breakdown
- ✅ Spend vs Revenue by industry
- ✅ Country-wise ROAS heatmap
- ✅ Monthly ROAS trend line
- ✅ Automated insights & budget reallocation recommendations
- ✅ Drill-down data tables (by platform, campaign type, country, industry)
- ✅ Top 20 best-performing campaigns

---

## 📸 Dashboard Preview

| KPI Summary | ROAS by Platform |
|---|---|
| Account-level metrics at a glance | Compare Google, Meta & TikTok performance |

| Monthly Trend | Country ROAS Map |
|---|---|
| Track ROAS over time with target zone | Green = above avg · Red = below avg |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Dashboard | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualizations | Matplotlib |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

```
ad_campaign_project/
│
├── app.py                          # Main Streamlit dashboard
├── real_ad_analytics.py            # Original analytics script (CLI version)
├── requirements.txt                # Python dependencies
├── global_ads_performance_dataset.csv  # Sample dataset
└── README.md
```

---

## ⚡ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Ayesha037/ad_campaign_project.git
cd ad_campaign_project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch the dashboard**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

Upload your `global_ads_performance_dataset.csv` and the dashboard loads instantly.

---

## 📊 Dataset Schema

Your CSV should contain these columns:

| Column | Description |
|---|---|
| `date` | Campaign date |
| `platform` | Ad platform (Google Ads, Meta Ads, TikTok Ads) |
| `campaign_type` | Type of campaign (Brand Awareness, Retargeting, etc.) |
| `industry` | Industry vertical |
| `country` | Target country |
| `impressions` | Total impressions |
| `clicks` | Total clicks |
| `ad_spend` | Amount spent ($) |
| `conversions` | Total conversions |
| `revenue` | Revenue generated ($) |

---

## 🧮 KPIs Calculated Automatically

| Metric | Formula |
|---|---|
| **CTR** | `clicks / impressions × 100` |
| **ROAS** | `revenue / spend` |
| **CPL** | `spend / conversions` |
| **CPC** | `spend / clicks` |
| **Conversion Rate** | `conversions / clicks × 100` |

### Performance Labels (auto-tagged per campaign)
| Label | ROAS Threshold |
|---|---|
| 🟢 Excellent | ≥ 8.0x |
| 🔵 Strong | ≥ 4.0x |
| 🟡 Moderate | ≥ 2.0x |
| 🔴 Underperforming | < 2.0x |

---

## 💡 Insights Generated

The dashboard auto-generates recommendations like:

- **Best platform** by true ROAS → suggests where to scale budget
- **Worst platform** → flags where to cut spend
- **Top campaign type** → identifies highest-converting formats
- **Best performing country** → shows where to geo-target
- **Best industry** → reveals highest ROI vertical

---

## 🌐 Deployment

Deployed on **Streamlit Community Cloud** — free, fast, no server setup needed.

To deploy your own fork:
1. Push code to GitHub (must be public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub → select repo → set `app.py` as main file
4. Hit **Deploy** — live in ~2 minutes 🚀

---

## 📦 Dependencies

```
streamlit
pandas
numpy
matplotlib
openpyxl
```

---

## 👩‍💻 Author

**Ayesha** — [@Ayesha037](https://github.com/Ayesha037)

Built as part of a data analytics portfolio project covering end-to-end ad performance analysis across 1,800 global campaigns.

---

## ⭐ Show Some Love

If this helped you, drop a ⭐ on the repo — it means a lot!

---

*Built with Python · Powered by Streamlit · Deployed on the cloud*
