import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="AI Procurement Intelligence", page_icon="📦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, body { font-family: 'Inter', sans-serif; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container
    { background: #0f172a !important; }
section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div
    { background: #1e293b !important; border-right: 1px solid #334155 !important; }
#MainMenu, footer, header { visibility: hidden; }
p, label, span, div { color: #cbd5e1; }
h1, h2, h3 { color: #f1f5f9 !important; }

.card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px 24px; margin-bottom: 14px; }
.metric-val { font-size: 2rem; font-weight: 700; color: #f1f5f9; margin: 4px 0; }
.metric-lbl { font-size: 0.72rem; text-transform: uppercase; letter-spacing: .08em; color: #64748b; }
.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
.green  { background: rgba(34,197,94,.1);  color: #22c55e; border: 1px solid rgba(34,197,94,.25); }
.yellow { background: rgba(245,158,11,.1); color: #f59e0b; border: 1px solid rgba(245,158,11,.25); }
.red    { background: rgba(239,68,68,.1);  color: #ef4444; border: 1px solid rgba(239,68,68,.25); }
.rec-box { background: #0f2744; border: 1px solid #1d4ed8; border-left: 3px solid #3b82f6; border-radius: 10px; padding: 16px 20px; font-size: 0.9rem; line-height: 1.7; color: #e2e8f0; }

.stTextInput input { background: #1e293b !important; color: #f1f5f9 !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
.stNumberInput input { background: #1e293b !important; color: #f1f5f9 !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
.stSlider { color: #f1f5f9 !important; }
.stButton > button { background: #3b82f6 !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 10px !important; }
.stButton > button:hover { background: #2563eb !important; }
.stSelectbox > div > div { background: #1e293b !important; border-color: #334155 !important; color: #f1f5f9 !important; }
hr { border-color: #334155 !important; }
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
  "strengths": ["strength1", "strength2"],
  "risks": ["risk1", "risk2"],
  "action_items": ["action1", "action2"]
}}

Scoring logic:
- supplier_score: higher is better (based on rating, low delay, stable country)
- risk_score: higher means more risk (based on delay, country risk, low rating)
- Be specific and actionable in recommendations"""

    raw = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
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
        st.markdown("**Supplier Details**")
        supplier_name   = st.text_input("Supplier Name", placeholder="e.g. Acme Corp")
        country         = st.text_input("Country",        placeholder="e.g. Germany")
        category        = st.selectbox("Category", [
            "Raw Materials", "Electronics", "Logistics",
            "Software", "Manufacturing", "Services", "Other"
        ])

    with c2:
        st.markdown("**Performance Metrics**")
        rating          = st.slider("Supplier Rating", 0.0, 5.0, 4.0, 0.1)
        delay           = st.slider("Delivery Delay %", 0, 100, 10)
        contract_value  = st.number_input("Contract Value (USD)", min_value=0, value=50000, step=5000)

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
    st.markdown("### Results")

    # scores
    risk_cat  = r.get("risk_category", "Medium")
    badge_cls = {"Low": "green", "Medium": "yellow", "High": "red"}.get(risk_cat, "yellow")
    score_color = lambda s: "#22c55e" if s >= 70 else "#f59e0b" if s >= 40 else "#ef4444"

    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        sc = r.get("supplier_score", 0)
        st.markdown(f'<div class="card"><div class="metric-lbl">Supplier Score</div>'
                    f'<div class="metric-val" style="color:{score_color(sc)};">{sc}<span style="font-size:1rem;color:#64748b;">/100</span></div></div>',
                    unsafe_allow_html=True)
    with m2:
        rc = r.get("risk_score", 0)
        st.markdown(f'<div class="card"><div class="metric-lbl">Risk Score</div>'
                    f'<div class="metric-val" style="color:{score_color(100-rc)};">{rc}<span style="font-size:1rem;color:#64748b;">/100</span></div></div>',
                    unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="card"><div class="metric-lbl">Risk Category</div>'
                    f'<div style="margin-top:10px;"><span class="badge {badge_cls}">{risk_cat} Risk</span></div></div>',
                    unsafe_allow_html=True)

    # recommendation
    st.markdown(f'<div class="rec-box">💡 {r.get("recommendation","")}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # details
    d1, d2, d3 = st.columns(3, gap="large")
    with d1:
        st.markdown("**✅ Strengths**")
        for s in r.get("strengths", []):
            st.markdown(f'<div style="background:#1e293b;border:1px solid #334155;border-left:3px solid #22c55e;border-radius:6px;padding:10px 14px;margin-bottom:6px;font-size:0.84rem;">{s}</div>', unsafe_allow_html=True)
    with d2:
        st.markdown("**⚠️ Risks**")
        for s in r.get("risks", []):
            st.markdown(f'<div style="background:#1e293b;border:1px solid #334155;border-left:3px solid #ef4444;border-radius:6px;padding:10px 14px;margin-bottom:6px;font-size:0.84rem;">{s}</div>', unsafe_allow_html=True)
    with d3:
        st.markdown("**📋 Action Items**")
        for s in r.get("action_items", []):
            st.markdown(f'<div style="background:#1e293b;border:1px solid #334155;border-left:3px solid #3b82f6;border-radius:6px;padding:10px 14px;margin-bottom:6px;font-size:0.84rem;">{s}</div>', unsafe_allow_html=True)
