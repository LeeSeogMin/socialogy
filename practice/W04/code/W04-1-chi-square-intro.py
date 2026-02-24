"""
W04-A 카이제곱 검정 개념 소개
=============================
교차표와 카이제곱 독립성 검정의 핵심 개념을 단일 변수 쌍(성별 × 지지정당)으로
단계별로 학습한다.

학습 흐름:
  1단계: 교차표(분할표) 만들기
  2단계: 카이제곱 검정 실행 및 결과 해석
  3단계: 효과 크기(Cramer's V) 계산
  4단계: 기대빈도 가정 점검
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path


def cramers_v(contingency_table: np.ndarray, chi2: float, n: int) -> float:
    """Cramer's V를 계산한다.

    카이제곱 통계량은 표본 크기에 민감하므로,
    관련성의 '강도'를 비교하려면 효과 크기 지표가 필요하다.

    Parameters
    ----------
    contingency_table : np.ndarray
        관측 빈도 교차표.
    chi2 : float
        카이제곱 통계량.
    n : int
        전체 표본 수.

    Returns
    -------
    float
        Cramer's V 값 (0~1).
    """
    r, k = contingency_table.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))


def interpret_cramers_v(v: float) -> str:
    """Cramer's V 값을 해석 기준에 따라 문자열로 반환한다.

    Cohen(1988)의 기준을 참고하되, 사회과학 맥락에 맞게 조정하였다.
    """
    if v < 0.10:
        return "무시할 수준 (negligible)"
    elif v < 0.20:
        return "약한 관련성 (weak)"
    elif v < 0.30:
        return "중간 정도 관련성 (moderate)"
    else:
        return "강한 관련성 (strong)"


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    # ── 데이터 불러오기 ──
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w04.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")

    print("=" * 65)
    print("  W04-A | 카이제곱 검정 개념 소개: 성별 × 지지정당")
    print("=" * 65)

    # ================================================================
    # 1단계: 교차표(분할표) 만들기
    # ================================================================
    print("\n" + "─" * 65)
    print("  1단계: 교차표(분할표) 작성")
    print("─" * 65)

    # 교차표: 행=성별, 열=지지정당, 주변합 포함
    crosstab = pd.crosstab(
        df["성별"], df["지지정당"],
        margins=True, margins_name="합계",
    )
    print("\n[관측 빈도표 (observed frequencies)]")
    print(crosstab)

    # 비율표도 함께 제공 — 패턴을 시각적으로 파악하기 위함
    crosstab_pct = pd.crosstab(
        df["성별"], df["지지정당"],
        normalize="index",  # 행 기준 비율
    ).round(3) * 100
    print("\n[행 비율표 (row percentages, %)]")
    print(crosstab_pct.round(1))

    # ================================================================
    # 2단계: 카이제곱 검정 실행
    # ================================================================
    print("\n" + "─" * 65)
    print("  2단계: 카이제곱 독립성 검정 실행")
    print("─" * 65)

    # margins 제외한 교차표로 검정 수행
    observed = pd.crosstab(df["성별"], df["지지정당"])
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)

    print(f"\n  카이제곱 통계량 (χ²) = {chi2:.4f}")
    print(f"  자유도 (df)          = {dof}")
    print(f"  p-value              = {p_value:.4f}")

    # 기대빈도표 출력 — 관측빈도와 비교하여 차이를 확인
    expected_df = pd.DataFrame(
        expected,
        index=observed.index,
        columns=observed.columns,
    ).round(2)
    print("\n[기대 빈도표 (expected frequencies)]")
    print(expected_df)

    # ================================================================
    # 3단계: 효과 크기 — Cramer's V
    # ================================================================
    print("\n" + "─" * 65)
    print("  3단계: 효과 크기 (Cramér's V)")
    print("─" * 65)

    n = observed.values.sum()
    v = cramers_v(observed.values, chi2, n)

    print(f"\n  Cramér's V = {v:.4f}")
    print(f"  해석: {interpret_cramers_v(v)}")

    # ================================================================
    # 4단계: 기대빈도 가정 점검
    # ================================================================
    print("\n" + "─" * 65)
    print("  4단계: 기대빈도 가정 점검")
    print("─" * 65)

    # 카이제곱 검정의 전제: 모든 셀의 기대빈도가 5 이상이어야 한다.
    # 기대빈도가 5 미만인 셀이 20% 이상이면 검정 결과를 신뢰하기 어렵다.
    min_expected = expected.min()
    cells_below_5 = (expected < 5).sum()
    total_cells = expected.size

    print(f"\n  최소 기대빈도       = {min_expected:.2f}")
    print(f"  기대빈도 < 5 인 셀  = {cells_below_5}개 / {total_cells}개")

    if cells_below_5 == 0:
        print("  → 모든 셀의 기대빈도 ≥ 5: 카이제곱 검정 가정 충족")
    else:
        pct_below = cells_below_5 / total_cells * 100
        print(f"  → 기대빈도 < 5 비율: {pct_below:.1f}%")
        if pct_below > 20:
            print("  → 20% 초과: Fisher 정확 검정 등 대안 고려 필요")
        else:
            print("  → 20% 이하: 카이제곱 검정 결과를 사용할 수 있음")

    # ================================================================
    # 종합 해석
    # ================================================================
    print("\n" + "─" * 65)
    print("  종합 해석")
    print("─" * 65)

    alpha = 0.05
    if p_value < alpha:
        sig_text = f"유의수준 {alpha}에서 통계적으로 유의미하다"
        decision = "귀무가설(H₀: 두 변수는 독립이다)을 기각한다."
    else:
        sig_text = f"유의수준 {alpha}에서 통계적으로 유의미하지 않다"
        decision = "귀무가설(H₀: 두 변수는 독립이다)을 기각할 수 없다."

    print(f"""
  분석 대상: 성별 × 지지정당
  ─────────────────────────────
  χ²({dof}) = {chi2:.4f}, p = {p_value:.4f}
  Cramér's V = {v:.4f} ({interpret_cramers_v(v)})

  결론: {sig_text}.
        {decision}

  실질적 의미:
    성별에 따라 지지정당의 분포에 차이가 {'있다' if p_value < alpha else '없다'}고 볼 수 있으며,
    그 관련성의 크기는 Cramér's V = {v:.4f}로 {interpret_cramers_v(v)}에 해당한다.
""")
