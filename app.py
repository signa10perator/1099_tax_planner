import streamlit as st
from datetime import date

st.set_page_config(
    page_title="1099 Quarterly Tax Planner",
    layout="wide"
)

# =========================
# ART DECO CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Josefin+Sans:wght@300;400;600;700&display=swap');

/* BASE */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #0a0a08 !important;
    color: #e8dfc8;
    font-family: 'Josefin Sans', sans-serif;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2.5rem;
    max-width: 1100px;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
footer, #MainMenu {
    display: none !important;
}

/* TITLE */
h1 {
    font-family: 'Cinzel', serif !important;
    color: #c8a84c !important;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #c8a84c;
    margin-bottom: 0.25rem !important;
}

/* SECTION HEADERS */
h2 {
    font-family: 'Cinzel', serif !important;
    color: #c8a84c !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    border-left: 3px solid #c8a84c;
    padding-left: 0.75rem;
    margin-top: 0.25rem !important;
}

h3 {
    font-family: 'Josefin Sans', sans-serif !important;
    color: #7a6e48 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
}

/* DIVIDERS */
hr {
    border: none !important;
    border-top: 1px solid #1e1c12 !important;
    margin: 1.75rem 0 !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: #0f0f0a !important;
    border: 1px solid #1e1c12 !important;
    border-left: 3px solid #c8a84c !important;
    padding: 1rem 1.25rem !important;
    border-radius: 0 !important;
}

[data-testid="stMetricLabel"] p {
    color: #5a5030 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] div {
    color: #c8a84c !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
    letter-spacing: 0.03em;
}

/* LABELS */
label {
    color: #5a5030 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
}

/* INPUTS */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background-color: #0f0f0a !important;
    border: none !important;
    border-bottom: 1px solid #2e2a18 !important;
    border-radius: 0 !important;
    color: #e8dfc8 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em;
    padding: 0.4rem 0 !important;
}

[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-bottom: 1px solid #c8a84c !important;
    box-shadow: none !important;
}

/* BUTTONS */
.stButton > button {
    background-color: transparent !important;
    border: 1px solid #c8a84c !important;
    color: #c8a84c !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    border-radius: 0 !important;
    transition: all 0.15s ease !important;
    padding: 0.45rem 1.2rem !important;
}

.stButton > button:hover {
    background-color: #c8a84c !important;
    color: #0a0a08 !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background-color: #0d0d09 !important;
    border: 1px solid #1e1c12 !important;
    border-radius: 0 !important;
}

[data-testid="stExpander"] summary span p {
    color: #7a6e48 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    background-color: #0f0f0a !important;
    border: 1px solid #1e1c12 !important;
    border-left: 3px solid #c8a84c !important;
    color: #7a6e48 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em;
}

/* CAPTION */
[data-testid="stCaptionContainer"] p {
    color: #2e2a18 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-size: 0.55rem !important;
}

/* CHECK HISTORY TABLE */
.deco-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Josefin Sans', sans-serif;
    margin-top: 0.75rem;
}

.deco-table thead tr {
    border-bottom: 1px solid #c8a84c;
}

.deco-table th {
    color: #c8a84c;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 0 0.5rem 0.6rem 0;
    text-align: left;
}

.deco-table td {
    border-bottom: 1px solid #141410;
    color: #e8dfc8;
    padding: 0.7rem 0.5rem 0.7rem 0;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
}

