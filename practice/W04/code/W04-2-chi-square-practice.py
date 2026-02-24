"""
W04-B 카이제곱 검정 실습 (스튜디오)
====================================
여러 변수 쌍에 대해 카이제곱 검정을 반복 수행하고,
관련성의 유무와 강도를 비교한다.

분석 대상:
  1) 성별 × 지지정당     — 중간 정도 관련성 예상
  2) 연령대 × SNS이용여부 — 강한 관련성 예상
  3) 성별 × 교육수준      — 독립(관련 없음) 예상

학습 포인트:
  - p-value만으로 결론짓지 않고 효과 크기(Cramér's V)를 함께 보는 습관
  - 기대빈도 가정 점검의 중요성
  - '유의미하지 않음'도 의미 있는 결과임을 이해
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
from dataclasses import dataclass


# ============================================================
# 결과 저장용 데이터 클래스
# ============================================================
@dataclass
class ChiSquareResult:
    """카이제곱 검정 결과를 구조화하여 저장한다."""

    var1: str
    var2: str
    chi2: float
    dof: int
    p_value: float
    cramers_v: float
    min_expected: float
    cells_below_5: int
    total_cells: int
    observed: pd.DataFrame
    expected: np.ndarray


# ============================================================
# 핵심 함수
# ============================================================
def run_chi_square(
    df: pd.DataFrame,
    var1: str,
    var2: str,
    alpha: float = 0.05,
) -> ChiSquareResult:
    """두 범주형 변수에 대해 카이제곱 독립성 검정을 수행하고 결과를 반환한다.

    Parameters
    ----------
    df : pd.DataFrame
        분석 대상 데이터프레임.
    var1 : str
        행 변수 이름.
    var2 : str
        열 변수 이름.
    alpha : float
        유의수준 (기본값 0.05).

    Returns
    -------
    ChiSquareResult
        검정 결과를 담은 데이터 클래스 인스턴스.
    """
    observed = pd.crosstab(df[var1], df[var2])
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)

    n = observed.values.sum()
    r, k = observed.shape
    v = np.sqrt(chi2 / (n * (min(r, k) - 1)))

    return ChiSquareResult(
        var1=var1,
        var2=var2,
        chi2=chi2,
        dof=dof,
        p_value=p_value,
        cramers_v=v,
        min_expected=expected.min(),
        cells_below_5=int((expected < 5).sum()),
        total_cells=expected.size,
        observed=observed,
        expected=expected,
    )


def interpret_v(v: float) -> str:
    """Cramér's V의 해석 기준."""
    if v < 0.10:
        return "무시할 수준"
    elif v < 0.20:
        return "약한 관련성"
    elif v < 0.30:
        return "중간 정도 관련성"
    else:
        return "강한 관련성"


