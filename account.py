import streamlit as st

def calculate_monthly_saving_with_inflation(target_monthly_pension, current_age, pension_start_age, retirement_years, rate_return, inflation):
    r = rate_return / 100 / 12  # 월 수익률
    i = inflation / 100  # 연 물가상승률 (연 기준)
    n_total = (pension_start_age - current_age) * 12  # 저축 및 거치 총 기간
    n_saving = n_total
    m = retirement_years  # 연금 수령 기간 (연 기준)

    # 연금 시작 시점 첫 연금 금액 (물가상승 반영)
    first_pension = target_monthly_pension * ((1 + i) ** (pension_start_age - current_age))

    # 연금 수령 전체 총액 계산 (매년 연금 인상 반영 - 등비수열 합 공식 사용)
    # 연금 수령 연 단위 계산 → 월로 환산
    if abs(rate_return - inflation) < 1e-6:
        # 수익률과 물가상승률이 거의 같을 경우, 등비수열 수렴 문제를 방지
        pv_needed = first_pension * m / ((1 + rate_return / 100) ** (pension_start_age - current_age))
    else:
        g = (1 + i) / (1 + rate_return / 100)  # 물가상승과 수익률을 비교
        pv_needed = first_pension * (1 - g ** m) / (1 - g)
        pv_needed = pv_needed / ((1 + rate_return / 100) ** (pension_start_age - current_age))  # 현재 시점 가치로 환산

    # 미래 가치 기준으로 필요한 금액
    fv_needed = pv_needed * (1 + r) ** n_total

    # 매달 저축할 금액
    monthly_saving = fv_needed * r / ((1 + r) ** n_saving - 1)

    return round(monthly_saving)

# Streamlit 인터페이스
st.markdown("### 📊 목표 연금 기반 저축 계산기 (물가연동 수령 포함)")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)
st.caption("연금 시작 시 현재 가치로 수령하고, 매년 물가상승률만큼 연금액이 인상되는 구조입니다.")

# 입력
current_age = st.number_input("현재 나이", min_value=0, value=30)
pension_start_age = st.number_input("연금 시작 나이", min_value=current_age+1, value=60)
target_monthly_pension = st.number_input("원하는 월 연금 수령액 (만원, 현재 가치)", min_value=0, value=200, step=10)
retirement_years = st.number_input("연금 수령 기간 (년)", min_value=1, value=30)
rate_return = st.number_input("연 수익률 (%)", min_value=0.0, value=3.0)
inflation = st.number_input("연 물가상승률 (%)", min_value=0.0, value=2.0)

# 계산
if st.button("🧮 계산하기"):
    result = calculate_monthly_saving_with_inflation(
        target_monthly_pension * 10000,
        current_age,
        pension_start_age,
        retirement_years,
        rate_return,
        inflation
    )
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 현재 가치 기준으로 첫 연금 수령 후, 매년 물가 상승률만큼 연금이 인상되는 것을 반영한 결과입니다.")
