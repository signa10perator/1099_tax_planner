import os
import streamlit as st
from datetime import date, datetime
from supabase import create_client
import plotly.graph_objects as go

st.set_page_config(
    page_title="The Contractors Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Josefin+Sans:wght@300;400;600;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: radial-gradient(ellipse at 50% 20%, #0d0d09 0%, #000000 70%) !important;
    color: #e8dfc8;
    font-family: 'Josefin Sans', sans-serif;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    max-width: 1200px;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
footer, #MainMenu {
    display: none !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid #1a1810 !important;
    min-width: 220px !important;
    max-width: 220px !important;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* SIDEBAR RADIO NAV */
section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 0;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center;
    padding: 0.7rem 0 0.7rem 1.25rem !important;
    border-left: 3px solid transparent;
    transition: all 0.12s;
    cursor: pointer;
    margin: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label p {
    color: #4a4228 !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.16em !important;
    font-weight: 700 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    text-transform: uppercase;
    margin: 0 !important;
    transition: all 0.12s;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    border-left: 3px solid #c8a84c !important;
    background: #060604 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
    color: #c8a84c !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    border-left: 3px solid #c8a84c !important;
    background: #080806 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #c8a84c !important;
}

/* TYPOGRAPHY */
h1 {
    font-family: 'Cinzel', serif !important;
    color: #c8a84c !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0 !important;
    line-height: 1.1 !important;
}

h2 {
    font-family: 'Cinzel', serif !important;
    color: #c8a84c !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 0.75rem !important;
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
    font-size: 0.7rem !important;
    font-weight: 600 !important;
}

hr {
    border: none !important;
    border-top: 1px solid #111108 !important;
    margin: 1.5rem 0 !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: #050504 !important;
    border: 1px solid #111108 !important;
    border-left: 3px solid #c8a84c !important;
    padding: 0.85rem 1rem !important;
    border-radius: 0 !important;
}

[data-testid="stMetricLabel"] p {
    color: #4a4228 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-size: 0.55rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] div {
    color: #c8a84c !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.3rem !important;
}

/* LABELS */
label {
    color: #4a4228 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.58rem !important;
    font-weight: 700 !important;
}

/* INPUTS */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input,
input[type="password"] {
    background-color: #050504 !important;
    border: none !important;
    border-bottom: 1px solid #1e1c12 !important;
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
    font-size: 0.58rem !important;
    font-weight: 700 !important;
    border-radius: 0 !important;
    transition: all 0.15s ease !important;
    padding: 0.4rem 1rem !important;
}

.stButton > button:hover {
    background-color: #c8a84c !important;
    color: #000000 !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background-color: #050504 !important;
    border: 1px solid #111108 !important;
    border-radius: 0 !important;
}

[data-testid="stExpander"] summary span p {
    color: #7a6e48 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    background-color: #050504 !important;
    border: 1px solid #111108 !important;
    border-left: 3px solid #c8a84c !important;
    color: #7a6e48 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.05em;
}

/* CAPTION */
[data-testid="stCaptionContainer"] p {
    color: #1e1c12 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-size: 0.52rem !important;
}

/* RADIO (auth page) */
[data-testid="stMain"] [data-testid="stRadio"] div[role="radiogroup"] > label {
    padding: 0.4rem 1rem !important;
}

[data-testid="stMain"] [data-testid="stRadio"] div[role="radiogroup"] > label p {
    color: #7a6e48 !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
}

/* CUSTOM ELEMENTS */
.terminal-header {
    border-bottom: 1px solid #1a1810;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}

.terminal-title {
    font-family: 'Cinzel', serif;
    color: #c8a84c;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    line-height: 1;
}

.terminal-sub {
    font-family: 'Josefin Sans', sans-serif;
    color: #4a4228;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

.terminal-tagline {
    font-family: 'Josefin Sans', sans-serif;
    color: #7a6e48;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.status-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4a9e4a;
    display: inline-block;
}

.status-text {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.55rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4a9e4a;
}

.status-ver {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    color: #2a2218;
}

.alert-panel {
    background: #050504;
    border: 1px solid #111108;
    border-top: 2px solid #8b1a1a;
    padding: 1rem;
    height: 100%;
}

.alert-title {
    font-family: 'Cinzel', serif;
    color: #8b1a1a;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.alert-item {
    font-family: 'Josefin Sans', sans-serif;
    color: #c8a84c;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.alert-detail {
    font-family: 'Josefin Sans', sans-serif;
    color: #4a4228;
    font-size: 0.55rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #111108;
}

.manifesto {
    background: #050504;
    border: 1px solid #111108;
    padding: 1.25rem 1.5rem;
    margin-top: 1.5rem;
}

.manifesto-main {
    font-family: 'Cinzel', serif;
    color: #c8a84c;
    font-size: 0.9rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    line-height: 1.4;
    margin-bottom: 0.5rem;
}

.manifesto-sub {
    font-family: 'Josefin Sans', sans-serif;
    color: #4a4228;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    line-height: 1.6;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.5rem 1.25rem 1.25rem;
    border-bottom: 1px solid #111108;
    margin-bottom: 0.5rem;
}

.logo-badge {
    background: #c8a84c;
    color: #000;
    font-family: 'Cinzel', serif;
    font-size: 0.9rem;
    font-weight: 700;
    padding: 0.35rem 0.5rem;
    text-align: center;
    line-height: 1.1;
    min-width: 38px;
}

.logo-label {
    font-family: 'Cinzel', serif;
    color: #c8a84c;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    font-weight: 700;
    text-transform: uppercase;
    line-height: 1.4;
}

.logo-sub-label {
    font-family: 'Josefin Sans', sans-serif;
    color: #2a2218;
    font-size: 0.5rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.sidebar-footer {
    padding: 1.25rem;
    border-top: 1px solid #111108;
    margin-top: 1rem;
}

.sidebar-motto {
    font-family: 'Josefin Sans', sans-serif;
    color: #4a4228;
    font-size: 0.55rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    line-height: 1.6;
}

.sidebar-motto-accent {
    font-family: 'Cinzel', serif;
    color: #8b1a1a;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.sidebar-sub {
    font-family: 'Josefin Sans', sans-serif;
    color: #1e1c12;
    font-size: 0.48rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    line-height: 1.6;
}

.user-bar {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #2a2218;
    text-align: right;
}

.gauge-label {
    font-family: 'Cinzel', serif;
    color: #c8a84c;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.25rem;
}

.gauge-sublabel {
    font-family: 'Josefin Sans', sans-serif;
    color: #4a4228;
    font-size: 0.5rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.5rem;
}

.gauge-flavor {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.5rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 0.25rem;
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
    letter-spacing: 0.16em;
    font-size: 0.55rem;
    font-weight: 700;
    padding: 0 0.5rem 0.6rem 0;
    text-align: left;
}

.deco-table td {
    border-bottom: 1px solid #0d0d09;
    color: #e8dfc8;
    padding: 0.65rem 0.5rem 0.65rem 0;
    font-size: 0.82rem;
    letter-spacing: 0.03em;
}

.deco-table tr:last-child td { border-bottom: none; }
.deco-table .col-date  { color: #4a4228; font-size: 0.72rem; letter-spacing: 0.06em; }
.deco-table .col-check { color: #c8a84c; font-weight: 600; }
.deco-table .col-tax   { color: #7a6e48; }
.deco-table .col-keep  { color: #e8dfc8; }
</style>
""", unsafe_allow_html=True)

# =========================
# SUPABASE
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
    st.markdown("""
    <div class="terminal-header" style="text-align:center; border:none;">
        <div class="terminal-title">THE CONTRACTORS TERMINAL</div>
        <div class="terminal-sub">Tax & Budget Control Console</div>
        <div class="terminal-tagline">No Subscriptions. No Financial Handcuffs. Just Survival.</div>
    </div>
    """, unsafe_allow_html=True)

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
                            st.success("Account created. Sign in to continue.")
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


if not st.session_state.get("data_loaded"):
    load_user_data()

# Session state defaults
if "deductions" not in st.session_state:
    st.session_state.deductions = {
        "business_miles": 0.0,
        "home_office": 0.0,
        "tools_equipment": 0.0,
        "health_insurance": 0.0,
        "professional_services": 0.0,
        "other": 0.0,
    }

if "weekly_bills" not in st.session_state:
    st.session_state.weekly_bills = 0.0

# =========================
# TAX HELPER
# =========================

def compute_check_taxes(amount):
    se_weekly   = amount * 0.9235 * 0.153
    annual      = amount * 52
    se_annual   = se_weekly * 52
    half_se     = se_annual / 2
    fed_taxable = max(annual - half_se - 16100, 0)
    fed_weekly  = (fed_taxable * 0.12) / 52
    state_weekly = amount * 0.025
    total = se_weekly + fed_weekly + state_weekly
    return se_weekly, fed_weekly, state_weekly, total

# =========================
# COMPUTED STATE
# =========================

total_se_account    = sum(c["se"]     for c in st.session_state.checks)
total_fed_account   = sum(c["fed"]    for c in st.session_state.checks)
total_state_account = sum(c["state"]  for c in st.session_state.checks)
total_gross         = sum(c["amount"] for c in st.session_state.checks)
avg_check           = total_gross / len(st.session_state.checks) if st.session_state.checks else 0.0
projected_annual    = avg_check * 52

monthly_bills_total         = sum(b["amount"] for b in st.session_state.monthly_bills)
weekly_monthly_bill_reserve = monthly_bills_total * 12 / 52

d = st.session_state.deductions
mileage_deduction  = d["business_miles"] * 0.725
total_deductions   = (
    mileage_deduction + d["home_office"] + d["tools_equipment"]
    + d["health_insurance"] + d["professional_services"] + d["other"]
)

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

latest_check       = st.session_state.checks[-1] if st.session_state.checks else None
weekly_gross_pay   = latest_check["amount"]  if latest_check else 0.0
weekly_tax_reserve = latest_check["reserve"] if latest_check else 0.0

monthly_obligations = st.session_state.weekly_bills * 4 + monthly_bills_total
annual_take_home    = projected_annual - annual_total_tax - (monthly_obligations * 12)
monthly_take_home   = annual_take_home / 12
remaining_weekly    = (
    weekly_gross_pay - weekly_tax_reserve
    - st.session_state.weekly_bills - weekly_monthly_bill_reserve
)

# =========================
# GAUGE HELPER
# =========================

def make_gauge(value, max_val, color, zone_label):
    pct = min((value / max_val * 100) if max_val > 0 else 0, 100)
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=pct,
        gauge={
            'axis': {
                'range': [0, 100],
                'visible': False,
            },
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': '#050504',
            'borderwidth': 1,
            'bordercolor': '#111108',
            'steps': [{'range': [0, 100], 'color': '#080806'}],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=160,
        margin=dict(l=15, r=15, t=15, b=0),
    )
    return fig

# =========================
# DEADLINE HELPER
# =========================

def next_deadline():
    today = date.today()
    year = today.year
    candidates = [
        ("Q1", date(year, 4, 15)),
        ("Q2", date(year, 6, 15) if date(year, 6, 15).weekday() < 5 else date(year, 6, 16)),
        ("Q3", date(year, 9, 15)),
        ("Q4", date(year + 1, 1, 15)),
    ]
    for label, d in candidates:
        if d >= today:
            return label, d, (d - today).days
    return None, None, None

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-badge">10<br>99</div>
        <div>
            <div class="logo-label">Contractor</div>
            <div class="logo-sub-label">Survival Systems</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        [
            "Control Console",
            "Income Log",
            "Allocation Matrix",
            "Mandatory Extraction",
            "Reserve Vault",
            "Ledger Archives",
            "System Settings",
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="sidebar-footer">
        <div class="sidebar-motto">Income isn't the problem.</div>
        <div class="sidebar-motto-accent">Control is.</div>
        <div class="sidebar-sub">Know your numbers.<br>Keep your freedom.</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# USER BAR
# =========================

col_usr, col_out = st.columns([6, 1])
with col_usr:
    q_label, q_date, q_days = next_deadline()
    if q_days is not None and q_days <= 45:
        st.markdown(
            f'<span style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;'
            f'letter-spacing:0.12em;text-transform:uppercase;color:#8b1a1a;">'
            f'⚠ {q_label} Payment Due in {q_days} Days — ${quarterly_payment:,.2f}</span>',
            unsafe_allow_html=True
        )
with col_out:
    st.markdown(f'<div class="user-bar">{user_email}</div>', unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        logout()

st.divider()

# =========================
# PAGES
# =========================

if page == "Control Console":

    st.markdown("""
    <div>
        <div class="status-bar">
            <span class="status-dot"></span>
            <span class="status-text">System Status: Operational</span>
            <span class="status-ver">Ver. 1.0.99</span>
        </div>
        <div class="terminal-title">The Contractors Terminal</div>
        <div class="terminal-sub">Tax & Budget Control Console</div>
        <div class="terminal-tagline">No Subscriptions. No Financial Handcuffs. Just Survival.</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col_g1, col_g2, col_g3, col_alert = st.columns([2, 2, 2, 1])

    with col_g1:
        st.markdown('<div class="gauge-label">Mandatory Extraction</div>', unsafe_allow_html=True)
        st.markdown('<div class="gauge-sublabel">Est. Tax Obligation</div>', unsafe_allow_html=True)
        fig = make_gauge(annual_total_tax, projected_annual, "#8b1a1a", "HIGH EXTRACTION ZONE")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="gauge-flavor" style="color:#8b1a1a;">High Extraction Zone</div>', unsafe_allow_html=True)
        st.metric("Annual Tax Obligation", f"${annual_total_tax:,.2f}")
        pct = (annual_total_tax / projected_annual * 100) if projected_annual > 0 else 0
        st.metric("Extraction Rate", f"{pct:.1f}% of Income")

    with col_g2:
        st.markdown('<div class="gauge-label">Reserve Allocation</div>', unsafe_allow_html=True)
        st.markdown('<div class="gauge-sublabel">Monthly Obligations</div>', unsafe_allow_html=True)
        fig = make_gauge(monthly_bills_total * 12, projected_annual, "#c8a84c", "FORTIFY YOUR POSITION")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="gauge-flavor" style="color:#c8a84c;">Fortify Your Position</div>', unsafe_allow_html=True)
        st.metric("Annual Obligations", f"${monthly_bills_total * 12:,.2f}")
        pct2 = (monthly_bills_total * 12 / projected_annual * 100) if projected_annual > 0 else 0
        st.metric("Reserve Rate", f"{pct2:.1f}% of Income")

    with col_g3:
        st.markdown('<div class="gauge-label">Survival Balance</div>', unsafe_allow_html=True)
        st.markdown('<div class="gauge-sublabel">Discretionary Funds</div>', unsafe_allow_html=True)
        fig = make_gauge(max(annual_take_home, 0), projected_annual, "#2d7a6b", "REMAINING CONTROL")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="gauge-flavor" style="color:#2d7a6b;">Remaining Control</div>', unsafe_allow_html=True)
        st.metric("Annual Take Home", f"${annual_take_home:,.2f}")
        pct3 = (max(annual_take_home, 0) / projected_annual * 100) if projected_annual > 0 else 0
        st.metric("Survival Rate", f"{pct3:.1f}% of Income")

    with col_alert:
        q_label, q_date, q_days = next_deadline()
        alert_html = '<div class="alert-panel"><div class="alert-title">System Alerts</div>'
        if q_days is not None:
            color = "#8b1a1a" if q_days <= 30 else "#c8a84c"
            alert_html += f"""
            <div class="alert-item" style="color:{color};">Tax Deadline Approaching</div>
            <div class="alert-detail">{q_label} Estimated Payment<br>Due in {q_days} Days</div>
            """
        alert_html += f"""
        <div class="alert-item">Extraction Pressure</div>
        <div class="alert-detail">2026 Effective Rate<br>{pct:.1f}%</div>
        <div class="alert-item" style="color:#4a4228;">System Notice</div>
        <div class="alert-detail">The more you earn,<br>the more they take.<br>Plan accordingly.</div>
        </div>"""
        st.markdown(alert_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="manifesto">
        <div class="manifesto-main">You don't work for them.<br>You work despite them.</div>
        <div class="manifesto-sub">This terminal gives you the edge they don't want you to have.</div>
    </div>
    """, unsafe_allow_html=True)

elif page == "Income Log":

    st.header("Income Log")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Receipts & Jobs</div>', unsafe_allow_html=True)

    col_in1, col_in2, col_in3 = st.columns([3, 3, 1])
    with col_in1:
        check_amount = st.number_input("Weekly Check", min_value=0.0, step=50.0, format="%.2f")
    with col_in2:
        check_date = st.date_input("Date", value=date.today())
    with col_in3:
        st.write("")
        st.write("")
        add_check = st.button("Log Check", use_container_width=True)

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

    st.divider()

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        st.metric("SE Tax Account",       f"${total_se_account:,.2f}")
    with col_a2:
        st.metric("Federal Account",      f"${total_fed_account:,.2f}")
    with col_a3:
        st.metric("State Account",        f"${total_state_account:,.2f}")
    with col_a4:
        st.metric("Total Gross",          f"${total_gross:,.2f}")

    st.divider()

    if st.session_state.checks:
        rows_html = ""
        for c in reversed(st.session_state.checks):
            rows_html += f"""
            <tr>
                <td class="col-date">{c["date"].strftime("%m/%d/%Y")}</td>
                <td class="col-check">${c['amount']:,.2f}</td>
                <td class="col-tax">${c['reserve']:,.2f}</td>
                <td class="col-keep">${c['remaining']:,.2f}</td>
            </tr>"""
        st.markdown(f"""
        <table class="deco-table">
            <thead><tr>
                <th>Date</th><th>Check Total</th>
                <th>Tax Reserve</th><th>Remaining Spendable</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)
    else:
        st.info("No checks logged yet. Add your first check above.")

elif page == "Allocation Matrix":

    st.header("Allocation Matrix")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Budget Planner</div>', unsafe_allow_html=True)

    monthly_income = projected_annual / 12

    categories = {
        "Tax Obligation":    annual_total_tax / 12,
        "Monthly Bills":     monthly_bills_total,
        "Weekly Bills":      st.session_state.weekly_bills * 4,
        "Business Expenses": total_deductions / 12,
        "Discretionary":     max(monthly_take_home, 0),
    }
    total_allocated = sum(categories.values())

    colors = ["#8b1a1a", "#c8a84c", "#2d4a7a", "#5a3a1a", "#2d7a6b"]

    col_chart, col_list = st.columns([2, 3])

    with col_chart:
        if monthly_income > 0:
            fig = go.Figure(go.Pie(
                labels=list(categories.keys()),
                values=list(categories.values()),
                hole=0.6,
                marker=dict(colors=colors, line=dict(color='#000000', width=2)),
                textinfo='none',
                hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>',
            ))
            fig.add_annotation(
                text="10/99",
                font=dict(family="Cinzel, serif", size=14, color="#c8a84c"),
                showarrow=False
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=280,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Log income to see your allocation matrix.")

    with col_list:
        rows_html = ""
        for (label, amount), color in zip(categories.items(), colors):
            pct = (amount / monthly_income * 100) if monthly_income > 0 else 0
            rows_html += f"""
            <tr>
                <td style="color:{color};font-size:0.65rem;letter-spacing:0.1em;padding:0.6rem 0.5rem 0.6rem 0;border-bottom:1px solid #0d0d09;text-transform:uppercase;font-weight:700;">{label}</td>
                <td style="color:#4a4228;font-size:0.62rem;padding:0.6rem 0.5rem;border-bottom:1px solid #0d0d09;text-align:right;">{pct:.1f}%</td>
                <td style="color:{color};font-size:0.82rem;font-weight:600;padding:0.6rem 0 0.6rem 0.5rem;border-bottom:1px solid #0d0d09;text-align:right;">${amount:,.2f}</td>
            </tr>"""
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;font-family:'Josefin Sans',sans-serif;margin-top:1rem;">
            <thead><tr>
                <th style="color:#c8a84c;font-size:0.55rem;letter-spacing:0.16em;text-transform:uppercase;padding:0 0.5rem 0.6rem 0;text-align:left;border-bottom:1px solid #c8a84c;">Category</th>
                <th style="color:#c8a84c;font-size:0.55rem;letter-spacing:0.16em;text-transform:uppercase;padding:0 0.5rem 0.6rem 0.5rem;text-align:right;border-bottom:1px solid #c8a84c;">%</th>
                <th style="color:#c8a84c;font-size:0.55rem;letter-spacing:0.16em;text-transform:uppercase;padding:0 0 0.6rem 0.5rem;text-align:right;border-bottom:1px solid #c8a84c;">Monthly</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)

elif page == "Mandatory Extraction":

    st.header("Mandatory Extraction")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Tax Planning</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric("Projected Annual Gross",  f"${projected_annual:,.2f}")
        st.metric("Arizona State Tax",       f"${arizona_state_tax:,.2f}")
        st.metric("Self-Employment Tax",     f"${self_employment_tax:,.2f}")
        st.metric("Federal Income Tax",      f"${federal_income_tax:,.2f}")
    with col_t2:
        st.metric("Total Annual Tax",        f"${annual_total_tax:,.2f}")
        st.metric("Quarterly Payment",       f"${quarterly_payment:,.2f}")
        st.metric("Weekly Tax Reserve",      f"${weekly_tax_reserve:,.2f}")
        effective = (annual_total_tax / projected_annual * 100) if projected_annual > 0 else 0
        st.metric("Effective Rate",          f"{effective:.1f}%")

    st.divider()

    q_label, q_date, q_days = next_deadline()
    if q_days is not None:
        color = "#8b1a1a" if q_days <= 30 else "#c8a84c"
        st.markdown(
            f'<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.65rem;'
            f'letter-spacing:0.12em;text-transform:uppercase;color:{color};padding:1rem;'
            f'border:1px solid #111108;border-left:3px solid {color};">'
            f'⚠ {q_label} Estimated Payment — ${quarterly_payment:,.2f} — Due in {q_days} Days'
            f'</div>',
            unsafe_allow_html=True
        )

elif page == "Reserve Vault":

    st.header("Reserve Vault")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Monthly Bills</div>', unsafe_allow_html=True)

    with st.expander("Add Monthly Bill", expanded=True):
        bill_name     = st.text_input("Bill Name", placeholder="Netflix, Insurance, GitHub, Credit Card")
        bill_amount   = st.number_input("Monthly Amount", min_value=0.0, step=1.0)
        bill_due_date = st.date_input("Due Date")

        if st.button("Add Bill"):
            if bill_name and bill_amount > 0:
                new_bill = {"name": bill_name, "amount": bill_amount, "due_date": bill_due_date}
                new_bill = add_bill_to_db(new_bill)
                st.session_state.monthly_bills.append(new_bill)
                st.rerun()
            else:
                st.warning("Enter a bill name and amount.")

    col_mb1, col_mb2 = st.columns(2)
    with col_mb1:
        st.metric("Monthly Bills Total",             f"${monthly_bills_total:,.2f}")
    with col_mb2:
        st.metric("Weekly Reserve for Monthly Bills", f"${weekly_monthly_bill_reserve:,.2f}")

    if st.session_state.monthly_bills:
        st.divider()
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
                if st.button("Delete", key=f"del_{index}"):
                    delete_bill_from_db(bill["id"])
                    st.session_state.monthly_bills.pop(index)
                    st.rerun()

elif page == "Ledger Archives":

    st.header("Ledger Archives")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Reports & History</div>', unsafe_allow_html=True)

    if st.session_state.checks:
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Checks Logged", len(st.session_state.checks))
        with col_s2:
            st.metric("Total Gross",         f"${total_gross:,.2f}")
        with col_s3:
            st.metric("Total Reserved",      f"${total_se_account + total_fed_account + total_state_account:,.2f}")
        with col_s4:
            st.metric("Avg Weekly Check",    f"${avg_check:,.2f}")

        st.divider()

        rows_html = ""
        for c in reversed(st.session_state.checks):
            rows_html += f"""
            <tr>
                <td class="col-date">{c["date"].strftime("%m/%d/%Y")}</td>
                <td class="col-check">${c['amount']:,.2f}</td>
                <td class="col-tax">${c['se']:,.2f}</td>
                <td class="col-tax">${c['fed']:,.2f}</td>
                <td class="col-tax">${c['state']:,.2f}</td>
                <td class="col-tax">${c['reserve']:,.2f}</td>
                <td class="col-keep">${c['remaining']:,.2f}</td>
            </tr>"""
        st.markdown(f"""
        <table class="deco-table">
            <thead><tr>
                <th>Date</th><th>Check</th>
                <th>SE Tax</th><th>Federal</th><th>State</th>
                <th>Total Reserve</th><th>Spendable</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)
    else:
        st.info("No records found. Log your first check in Income Log.")

elif page == "System Settings":

    st.header("System Settings")
    st.markdown('<div style="font-family:\'Josefin Sans\',sans-serif;font-size:0.55rem;letter-spacing:0.16em;color:#4a4228;text-transform:uppercase;margin-bottom:1.5rem;">Preferences</div>', unsafe_allow_html=True)

    st.subheader("Business Deductions")

    d = st.session_state.deductions
    d["business_miles"]       = st.number_input("Business Miles",        min_value=0.0, step=100.0, value=d["business_miles"])
    d["home_office"]          = st.number_input("Home Office Deduction", min_value=0.0, step=100.0, value=d["home_office"])
    d["tools_equipment"]      = st.number_input("Tools & Equipment",     min_value=0.0, step=100.0, value=d["tools_equipment"])
    d["health_insurance"]     = st.number_input("Health Insurance",      min_value=0.0, step=100.0, value=d["health_insurance"])
    d["professional_services"]= st.number_input("Professional Services", min_value=0.0, step=100.0, value=d["professional_services"])
    d["other"]                = st.number_input("Other Deductions",      min_value=0.0, step=100.0, value=d["other"])

    st.metric("Total Deductions", f"${total_deductions:,.2f}")

    st.divider()
    st.subheader("Weekly Budget")

    st.session_state.weekly_bills = st.number_input(
        "Weekly Bills",
        min_value=0.0,
        step=50.0,
        value=st.session_state.weekly_bills
    )

    st.divider()
    st.subheader("Final Totals")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric("Annual Take Home",  f"${annual_take_home:,.2f}")
    with col_f2:
        st.metric("Monthly Take Home", f"${monthly_take_home:,.2f}")
    with col_f3:
        st.metric("Weekly Spendable",  f"${remaining_weekly:,.2f}")

st.caption("2026 mileage rate: $0.725/mile  ·  Estimates only — not financial advice")
