import streamlit as st
import requests

st.set_page_config(
    page_title="AI Procurement Intelligence",
    layout="wide"
)

st.title("AI Procurement Intelligence")

st.markdown(
    "Evaluate suppliers and procurement risk using AI."
)

col1, col2 = st.columns(2)

with col1:

    supplier_name = st.text_input(
        "Supplier Name"
    )

    rating = st.slider(
        "Supplier Rating",
        0.0,
        5.0,
        4.0
    )

with col2:

    delay = st.number_input(
        "Delivery Delay %",
        0,
        100,
        10
    )

    country = st.text_input(
        "Country"
    )

if st.button("Analyze Supplier"):

    payload = {
        "name": supplier_name,
        "rating": rating,
        "delivery_delay": delay,
        "country": country
    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/evaluate",
            json=payload
        )

        result = response.json()

        st.subheader("📊 Results")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Supplier Score",
                result["supplier_score"]
            )

        with c2:
            st.metric(
                "Risk Score",
                result["risk_score"]
            )

        with c3:
            st.metric(
                "Category",
                result["risk_category"]
            )

        st.success(
            result["recommendation"]
        )

    except Exception as e:

        st.error(
            f"API Error: {e}"
        )