.deco-table tr:last-child td { border-bottom: none; }
.deco-table .col-date  { color: #5a5030; font-size: 0.75rem; letter-spacing: 0.06em; }
.deco-table .col-check { color: #c8a84c; font-weight: 600; }
.deco-table .col-tax   { color: #7a6e48; }
.deco-table .col-keep  { color: #e8dfc8; }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "monthly_bills" not in st.session_state:
    st.session_state.monthly_bills = []

if "checks" not in st.session_state:
    st.session_state.checks = []

monthly_bills_total = sum(b["amount"] for b in st.session_state.monthly_bills)
weekly_monthly_bill_reserve = monthly_bills_total * 12 / 52

# =========================
# TAX HELPER
# =========================

def compute_check_taxes(amount):
    se_weekly = amount * 0.9235 * 0.153

    annual = amount * 52
    se_annual = se_weekly * 52
    half_se = se_annual / 2
    fed_taxable = max(annual - half_se - 16100, 0)
    fed_weekly = (fed_taxable * 0.12) / 52

    state_weekly = amount * 0.025

    total = se_weekly + fed_weekly + state_weekly
    return se_weekly, fed_weekly, state_weekly, total

# =========================
# INCOME
# =========================

st.title("1099 Quarterly Tax Planner")

st.divider()

st.header("Income")

col_in1, col_in2, col_in3 = st.columns([3, 3, 1])

with col_in1:
    check_amount = st.number_input(
        "Weekly Check",
        min_value=0.0,
        step=50.0,
        format="%.2f"
    )

with col_in2:
    check_date = st.date_input("Date", value=date.today())

with col_in3:
    st.write("")
    st.write("")
    add_check = st.button("Add Check", use_container_width=True)

if add_check:
    if check_amount > 0:
        se, fed, state_t, reserve = compute_check_taxes(check_amount)
        st.session_state.checks.append({
            "amount": check_amount,
            "date": check_date,
            "se": se,
            "fed": fed,
            "state": state_t,
            "reserve": reserve,
            "remaining": check_amount - reserve
        })
        st.rerun()
    else:
        st.warning("Enter a check amount.")

total_se_account    = sum(c["se"]     for c in st.session_state.checks)
total_fed_account   = sum(c["fed"]    for c in st.session_state.checks)
total_state_account = sum(c["state"]  for c in st.session_state.checks)
total_gross         = sum(c["amount"] for c in st.session_state.checks)

avg_check       = total_gross / len(st.session_state.checks) if st.session_state.checks else 0.0
projected_annual = avg_check * 52

col_a1, col_a2, col_a3, col_a4 = st.columns(4)

with col_a1:
    st.metric("SE Tax Account", f"${total_se_account:,.2f}")
with col_a2:
    st.metric("Federal Account", f"${total_fed_account:,.2f}")
with col_a3:
    st.metric("State Account", f"${total_state_account:,.2f}")
with col_a4:
    st.metric("Projected Annual Gross", f"${projected_annual:,.2f}")

st.divider()

# =========================
# WEEKLY BUDGET
# =========================

st.header("Weekly Budget")

if st.session_state.checks:
    rows_html = ""
    for c in reversed(st.session_state.checks):
        rows_html += f"""
        <tr>
            <td class="col-date">{c["date"].strftime("%m/%d/%Y")}</td>
            <td class="col-check">${c['amount']:,.2f}</td>
            <td class="col-tax">${c['reserve']:,.2f}</td>
            <td class="col-keep">${c['remaining']:,.2f}</td>
        </tr>
        """

    st.markdown(f"""
    <table class="deco-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Check Total</th>
                <th>Tax Reserve</th>
                <th>Remaining Spendable</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

else:
    st.info("Add your first check above to see your budget breakdown.")

st.divider()

# =========================
# MONTHLY BILLS
# =========================

st.header("Monthly Bills")

with st.expander("Add Monthly Bill", expanded=True):
    bill_name    = st.text_input("Bill Name", placeholder="Netflix, Insurance, GitHub, Credit Card")
    bill_amount  = st.number_input("Monthly Amount", min_value=0.0, step=1.0)
    bill_due_date = st.date_input("Due Date")

    if st.button("Add Bill"):
        if bill_name and bill_amount > 0:
            st.session_state.monthly_bills.append({
                "name": bill_name,
                "amount": bill_amount,
                "due_date": bill_due_date
            })
            st.success(f"Added {bill_name}")
        else:
            st.warning("Enter a bill name and amount.")

monthly_bills_total         = sum(b["amount"] for b in st.session_state.monthly_bills)
weekly_monthly_bill_reserve = monthly_bills_total * 12 / 52

col_mb1, col_mb2 = st.columns(2)
with col_mb1:
    st.metric("Monthly Bills Total", f"${monthly_bills_total:,.2f}")
with col_mb2:
    st.metric("Weekly Reserve for Monthly Bills", f"${weekly_monthly_bill_reserve:,.2f}")

if st.session_state.monthly_bills:
    st.subheader("Bills List")

    for index, bill in enumerate(st.session_state.monthly_bills):
        col_b1, col_b2, col_b3, col_b4 = st.columns([3, 2, 2, 1])

        with col_b1:
            st.write(bill["name"])
        with col_b2:
            st.write(f"${bill['amount']:,.2f}")
        with col_b3:
            st.write(bill["due_date"].strftime("%B %d"))
        with col_b4:
            if st.button("Delete", key=f"delete_bill_{index}"):
                st.session_state.monthly_bills.pop(index)
                st.rerun()

st.divider()

# =========================
# BUSINESS DEDUCTIONS
# =========================

st.header("Business Deductions")

business_miles       = st.number_input("Business Miles",          min_value=0.0, step=100.0)
mileage_deduction    = business_miles * 0.725
home_office          = st.number_input("Home Office Deduction",   min_value=0.0, step=100.0)
tools_equipment      = st.number_input("Tools & Equipment",       min_value=0.0, step=100.0)
health_insurance     = st.number_input("Health Insurance",        min_value=0.0, step=100.0)
professional_services = st.number_input("Professional Services",  min_value=0.0, step=100.0)
other_deductions     = st.number_input("Other Deductions",        min_value=0.0, step=100.0)

total_deductions = (
    mileage_deduction + home_office + tools_equipment
    + health_insurance + professional_services + other_deductions
)

st.metric("Total Deductions", f"${total_deductions:,.2f}")

st.divider()

# =========================
# TAX CALCULATIONS
# =========================

st.header("Tax Calculations")

net_se_income          = max(projected_annual - total_deductions, 0)
se_taxable_income      = net_se_income * 0.9235
self_employment_tax    = se_taxable_income * 0.153
half_se_tax_deduction  = self_employment_tax / 2
standard_deduction     = 16100
federal_taxable_income = max(net_se_income - half_se_tax_deduction - standard_deduction, 0)
federal_income_tax     = federal_taxable_income * 0.12
arizona_state_tax      = net_se_income * 0.025
annual_total_tax       = self_employment_tax + federal_income_tax + arizona_state_tax
quarterly_payment      = annual_total_tax / 4

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.metric("Arizona State Tax",    f"${arizona_state_tax:,.2f}")
    st.metric("Self-Employment Tax",  f"${self_employment_tax:,.2f}")
    st.metric("Federal Income Tax",   f"${federal_income_tax:,.2f}")

with col_t2:
    st.metric("Estimated Annual Taxes", f"${annual_total_tax:,.2f}")
    st.metric("Quarterly Payment",      f"${quarterly_payment:,.2f}")

st.divider()

# =========================
# FINAL TOTALS
# =========================

st.header("Final Totals")

weekly_bills = st.number_input("Weekly Bills", min_value=0.0, step=50.0)

latest_check      = st.session_state.checks[-1] if st.session_state.checks else None
weekly_gross_pay  = latest_check["amount"]  if latest_check else 0.0
weekly_tax_reserve = latest_check["reserve"] if latest_check else 0.0

remaining_weekly_cash = (
    weekly_gross_pay
    - weekly_tax_reserve
    - weekly_bills
    - weekly_monthly_bill_reserve
)

monthly_total_obligations = weekly_bills * 4 + monthly_bills_total

annual_take_home  = projected_annual - annual_total_tax - (monthly_total_obligations * 12)
monthly_take_home = annual_take_home / 12

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.metric("Annual Take Home",   f"${annual_take_home:,.2f}")
with col_f2:
    st.metric("Monthly Take Home",  f"${monthly_take_home:,.2f}")
with col_f3:
    st.metric("Weekly Spendable",   f"${remaining_weekly_cash:,.2f}")

st.caption("2026 mileage rate: $0.725/mile  ·  Estimates only — not financial advice")
