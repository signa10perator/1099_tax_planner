import os
import streamlit as st
from datetime import date, datetime
from supabase import create_client

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

hr {
    border: none !important;
    border-top: 1px solid #1e1c12 !important;
    margin: 1.75rem 0 !important;
}

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

label {
    color: #5a5030 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
}

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

input[type="password"] {
    background-color: #0f0f0a !important;
    border: none !important;
    border-bottom: 1px solid #2e2a18 !important;
    border-radius: 0 !important;
    color: #e8dfc8 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

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

[data-testid="stAlert"] {
    border-radius: 0 !important;
    background-color: #0f0f0a !important;
    border: 1px solid #1e1c12 !important;
    border-left: 3px solid #c8a84c !important;
    color: #7a6e48 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em;
}

[data-testid="stCaptionContainer"] p {
    color: #2e2a18 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-size: 0.55rem !important;
}

/* Radio buttons (auth page) */
[data-testid="stRadio"] label {
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
}

.deco-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Josefin Sans', sans-serif;
    margin-top: 0.75rem;
}

.deco-table thead tr { border-bottom: 1px solid #c8a84c; }

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

.user-bar {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3a3020;
    text-align: right;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SUPABASE CLIENT
# =========================

def get_secret(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        return st.secrets[key]
    except Exception:
        return None

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_KEY")
)

# =========================
# SESSION RESTORE
# =========================

user_id    = None
user_email = None

if "sb_access_token" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state["sb_access_token"],
            st.session_state["sb_refresh_token"]
        )
        supabase.postgrest.auth(st.session_state["sb_access_token"])
        user_id    = st.session_state["sb_user_id"]
        user_email = st.session_state["sb_user_email"]
    except Exception:
        for key in ["sb_access_token", "sb_refresh_token", "sb_user_id", "sb_user_email", "data_loaded"]:
            st.session_state.pop(key, None)

# =========================
# AUTH PAGE
# =========================

if not user_id:
    st.title("1099 Quarterly Tax Planner")
    st.divider()

    _, col_auth, _ = st.columns([1, 2, 1])

    with col_auth:
        auth_mode = st.radio(
            "",
            ["Sign In", "Create Account"],
            horizontal=True,
            label_visibility="collapsed"
        )

        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if auth_mode == "Sign In":
            if st.button("Sign In", use_container_width=True):
                if email and password:
                    try:
                        resp = supabase.auth.sign_in_with_password(
                            {"email": email, "password": password}
                        )
                        st.session_state["sb_access_token"]  = resp.session.access_token
                        st.session_state["sb_refresh_token"] = resp.session.refresh_token
                        st.session_state["sb_user_id"]       = resp.user.id
                        st.session_state["sb_user_email"]    = resp.user.email
                        st.rerun()
                    except Exception:
                        st.error("Invalid email or password.")
                else:
                    st.warning("Enter your email and password.")
        else:
            if st.button("Create Account", use_container_width=True):
                if email and password:
                    try:
                        resp = supabase.auth.sign_up(
                            {"email": email, "password": password}
                        )
                        if resp.user:
                            st.success("Account created. Check your email to confirm, then sign in.")
                        else:
                            st.error("Could not create account.")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Enter an email and password.")

    st.stop()

# =========================
# DATA HELPERS
# =========================

def parse_date(d):
    if isinstance(d, (date, datetime)):
        return d if isinstance(d, date) else d.date()
    return datetime.strptime(d[:10], "%Y-%m-%d").date()


def load_user_data():
    checks_res = (
        supabase.table("checks")
        .select("*")
        .eq("user_id", user_id)
        .order("date")
        .execute()
    )
    bills_res = (
        supabase.table("monthly_bills")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at")
        .execute()
    )

    st.session_state.checks = [
        {
            "id":        c["id"],
            "amount":    c["amount"],
            "date":      parse_date(c["date"]),
            "se":        c["se"],
            "fed":       c["fed"],
            "state":     c["state"],
            "reserve":   c["reserve"],
            "remaining": c["remaining"],
        }
        for c in checks_res.data
    ]

    st.session_state.monthly_bills = [
        {
            "id":       b["id"],
            "name":     b["name"],
            "amount":   b["amount"],
            "due_date": parse_date(b["due_date"]),
        }
        for b in bills_res.data
    ]

    st.session_state.data_loaded = True


def add_check_to_db(check_data):
    result = (
        supabase.table("checks")
        .insert({
            "user_id":   user_id,
            "amount":    check_data["amount"],
            "date":      check_data["date"].isoformat(),
            "se":        check_data["se"],
            "fed":       check_data["fed"],
            "state":     check_data["state"],
            "reserve":   check_data["reserve"],
            "remaining": check_data["remaining"],
        })
        .execute()
    )
    check_data["id"] = result.data[0]["id"]
    return check_data


def add_bill_to_db(bill_data):
    result = (
        supabase.table("monthly_bills")
        .insert({
            "user_id":  user_id,
            "name":     bill_data["name"],
            "amount":   bill_data["amount"],
            "due_date": bill_data["due_date"].isoformat(),
        })
        .execute()
    )
    bill_data["id"] = result.data[0]["id"]
    return bill_data


def delete_bill_from_db(bill_id):
    supabase.table("monthly_bills").delete().eq("id", bill_id).execute()


def logout():
    supabase.auth.sign_out()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# Load data once per session
if not st.session_state.get("data_loaded"):
    load_user_data()

# =========================
# TAX HELPER
# =========================

def compute_check_taxes(amount):
    se_weekly = amount * 0.9235 * 0.153

    annual   = amount * 52
    se_annual = se_weekly * 52
    half_se  = se_annual / 2
    fed_taxable = max(annual - half_se - 16100, 0)
    fed_weekly  = (fed_taxable * 0.12) / 52

    state_weekly = amount * 0.025

    total = se_weekly + fed_weekly + state_weekly
    return se_weekly, fed_weekly, state_weekly, total

# =========================
# HEADER + SIGN OUT
# =========================

col_title, col_user = st.columns([5, 1])
with col_title:
    st.title("1099 Quarterly Tax Planner")
with col_user:
    st.markdown(f'<div class="user-bar">{user_email}</div>', unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        logout()

st.divider()

# =========================
# INCOME
# =========================

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
        new_check = {
            "amount":    check_amount,
            "date":      check_date,
            "se":        se,
            "fed":       fed,
            "state":     state_t,
            "reserve":   reserve,
            "remaining": check_amount - reserve,
        }
        new_check = add_check_to_db(new_check)
        st.session_state.checks.append(new_check)
        st.rerun()
    else:
        st.warning("Enter a check amount.")

total_se_account    = sum(c["se"]     for c in st.session_state.checks)
total_fed_account   = sum(c["fed"]    for c in st.session_state.checks)
total_state_account = sum(c["state"]  for c in st.session_state.checks)
total_gross         = sum(c["amount"] for c in st.session_state.checks)

avg_check        = total_gross / len(st.session_state.checks) if st.session_state.checks else 0.0
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
    bill_name     = st.text_input("Bill Name", placeholder="Netflix, Insurance, GitHub, Credit Card")
    bill_amount   = st.number_input("Monthly Amount", min_value=0.0, step=1.0)
    bill_due_date = st.date_input("Due Date")

    if st.button("Add Bill"):
        if bill_name and bill_amount > 0:
            new_bill = {
                "name":     bill_name,
                "amount":   bill_amount,
                "due_date": bill_due_date,
            }
            new_bill = add_bill_to_db(new_bill)
            st.session_state.monthly_bills.append(new_bill)
            st.rerun()
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
                delete_bill_from_db(bill["id"])
                st.session_state.monthly_bills.pop(index)
                st.rerun()

st.divider()

# =========================
# BUSINESS DEDUCTIONS
# =========================

st.header("Business Deductions")

business_miles        = st.number_input("Business Miles",         min_value=0.0, step=100.0)
mileage_deduction     = business_miles * 0.725
home_office           = st.number_input("Home Office Deduction",  min_value=0.0, step=100.0)
tools_equipment       = st.number_input("Tools & Equipment",      min_value=0.0, step=100.0)
health_insurance      = st.number_input("Health Insurance",       min_value=0.0, step=100.0)
professional_services = st.number_input("Professional Services",  min_value=0.0, step=100.0)
other_deductions      = st.number_input("Other Deductions",       min_value=0.0, step=100.0)

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
    st.metric("Arizona State Tax",   f"${arizona_state_tax:,.2f}")
    st.metric("Self-Employment Tax", f"${self_employment_tax:,.2f}")
    st.metric("Federal Income Tax",  f"${federal_income_tax:,.2f}")

with col_t2:
    st.metric("Estimated Annual Taxes", f"${annual_total_tax:,.2f}")
    st.metric("Quarterly Payment",      f"${quarterly_payment:,.2f}")

st.divider()

# =========================
# FINAL TOTALS
# =========================

st.header("Final Totals")

weekly_bills = st.number_input("Weekly Bills", min_value=0.0, step=50.0)

latest_check       = st.session_state.checks[-1] if st.session_state.checks else None
weekly_gross_pay   = latest_check["amount"]  if latest_check else 0.0
weekly_tax_reserve = latest_check["reserve"] if latest_check else 0.0

remaining_weekly_cash = (
    weekly_gross_pay
    - weekly_tax_reserve
    - weekly_bills
    - weekly_monthly_bill_reserve
)

monthly_total_obligations = weekly_bills * 4 + monthly_bills_total
annual_take_home          = projected_annual - annual_total_tax - (monthly_total_obligations * 12)
monthly_take_home         = annual_take_home / 12

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.metric("Annual Take Home",  f"${annual_take_home:,.2f}")
with col_f2:
    st.metric("Monthly Take Home", f"${monthly_take_home:,.2f}")
with col_f3:
    st.metric("Weekly Spendable",  f"${remaining_weekly_cash:,.2f}")

st.caption("2026 mileage rate: $0.725/mile  ·  Estimates only — not financial advice")
