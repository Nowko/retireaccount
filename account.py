import streamlit as st

def calculate_monthly_saving(target_monthly_pension, saving_years, retirement_years, rate_return, inflation):
    r = (rate_return - inflation) / 100 / 12  # 실질 수익률 (월 단위)
    n = saving_years * 12
    m = retirement_years * 12

    # 연금 수령 총액 (현재 가치 기준)
    pv_needed = target_monthly_pension * ((1 - (1 + r) ** -m) / r)

    # 매달 저축해야 할 금액 계산 (현재 가치 기준)
    monthly_saving = pv_needed * r / ((1 + r) ** n - 1)

    return round(monthly_saving)

st.title("💸 목표 연금 기반 저축 계산기")
st.caption("현재 가치 기준으로 원하는 연금을 받으려면 매달 얼마나 저축해야 할까요?")

# 입력값 받기
target_monthly_pension = st.number_input("원하는 월 연금 수령액 (만원)", min_value=0, value=200, step=10)
saving_years = st.number_input("저축 기간 (년)", min_value=1, value=20)
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
rate_return = st.number_input("연 수익률 (%)", min_value=0.0, value=3.0)
inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.0)

# 계산 버튼
if st.button("💰 계산하기"):
    result = calculate_monthly_saving(target_monthly_pension * 10000, saving_years, retirement_years, rate_return, inflation)
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 현재 가치 기준이며, 실질 수익률(수익률 - 물가상승률)을 적용한 결과입니다.")
