# 1099 Quarterly Tax Planner

A Streamlit app for freelancers and independent contractors to estimate quarterly taxes, track business deductions, and manage weekly/monthly cash flow — all in one place.

---

## Features

- **Flexible income entry** — input by weekly pay or annual income
- **Business deductions** — mileage (2026 IRS rate), home office, tools, health insurance, professional services, and more
- **Tax estimates** — self-employment tax, federal income tax, and Arizona state tax
- **Quarterly payment calculator** — know exactly what to set aside each quarter
- **Weekly budget planner** — see your real spendable income after taxes and bills
- **Monthly bills ledger** — track recurring bills with due dates, auto-converted to a weekly reserve
- **Final totals** — annual, monthly, and weekly take-home at a glance

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/signa10perator/1099_tax_planner.git
cd 1099_tax_planner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Tax Assumptions

| Item | Value |
|------|-------|
| Mileage rate | $0.725 / mile (2026 IRS rate) |
| SE tax rate | 15.3% on 92.35% of net income |
| Standard deduction | $16,100 |
| Federal income tax | 12% flat estimate |
| Arizona state tax | 2.5% flat rate |

> These are estimates for planning purposes only. Consult a tax professional for advice specific to your situation.

---

## Deployment

This app is ready to deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) for free:

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the entry point
4. Deploy

---

## License

MIT
