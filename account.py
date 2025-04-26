import streamlit as st

def calculate_monthly_saving_with_wait(current_age, saving_years, pension_start_age, target_monthly_pension, retirement_years, annual_return, inflation):
    r = annual_return / 100 / 12  # 월 수익률
    i = inflation / 100  # 연 물가상승률
    saving_months = saving_years * 12
    waiting_years = pension_start_age - (current_age + saving_years)
    total_waiting_months = waiting_years * 12

    # 1. 연금 개시 시점의 첫 월 연금액 계산 (물가상승 반영)
    years_until_pension = pension_start_age - current_age
    first_pension = target_monthly_pension * ((1 + i) ** years_until_pension)

    # 2. 연금 수령 총액 계산 (물가연동 연금 흐름)
    if abs(annual_return - inflation) < 1e-6:
        # 수익률과 물가상승률이 같으면 등비수열 대신 단순합
        pv_needed = first_pension * retirement_years * 12
    else:
        g = (1 + i) / (1 + annual_return / 100)
        pv_needed = first_pension * (1 - g ** (retirement_years)) / (1 - g)
        pv_needed = pv_needed * 12  # 월 단위 환산

    # 3. 저축이 끝난 이후, 거치기간 동안 이자 복리로 불림
    if total_waiting_months > 0:
        pv_needed = pv_needed / ((1 + r) ** total_waiting_months)

    # 4. 목표 금액(pv_needed)을 만들기 위한 매달 저축액 계산
    monthly_saving = pv_needed * r / ((1 + r) ** saving_months - 1)

    return round(monthly_saving)

# --- Streamlit 인터페이스 ---

st.markdown("### 📊 목표 연금 기반 저축 계산기 (거치기간 포함, 물가연동 연금 수령)")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)
st.caption("연금 개시 시점에 필요한 목표 금액을 정확히 계산하고, 저축 기간 동안 매달 저축할 금액을 구합니다.")

# 입력값
current_age = st.number_input("현재 나이", min_value=0, value=30)
saving_years = st.number_input("저축 기간 (년)", min_value=1, value=20)
pension_start_age = st.number_input("연금 개시 나이", min_value=current_age+saving_years, value=60)
target_monthly_pension = st.number_input("원하는 월 연금 수령액 (만원, 현재 가치)", min_value=0, value=200, step=10)
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
annual_return = st.number_input("연 수익률 (%)", min_value=0.0, value=2.7)
inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.7)

# 계산
if st.button("🧮 계산하기"):
    result = calculate_monthly_saving_with_wait(
        current_age,
        saving_years,
        pension_start_age,
        target_monthly_pension * 10000,
        retirement_years,
        annual_return,
        inflation
    )
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 저축 후 거치기간 동안 이자를 굴리고, 연금 개시 시점부터 매년 물가상승률만큼 연금액이 증가하는 구조를 반영했습니다.")
