import streamlit as st

def calculate_required_monthly_saving(current_age, target_monthly_pension_now, pension_start_age,
                                       saving_years, retirement_years,
                                       annual_return, annual_inflation):
    # 월 수익률과 월 물가상승률 계산
    monthly_return = annual_return / 100 / 12
    monthly_inflation = annual_inflation / 100 / 12

    # 1. 연금개시 시점의 월 연금 수령액 (물가상승 반영)
    years_until_pension = pension_start_age - current_age
    future_monthly_pension = target_monthly_pension_now * ((1 + annual_inflation / 100) ** years_until_pension)

    # 2. 연금 수령 흐름 전체를 현재가치로 계산
    if abs(annual_return - annual_inflation) < 1e-6:
        # 수익률과 물가상승률이 같으면 특별 계산 (단순합)
        pv_needed = future_monthly_pension * retirement_years * 12
    else:
        g = (1 + annual_inflation / 100) / (1 + annual_return / 100)
        pv_needed = future_monthly_pension * (1 - g ** (retirement_years)) / (1 - g)
        pv_needed = pv_needed * 12  # 월 단위 환산

    # 3. 거치기간 동안 할인
    waiting_years = pension_start_age - (current_age + saving_years)
    waiting_months = waiting_years * 12

    if waiting_months > 0:
        pv_needed = pv_needed / ((1 + monthly_return) ** waiting_months)

    # 4. 저축기간 동안 필요한 월 저축액 계산
    saving_months = saving_years * 12
    monthly_saving = pv_needed * monthly_return / ((1 + monthly_return) ** saving_months - 1)

    return round(monthly_saving)

# --- Streamlit 화면 구성 ---

st.markdown("### 📊 목표 연금 기반 저축 계산기 (거치기간 포함, 물가연동 연금 수령)")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)
st.caption("현재 나이, 원하는 연금 수령액 등을 입력하면, 저축 기간 동안 매달 얼마를 저축해야 하는지 계산합니다.")

# ✅ 입력 순서 (요청하신 순서 반영)
current_age = st.number_input("현재 나이", min_value=0, value=30)
target_monthly_pension_now = st.number_input("원하는 월 연금 수령액 (만원, 현재 가치)", min_value=0, value=200, step=10)
pension_start_age = st.number_input("연금 개시 나이", min_value=current_age+1, value=60)
saving_years = st.number_input("저축 기간 (년)", min_value=1, value=20)
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
annual_return = st.number_input("연 수익률 (%)", min_value=0.0, value=2.7)
annual_inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.1)

# 계산
if st.button("🧮 계산하기"):
    result = calculate_required_monthly_saving(
        current_age,
        target_monthly_pension_now * 10000,
        pension_start_age,
        saving_years,
        retirement_years,
        annual_return,
        annual_inflation
    )
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 저축 후 거치기간 동안 복리로 불리고, 연금 개시 시점부터 매월 물가상승률만큼 연금이 인상되는 구조를 반영했습니다.")
