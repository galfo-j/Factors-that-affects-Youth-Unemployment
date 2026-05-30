# 📊 SDG 8 — Youth Unemployment Dashboard
---

## 🎯 Research Question

> **"What macroeconomic and structural factors influence Youth Unemployment Rates across countries over time?"**

---
---

## 📦 Dataset

| Attribute       | Details                                      |
|----------------|----------------------------------------------|
| **Source**      | World Bank — World Development Indicators (WDI) |
| **Region**      | East Asia & Pacific                          |
| **Period**      | 2014 – 2024                                  |
| **Countries**   | 29                                           |
| **Records**     | 319 (after cleaning)                         |

### Variables

| Role | Indicator | World Bank Code |
|------|-----------|----------------|
| **Response (Y)** | Youth Unemployment Rate (% of labour force ages 15–24) | `SL.UEM.1524.ZS` |
| **Predictor (X₁)** | Annual GDP Growth (%) | `NY.GDP.MKTP.KD.ZG` |
| **Predictor (X₂)** | Labour Force Participation Rate, Total (%) | `SL.TLF.CACT.ZS` |
| **Predictor (X₃)** | Access to Electricity (% of population) | `EG.ELC.ACCS.ZS` |

---

## 🗂️ Dashboard Pages

### 📈 Dashboard Overview
The landing page. Displays dataset-level quick stats, regional highlights (average youth unemployment, average GDP growth, highest-unemployment country), and a **country selector** for individual analysis. Per-country charts include a youth unemployment trend, GDP growth bar chart, and a GDP vs unemployment scatter plot.

### 🌏 Country Comparison
Compare up to 10 countries simultaneously on any indicator. Includes a **multi-line trend chart**, a **ranked data table** with conditional color-coding, and a **bar chart** for the selected year.

### 📉 Trend Analysis
Deep-dive into a single metric for a chosen country or the regional average. Annotates peak and low years, computes the **overall change** and **volatility (std dev)**, and shows a **year-over-year change bar chart**.

### 🔮 Unemployment Forecasting
Uses **Simple Linear Regression** on a country's historical data to project youth unemployment up to 5 years ahead. Displays R², MAE, a forecast chart with optional prediction interval bands, a projection table, and a plain-language summary.

### 📐 Regression Insights
Presents the full **OLS (Ordinary Least Squares)** model results: coefficient table, model fit statistics (R², Adjusted R², F-statistic), key finding cards per variable, the regression equation, a coefficient comparison bar chart, and an interpretive conclusion.

---

### 🔗 Link
_https://factors-that-affects-youth-unemployment.streamlit.app/_



