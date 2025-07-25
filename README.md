# 💳 Digital Lending Funnel Simulation & Analysis

This project simulates and analyzes the **end-to-end user journey in a digital lending product**, from website visit to loan disbursement (funded). The dataset is fully synthetic, but modeled to reflect realistic user behavior, application stages, dropouts, and fraud patterns.

---

## 🧩 Project Summary

- **70,000 synthetic users**
- Simulated full customer lifecycle:
  - from first visit → started → submitted → verified → approved → funded
  - with rejection, expiration, cancellation events
- Modeled:
  - Retention (repeat applications)
  - Delays between stages
  - Fraud users & scoring
  - Acquisition channels & geographies
  - Credit score segmentation
- Built a comprehensive **interactive dashboard in Tableau**

---

## 📊 Dashboard Highlights (Tableau)

🔗 **[Open Dashboard on Tableau Public →](https://public.tableau.com/app/profile/nikita.metelkin/viz/FINSTARTNEW/Dashboard1?publish=yes)**

- **Funnel Analysis** — visual breakdown of each user stage
- **Conversion by Channel** — best: Referral (>33%), worst: Facebook (~11%)
- **Drop-off Reasons** — most users drop at `submitted → verified`
- **Retention** — only ~20% take a 2nd loan; steep drop after
- **Stage Delays** — longest bottleneck: `approved → funded`

---

## 💡 Key Insights

- ⚠️ Largest drop occurs between **submitted → verified**, likely due to ID/document issues or low credit score.
- 📈 **Referral traffic** converts best, Facebook Ads worst — potential mismatch in targeting.
- 🧲 Retention drops sharply after 2nd loan — possible opportunity for loyalty programs or personalized offers.
- ⏳ Delays between approved → funded highlight a backend/process bottleneck — may need integration improvement.

---

## 🔍 Why This Matters

The goal was to create a **realistic simulation of a lending funnel** — not just perfect data, but realistic issues:

- Delays in loan approval or funding
- Real conversion losses across funnel
- Channels with varying ROI

This setup allows for:
- Funnel optimization
- Growth opportunity discovery
- Retention & cohort analysis
- Channel efficiency analysis

---

## 🛠️ Tools & Technologies

- **Python** — data simulation, session logic
- **Tableau** — dashboards (funnel, drop-off, retention, conversion)
- **Pandas, NumPy** — data wrangling
- **Matplotlib, Seaborn** — EDA, plots

---

## ✍️ Author

Nikita Metelkin  
Data Analyst | Python, SQL, A/B Testing, BI  
[LinkedIn](https://www.linkedin.com/in/nikita-metelkin-40233326b/) • [Telegram](https://t.me/MetelkinNikita)