def print_result(result: ChiSquareResult, alpha: float = 0.05) -> None:
    """카이제곱 검정 결과를 3단계(실행→확인→해석) 구조로 출력한다.

    Parameters
    ----------
    result : ChiSquareResult
        run_chi_square()의 반환값.
    alpha : float
        유의수준.
    """
    title = f"{result.var1} × {result.var2}"

    print("\n" + "=" * 65)
    print(f"  분석: {title}")
    print("=" * 65)

    # ── ① 실행: 교차표 ──
    print("\n[① 교차표 (관측 빈도)]")
    # 주변합 포함 교차표
    obs_with_margins = result.observed.copy()
    obs_with_margins["합계"] = obs_with_margins.sum(axis=1)
    obs_with_margins.loc["합계"] = obs_with_margins.sum()
    print(obs_with_margins.astype(int))

    # 행 비율
    row_pct = result.observed.div(result.observed.sum(axis=1), axis=0) * 100
    print("\n[행 비율 (%)]")
    print(row_pct.round(1))

    # ── ② 확인: 검정 통계량 ──
    print(f"\n[② 카이제곱 검정 결과]")
    print(f"  χ²({result.dof}) = {result.chi2:.4f}")
    print(f"  p-value   = {result.p_value:.4f}")
    print(f"  Cramér's V = {result.cramers_v:.4f} ({interpret_v(result.cramers_v)})")

    # 기대빈도 가정 점검
    print(f"\n[기대빈도 가정 점검]")
    expected_df = pd.DataFrame(
        result.expected,
        index=result.observed.index,
        columns=result.observed.columns,
    ).round(2)
    print(expected_df)
    print(f"  최소 기대빈도: {result.min_expected:.2f}")
    print(f"  기대빈도 < 5: {result.cells_below_5}개 / {result.total_cells}개", end="")

    if result.cells_below_5 == 0:
        print(" → 가정 충족")
    else:
        pct = result.cells_below_5 / result.total_cells * 100
        status = "대안 검정 고려" if pct > 20 else "허용 범위"
        print(f" ({pct:.1f}%) → {status}")

    # ── ③ 해석 ──
    significant = result.p_value < alpha
    print(f"\n[③ 해석]")
    if significant:
        print(f"  → p = {result.p_value:.4f} < {alpha}: "
              f"두 변수 사이에 통계적으로 유의미한 관련성이 있다.")
        print(f"  → 관련성 강도: Cramér's V = {result.cramers_v:.4f} "
              f"({interpret_v(result.cramers_v)})")
    else:
        print(f"  → p = {result.p_value:.4f} ≥ {alpha}: "
              f"두 변수 사이에 통계적으로 유의미한 관련성이 없다.")
        print(f"  → 귀무가설(독립)을 기각할 수 없다.")


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    # ── 데이터 불러오기 ──
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w04.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")

    print("=" * 65)
    print("  W04-B | 카이제곱 검정 실습 (스튜디오)")
    print("=" * 65)
    print(f"  데이터: {data_path.name} (n={len(df)})")

    # ── 분석할 변수 쌍 정의 ──
    pairs = [
        ("성별", "지지정당"),
        ("연령대", "SNS이용여부"),
        ("성별", "교육수준"),
    ]

    # ── 각 쌍에 대해 카이제곱 검정 수행 ──
    results: list[ChiSquareResult] = []
    for var1, var2 in pairs:
        result = run_chi_square(df, var1, var2)
        results.append(result)
        print_result(result)

    # ================================================================
    # 종합 비교: 어떤 변수 쌍의 관련성이 가장 강한가?
    # ================================================================
    print("\n" + "=" * 65)
    print("  종합 비교: 관련성 강도 순위")
    print("=" * 65)

    # Cramér's V 기준 내림차순 정렬
    sorted_results = sorted(results, key=lambda r: r.cramers_v, reverse=True)

    print(f"\n  {'순위':<4} {'변수 쌍':<22} {'χ²':>10} {'df':>4} "
          f"{'p-value':>10} {'Cramér V':>10} {'판정':<14}")
    print("  " + "─" * 76)

    for rank, r in enumerate(sorted_results, 1):
        sig = "유의미 *" if r.p_value < 0.05 else "유의미하지 않음"
        pair_name = f"{r.var1} × {r.var2}"
        print(f"  {rank:<4} {pair_name:<22} {r.chi2:>10.4f} {r.dof:>4} "
              f"{r.p_value:>10.4f} {r.cramers_v:>10.4f} {sig:<14}")

    # ── 핵심 요약 ──
    strongest = sorted_results[0]
    weakest = sorted_results[-1]

    print(f"""
  ─────────────────────────────────────────
  핵심 요약
  ─────────────────────────────────────────
  ▸ 가장 강한 관련성: {strongest.var1} × {strongest.var2}
    (V = {strongest.cramers_v:.4f}, {interpret_v(strongest.cramers_v)})

  ▸ 가장 약한 관련성: {weakest.var1} × {weakest.var2}
    (V = {weakest.cramers_v:.4f}, {interpret_v(weakest.cramers_v)})

  ▸ 통계적 유의성(p < .05)과 실질적 의미(Cramér's V)를
    함께 보고해야 연구 결과의 해석이 완전해진다.
    p-value는 '관련이 있는가?'를 알려주고,
    Cramér's V는 '얼마나 관련이 있는가?'를 알려준다.
""")
