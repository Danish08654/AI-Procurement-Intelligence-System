import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="AI Procurement Intelligence", page_icon="📦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, body { font-family: 'Inter', sans-serif; }

/* ── background ── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.block-container, [data-testid="stVerticalBlock"] {
    background: #f8fafc !important;
}
section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── global text ── */
p, div, span, label { color: #1e293b !important; }
h1, h2, h3 { color: #0f172a !important; }
.stMarkdown p { color: #1e293b !important; }

/* ── form labels ── */
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label { color: #374151 !important; font-weight: 500 !important; font-size: 0.875rem !important; }

/* ── inputs ── */
.stTextInput input {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important; }
.stTextInput input::placeholder { color: #94a3b8 !important; }

.stNumberInput input {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* ── selectbox ── */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
}
.stSelectbox svg { fill: #64748b !important; }

/* ── slider ── */
.stSlider > div > div > div > div { background: #3b82f6 !important; }
.stSlider [data-testid="stTickBar"] { color: #64748b !important; }
[data-testid="stSlider"] label { color: #374151 !important; }

/* ── button ── */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: #1d4ed8 !important;
}

/* ── divider ── */
hr { border-color: #e2e8f0 !important; }

/* ── section header ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 12px;
}

/* ── cards ── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.metric-lbl { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: #64748b; margin-bottom: 6px; }
.metric-val { font-size: 2rem; font-weight: 700; line-height: 1; }
.metric-sub { font-size: 0.85rem; color: #94a3b8; }

/* ── badge ── */
.badge { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.badge-green  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.badge-yellow { background: #fef9c3; color: #a16207; border: 1px solid #fde68a; }
.badge-red    { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

/* ── recommendation ── */
.rec-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    padding: 16px 20px;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #1e3a5f;
}

/* ── issue rows ── */
.row-green  { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3px solid #16a34a; border-radius: 7px; padding: 10px 14px; margin-bottom: 7px; font-size: 0.85rem; color: #14532d; line-height: 1.55; }
.row-red    { background: #fff1f2; border: 1px solid #fecaca; border-left: 3px solid #dc2626; border-radius: 7px; padding: 10px 14px; margin-bottom: 7px; font-size: 0.85rem; color: #7f1d1d; line-height: 1.55; }
.row-blue   { background: #eff6ff; border: 1px solid #bfdbfe; border-left: 3px solid #2563eb; border-radius: 7px; padding: 10px 14px; margin-bottom: 7px; font-size: 0.85rem; color: #1e3a5f; line-height: 1.55; }

/* ── form container ── */
[data-testid="stForm"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 24px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.05) !important;
}
</style>
""", unsafe_allow_html=True)


def get_client():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: st.error("Add GROQ_API_KEY to Streamlit Secrets."); st.stop()

def evaluate(supplier_name, rating, delay, country, category, contract_value):
    client = get_client()
    prompt = f"""You are a procurement risk analyst. Evaluate this supplier and return ONLY valid JSON, no markdown.

Supplier details:
- Name: {supplier_name}
- Country: {country}
- Category: {category}
- Rating: {rating}/5.0
- Delivery Delay: {delay}%
- Contract Value: ${contract_value:,}

Return exactly this JSON:
{{
  "supplier_score": <integer 0-100>,
  "risk_score": <integer 0-100>,
  "risk_category": "Low" | "Medium" | "High",
  "recommendation": "2-3 sentence recommendation",
  "strengths": ["strength1", "strength2", "strength3"],
  "risks": ["risk1", "risk2", "risk3"],
  "action_items": ["action1", "action2", "action3"]
}}

Scoring: supplier_score higher = better. risk_score higher = more risky.
Be specific — reference the supplier name, country, and numbers provided."""

    raw = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2, max_tokens=900
    ).choices[0].message.content.strip()

    if "```" in raw:
        raw = raw.split("```")[1].lstrip("json")
    return json.loads(raw.strip().rstrip("`"))


# ── header ──
st.markdown("## 📦 AI Procurement Intelligence")
st.caption("Evaluate suppliers and assess procurement risk using AI.")
st.divider()

# ── form ──
with st.form("supplier_form"):
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="section-label">Supplier Details</div>', unsafe_allow_html=True)
        supplier_name  = st.text_input("Supplier Name",  placeholder="e.g. Shenzhen Electronics Co.")
        country        = st.text_input("Country",         placeholder="e.g. Germany")
        category       = st.selectbox("Category", [
            "Raw Materials", "Electronics", "Logistics",
            "Software", "Manufacturing", "Services", "Other"
        ])

    with c2:
        st.markdown('<div class="section-label">Performance Metrics</div>', unsafe_allow_html=True)
        rating         = st.slider("Supplier Rating", 0.0, 5.0, 4.0, 0.1)
        delay          = st.slider("Delivery Delay %", 0, 100, 10)
        contract_value = st.number_input("Contract Value (USD)", min_value=0, value=50000, step=5000)

    submitted = st.form_submit_button("Analyze Supplier →", use_container_width=True)

# ── results ──
if submitted:
    if not supplier_name or not country:
        st.warning("Please fill in Supplier Name and Country.")
        st.stop()

    with st.spinner("Analyzing supplier…"):
        try:
            r = evaluate(supplier_name, rating, delay, country, category, contract_value)
        except json.JSONDecodeError:
            st.error("Couldn't parse AI response. Try again."); st.stop()
        except Exception as e:
            st.error(f"Error: {e}"); st.stop()

    st.divider()
    st.markdown("### Analysis Results")

    risk_cat  = r.get("risk_category", "Medium")
    badge_cls = {"Low": "badge-green", "Medium": "badge-yellow", "High": "badge-red"}.get(risk_cat, "badge-yellow")

    def score_color(s): return "#16a34a" if s >= 70 else "#d97706" if s >= 40 else "#dc2626"

    # ── score cards ──
    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        sc = r.get("supplier_score", 0)
        st.markdown(f"""<div class="card">
            <div class="metric-lbl">Supplier Score</div>
            <div class="metric-val" style="color:{score_color(sc)};">{sc}
                <span class="metric-sub">/100</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with m2:
        rc = r.get("risk_score", 0)
        st.markdown(f"""<div class="card">
            <div class="metric-lbl">Risk Score</div>
            <div class="metric-val" style="color:{score_color(100-rc)};">{rc}
                <span class="metric-sub">/100</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="card">
            <div class="metric-lbl">Risk Category</div>
            <div style="margin-top:10px;">
                <span class="badge {badge_cls}">{risk_cat} Risk</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── recommendation ──
    st.markdown(f'<div class="rec-box">💡 {r.get("recommendation", "")}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── details ──
    d1, d2, d3 = st.columns(3, gap="large")
    with d1:
        st.markdown("**✅ Strengths**")
        for s in r.get("strengths", []):
            st.markdown(f'<div class="row-green">{s}</div>', unsafe_allow_html=True)
    with d2:
        st.markdown("**⚠️ Risks**")
        for s in r.get("risks", []):
            st.markdown(f'<div class="row-red">{s}</div>', unsafe_allow_html=True)
    with d3:
        st.markdown("**📋 Action Items**")
        for s in r.get("action_items", []):
            st.markdown(f'<div class="row-blue">{s}</div>', unsafe_allow_html=True)
