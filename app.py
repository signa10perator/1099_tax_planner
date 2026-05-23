import streamlit as st

st.set_page_config(
    page_title="1099 Quarterly Tax Planner",
    layout="wide"
)

st.title("1099 Quarterly Tax Planner")

# Initialize session state early so weekly_monthly_bill_reserve is available
if "monthly_bills" not in st.session_state:
    st.session_state.monthly_bills = []

st.divider()

# =========================
# INCOME
# =========================

st.header("Income")

income_mode = st.radio(
    "Income Entry Mode",
    ["Weekly Pay", "Annual Income"],
    horizontal=True
)

weeks_worked = 52

if income_mode == "Weekly Pay":

    weekly_gross_pay = st.number_input(
        "Weekly Gross Pay",
        min_value=0.0,
        step=50.0
    )

    weeks_worked = st.number_input(
        "Weeks Worked Per Year",
        min_value=1,
        max_value=52,
        value=52
    )

    annual_gross_income = weekly_gross_pay * weeks_worked

else:

    annual_gross_income = st.number_input(
        "Annual Gross Income",
        min_value=0.0,
        step=1000.0
    )

    weekly_gross_pay = annual_gross_income / 52

st.metric(
    "Projected Annual Gross Income",
    f"${annual_gross_income:,.2f}"
)

st.divider()

# =========================
# DEDUCTIONS
# =========================

st.header("Business Deductions")

business_miles = st.number_input(
    "Business Miles",
    min_value=0.0,
    step=100.0
)

mileage_deduction = business_miles * 0.725

home_office = st.number_input(
    "Home Office Deduction",
    min_value=0.0,
    step=100.0
)

tools_equipment = st.number_input(
    "Tools & Equipment",
    min_value=0.0,
    step=100.0
)

health_insurance = st.number_input(
    "Health Insurance",
    min_value=0.0,
    step=100.0
)

professional_services = st.number_input(
    "Professional Services",
    min_value=0.0,
    step=100.0
)

other_deductions = st.number_input(
    "Other Deductions",
    min_value=0.0,
    step=100.0
)

total_deductions = (
    mileage_deduction
    + home_office
    + tools_equipment
    + health_insurance
    + professional_services
    + other_deductions
)

st.metric(
    "Total Deductions",
    f"${total_deductions:,.2f}"
)

st.divider()

# =========================
# TAX CALCULATIONS
# =========================

st.header("Tax Calculations")

net_se_income = max(
    annual_gross_income - total_deductions,
    0
)

# Self-employment tax
se_taxable_income = net_se_income * 0.9235
self_employment_tax = se_taxable_income * 0.153

# Half SE tax deduction
half_se_tax_deduction = self_employment_tax / 2

# Standard deduction
standard_deduction = 16100

# Federal taxable income
federal_taxable_income = max(
    net_se_income
    - half_se_tax_deduction
    - standard_deduction,
    0
)

# SIMPLE federal estimate
# Replace later with full tax brackets
federal_income_tax = federal_taxable_income * 0.12

# ========================
# ARIZONA STATE TAX
# ========================

arizona_state_tax = net_se_income * 0.025

annual_total_tax = (
    self_employment_tax
    + federal_income_tax
    + arizona_state_tax
)

quarterly_payment = annual_total_tax / 4

weekly_tax_reserve = annual_total_tax / weeks_worked

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Arizona State Tax",
        f"${arizona_state_tax:,.2f}"
    )

    st.metric(
        "Self-Employment Tax",
        f"${self_employment_tax:,.2f}"
    )

    st.metric(
        "Federal Income Tax",
        f"${federal_income_tax:,.2f}"
    )

with col2:
    st.metric(
        "Estimated Annual Taxes",
        f"${annual_total_tax:,.2f}"
    )

    st.metric(
        "Quarterly Payment",
        f"${quarterly_payment:,.2f}"
    )

st.divider()

# =========================
# WEEKLY BILLS
# =========================

# Compute monthly bill reserve from session state before it's displayed
monthly_bills_total = sum(
    bill["amount"] for bill in st.session_state.monthly_bills
)
weekly_monthly_bill_reserve = monthly_bills_total * 12 / 52

st.header("Weekly Budget")

weekly_bills = st.number_input(
    "Weekly Bills",
    min_value=0.0,
    step=50.0
)

remaining_weekly_cash = (
    weekly_gross_pay
    - weekly_tax_reserve
    - weekly_bills
    - weekly_monthly_bill_reserve
)

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "Weekly Tax Reserve",
        f"${weekly_tax_reserve:,.2f}"
    )

with col4:
    st.metric(
        "Remaining Weekly Cash",
        f"${remaining_weekly_cash:,.2f}"
    )

st.divider()

# =========================
# MONTHLY BILLS Ledger
# =========================

st.header("Monthly Bills")

with st.expander("Add Monthly Bill", expanded=True):
    bill_name = st.text_input("Bill Name", placeholder="Netflix, Insurance, GitHub, Credit Card")
    bill_amount = st.number_input("Monthly Amount", min_value=0.0, step=1.0)
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

st.metric("Monthly Bills Total", f"${monthly_bills_total:,.2f}")
st.metric("Weekly Reserve for Monthly Bills", f"${weekly_monthly_bill_reserve:,.2f}")

if st.session_state.monthly_bills:
    st.subheader("Bills List")

    for index, bill in enumerate(st.session_state.monthly_bills):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.write(bill["name"])

        with col2:
            st.write(f"{bill['amount']:,.2f}")

        with col3:
            st.write(bill["due_date"].strftime("%B %d"))

        with col4:
            if st.button("Delete", key=f"delete_bill_{index}"):
                st.session_state.monthly_bills.pop(index)
                st.rerun()

st.divider()

# =========================
# FINAL TOTALS
# =========================

st.header("Final Totals")

monthly_total_obligations = (
    weekly_bills * 4
    + monthly_bills_total
)

annual_take_home = (
    annual_gross_income
    - annual_total_tax
    - (monthly_total_obligations * 12)
)

monthly_take_home = annual_take_home / 12

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Annual Take Home",
        f"${annual_take_home:,.2f}"
    )

with col6:
    st.metric(
        "Monthly Take Home",
        f"${monthly_take_home:,.2f}"
    )

with col7:
    st.metric(
        "Weekly Spendable",
        f"${remaining_weekly_cash:,.2f}"
    )

st.caption(
    "2026 mileage rate: $0.725/mile | Estimates only"
)
