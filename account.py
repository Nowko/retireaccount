import streamlit as st
import pandas as pd

# --- 계산 함수 (생략) ---

# --- Streamlit UI 시작 ---

st.markdown("### 📊 거치형 연금 준비 계산기 (20년 저축 + 10년 거치)")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)

st.caption("현재 나이와 원하는 연금 수령 조건을 입력하면, 저축 + 거치 구조로 매달 얼마를 저축해야 하는지를 계산하고, 연금 흐름을 함께 제공합니다.")

# ✅ 입력
current_age = st.number_input("현재 나이", min_value=0, value=30)
target_monthly_pension_now = st.number_input("원하는 월 연금 수령액 (만원, 현재 가치)", min_value=0, value=200, step=10)
pension_start_age = st.number_input("연금 개시 나이", min_value=current_age+1, value=60)

# ✅ 검증1: 연금 개시 나이는 현재 나이보다 최소 1살 많아야 함
if pension_start_age <= current_age:
    st.error("⛔ 연금 개시 나이는 현재 나이보다 최소 1살 이상 많아야 합니다.")
    st.stop()

# ✅ 검증2: 저축 기간 설정
saving_period_limit = pension_start_age - current_age
saving_years = st.number_input(
    "저축 기간 (년)", 
    min_value=1, 
    max_value=saving_period_limit, 
    value=min(20, saving_period_limit)
)

# ✅ 검증3: 연금 수령 기간 입력
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)

# ✅ 검증4: 수익률 / 물가상승률
annual_return = st.number_input("연 수익률 (%)", min_value=0.0, value=2.0)
annual_inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.0)

# 🧮 계산
if st.button("🧮 계산하기"):
    monthly_saving, future_monthly_pension, pv_needed = calculate_monthly_saving_with_deposit_then_wait(
        current_age,
        pension_start_age,
        saving_years,
        target_monthly_pension_now * 10000,
        retirement_years,
        annual_return,
        annual_inflation
    )
    st.subheader(f"👉 매달 저축해야 할 금액: **{monthly_saving / 10000:,.1f}만 원**")
    st.caption(f"※ 20년간 저축 후 10년 동안 거치하여 연 {annual_return:.1f}% 수익률로 불려, "
               f"{retirement_years}년간 물가상승률 {annual_inflation:.1f}% 반영 연금을 수령하는 구조입니다.")
    st.markdown("---")
    st.markdown(f"🧾 연금 개시 시점의 월 연금: **{future_monthly_pension / 10000:,.0f}만원**")
    st.markdown(f"💰 연금 개시 시점에 필요 일시금: **{pv_needed / 10000:,.0f}만원**")

    # 📋 연금 흐름표
    df_pension = generate_pension_table(future_monthly_pension, retirement_years, annual_inflation)
    st.markdown("### 📋 연금 흐름표 (물가상승률 반영)")
    st.dataframe(df_pension, use_container_width=True)
