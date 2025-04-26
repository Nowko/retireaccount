import streamlit as st
import pandas as pd

def calculate_required_pv(future_monthly_pension, retirement_years, annual_return, annual_inflation):
    pv_needed = 0
    current_annual_pension = future_monthly_pension * 12

    for year in range(retirement_years):
        discounted = current_annual_pension / ((1 + annual_return / 100) ** year)
        pv_needed += discounted
        current_annual_pension *= (1 + annual_inflation / 100)

    return pv_needed

def calculate_monthly_saving_with_deposit_then_wait(
    current_age, pension_start_age, saving_years,
    target_monthly_pension_now, retirement_years,
    annual_return, annual_inflation):

    monthly_return = annual_return / 100 / 12
    years_until_pension = pension_start_age - current_age
    waiting_years = years_until_pension - saving_years
    saving_months = saving_years * 12
    waiting_months = waiting_years * 12

    # 연금 개시 시점의 첫 월 연금 계산 (물가상승 반영)
    future_monthly_pension = target_monthly_pension_now * ((1 + annual_inflation / 100) ** years_until_pension)

    # ✨ 수정된 연금개시 시점 필요 일시금 계산
    pv_needed = calculate_required_pv(
        future_monthly_pension,
        retirement_years,
        annual_return,
        annual_inflation
    )

    # 저축 종료 후 거치기간 동안 할인
    if waiting_months > 0:
        pv_needed /= (1 + monthly_return) ** waiting_months

    # 저축 기간 동안 매달 저축해야 할 금액 계산
    monthly_saving = pv_needed * monthly_return / ((1 + monthly_return) ** saving_months - 1)

    return round(monthly_saving), round(future_monthly_pension), round(pv_needed)

def generate_pension_table(first_monthly_pension, years, inflation_rate):
    data = []
    for year in range(1, years + 1):
        monthly_pension = first_monthly_pension * ((1 + inflation_rate / 100) ** (year - 1))
        annual_pension = monthly_pension * 12
        data.append({
            "연차": f"{year}년차",
            "예상 월 연금": f"{monthly_pension / 10000:,.0f}만원",
            "연간 합계": f"{annual_pension / 10000:,.0f}만원"
        })
    return pd.DataFrame(data)

# --- Streamlit UI ---

st.markdown("### 📊 연금 준비 계산기 (정확한 일시금 계산 반영)")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)

st.caption("현재 나이와 원하는 연금 수령 조건을 입력하면, 저축 + 거치 구조로 매달 얼마를 저축해야 하는지를 계산하고, 정확한 연금 흐름을 제공합니다.")

# ✅ 입력
current_age = st.number_input("현재 나이", min_value=0, value=30)
target_monthly_pension_now = st.number_input("원하는 월 연금 수령액 (만원, 현재 가치)", min_value=0, value=200, step=10)
pension_start_age = st.number_input("연금 개시 나이", min_value=current_age+1, value=60)

saving_period_limit = pension_start_age - current_age
saving_years = st.number_input(
    "저축 기간 (년)", 
    min_value=1, 
    max_value=saving_period_limit, 
    value=min(20, saving_period_limit)
)

retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
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
        # ✨ 여기부터 추가
    waiting_years = pension_start_age - (current_age + saving_years)
    if waiting_years > 0:
        waiting_text = f"{waiting_years}년 동안 거치하여 "
    else:
        waiting_text = ""
    st.caption(f"※ {saving_years}년간 저축 후 {waiting_text}연 {annual_return:.1f}% 수익률로 불려, "
               f"{retirement_years}년간 물가상승률 {annual_inflation:.1f}% 반영 연금을 수령하는 구조입니다.")
    # ✨ 여기까지

    st.markdown("---")
    st.markdown(f"🧾 연금 개시 시점의 월 연금: **{future_monthly_pension / 10000:,.0f}만원**")
    st.markdown(f"💰 연금 개시 시점에 필요 일시금: **{pv_needed / 10000:,.0f}만원**")

    # 📋 연금 흐름표
    st.markdown("### 📋 연금 흐름표 (물가상승률 반영)")
    df_pension = generate_pension_table(future_monthly_pension, retirement_years, annual_inflation)
    st.dataframe(df_pension, use_container_width=True)
