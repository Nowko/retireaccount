import streamlit as st

def calculate_monthly_saving(target_monthly_pension, current_age, pension_start_age, retirement_years, rate_return, inflation):
    r = (rate_return - inflation) / 100 / 12  # 실질 수익률 (월)
    n_total = (pension_start_age - current_age) * 12  # 저축 + 거치 총 기간
    n_saving = n_total  # 매달 납입하는 전체 기간 (거치 없이 끝까지 납입한다고 가정)
    m = retirement_years * 12  # 연금 수령 월 수

    # 현재 가치 기준으로 연금 수령 총액
    pv_needed = target_monthly_pension * ((1 - (1 + r) ** -m) / r)

    # 미래 가치 기준으로 목표 금액 (현재가치를 미래로 이월)
    fv_needed = pv_needed * (1 + r) ** n_total

    # 매달 저축할 금액 계산
    monthly_saving = fv_needed * r / ((1 + r) ** n_saving - 1)

    return round(monthly_saving)

st.title("📊 목표 연금 기반 저축 계산기 (거치기간 포함)")
st.caption("지금부터 연금 시작 시점까지 이자가 붙는 기간 전체를 고려해 계산합니다.")

# 입력값
current_age = st.number_input("현재 나이", min_value=0, value=30)
pension_start_age = st.number_input("연금 시작 나이", min_value=current_age+1, value=60)
target_monthly_pension = st.number_input("원하는 월 연금 수령액 (만원)", min_value=0, value=200, step=10)
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
rate_return = st.number_input("연 수익률 (%)", min_value=0.0, value=3.0)
inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.0)

# 계산
if st.button("🧮 계산하기"):
    result = calculate_monthly_saving(
        target_monthly_pension * 10000,
        current_age,
        pension_start_age,
        retirement_years,
        rate_return,
        inflation
    )
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 현재 가치 기준 목표 연금 금액을 달성하기 위해, 전체 투자 기간 동안의 복리 이자까지 고려한 결과입니다.")
