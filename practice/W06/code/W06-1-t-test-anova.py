"""
W06 실습: 독립표본 t-검정 + 일원분산분석(ANOVA)
================================================
성별 × 소득 (t-검정)과 교육수준 × 소득 (ANOVA)을 수행한다.

학습 목표:
  1. 가정 확인(정규성, 등분산)을 수행할 수 있다.
  2. t-검정과 ANOVA를 실행하고 효과 크기를 보고할 수 있다.
  3. Tukey 사후검정으로 집단 쌍별 차이를 확인할 수 있다.
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from pathlib import Path


def load_data() -> pd.DataFrame:
    """실습 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w06.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W06 실습: 독립표본 t-검정 + ANOVA")
    print("=" * 60)

    df = load_data()

    # ============================================================
    # 과제 1: 성별 × 소득 (독립표본 t-검정)
    # ============================================================
    print("\n" + "=" * 60)
    print("과제 1: 성별 × 소득 (독립표본 t-검정)")
    print("=" * 60)

    male = df[df["성별"] == "남성"]["소득"]
    female = df[df["성별"] == "여성"]["소득"]

    # ① 기술통계
    print("\n① 기술통계")
    print("-" * 60)
    print(f"  남성: n = {len(male)}, 평균 = {male.mean():.1f}, SD = {male.std():.1f}")
    print(f"  여성: n = {len(female)}, 평균 = {female.mean():.1f}, SD = {female.std():.1f}")

    # ② 정규성 검정 (Shapiro-Wilk)
    stat_m, p_m = stats.shapiro(male)
    stat_f, p_f = stats.shapiro(female)
    print("\n② 정규성 검정 (Shapiro-Wilk)")
    print("-" * 60)
    print(f"  남성: W = {stat_m:.4f}, p = {p_m:.4f} {'✓ 충족' if p_m > 0.05 else '✗ 위반'}")
    print(f"  여성: W = {stat_f:.4f}, p = {p_f:.4f} {'✓ 충족' if p_f > 0.05 else '✗ 위반'}")

    # ③ 등분산 검정 (Levene)
    lev_stat, lev_p = stats.levene(male, female)
    print("\n③ 등분산 검정 (Levene)")
    print("-" * 60)
    print(f"  Levene: F = {lev_stat:.4f}, p = {lev_p:.4f} {'✓ 충족' if lev_p > 0.05 else '✗ 위반'}")

    # ④ 독립표본 t-검정
    equal_var = lev_p > 0.05
    t_stat, t_p = stats.ttest_ind(male, female, equal_var=equal_var)
    df_t = len(male) + len(female) - 2
    print("\n④ 독립표본 t-검정")
    print("-" * 60)
    print(f"  t({df_t}) = {t_stat:.3f}, p = {t_p:.4f}")
    print(f"  판정: {'귀무가설 기각 (유의)' if t_p < 0.05 else '귀무가설 채택 (비유의)'}")

    # ⑤ 효과 크기 (Cohen's d)
    n1, n2 = len(male), len(female)
    pooled_std = np.sqrt(
        ((n1 - 1) * male.std(ddof=1) ** 2 + (n2 - 1) * female.std(ddof=1) ** 2)
        / (n1 + n2 - 2)
    )
    cohens_d = (male.mean() - female.mean()) / pooled_std
    print("\n⑤ 효과 크기 (Cohen's d)")
    print("-" * 60)
    print(f"  Cohen's d = {cohens_d:.3f}")
    if abs(cohens_d) < 0.2:
        판정 = "무시할 수준"
    elif abs(cohens_d) < 0.5:
        판정 = "작은~중간 효과"
    elif abs(cohens_d) < 0.8:
        판정 = "중간~큰 효과"
    else:
        판정 = "큰 효과"
    print(f"  판정: {판정} (기준: 0.2/0.5/0.8)")

    # ============================================================
    # 과제 2: 교육수준 × 소득 (일원분산분석 ANOVA)
    # ============================================================
    print("\n" + "=" * 60)
    print("과제 2: 교육수준 × 소득 (ANOVA)")
    print("=" * 60)

    edu_groups = ["고졸", "대졸", "대학원"]
    groups = {e: df[df["교육수준"] == e]["소득"] for e in edu_groups}

    # ① 기술통계
    print("\n① 집단별 기술통계")
    print("-" * 60)
    for e in edu_groups:
        g = groups[e]
        print(f"  {e}: n = {len(g)}, 평균 = {g.mean():.1f}, SD = {g.std():.1f}")

    # ② 등분산 검정 (Levene)
    lev_stat_a, lev_p_a = stats.levene(*[groups[e] for e in edu_groups])
    print("\n② 등분산 검정 (Levene)")
    print("-" * 60)
    print(f"  Levene: F = {lev_stat_a:.4f}, p = {lev_p_a:.4f} {'✓ 충족' if lev_p_a > 0.05 else '✗ 위반'}")

    # ③ ANOVA
    f_stat, f_p = stats.f_oneway(*[groups[e] for e in edu_groups])
    df_between = len(edu_groups) - 1
    df_within = len(df) - len(edu_groups)
    print("\n③ ANOVA 결과")
    print("-" * 60)
    print(f"  F({df_between}, {df_within}) = {f_stat:.2f}, p = {f_p:.6f}")
    print(f"  판정: {'귀무가설 기각 (유의)' if f_p < 0.05 else '귀무가설 채택 (비유의)'}")

    # ④ 효과 크기 (η²)
    grand_mean = df["소득"].mean()
    ss_between = sum(
        len(groups[e]) * (groups[e].mean() - grand_mean) ** 2 for e in edu_groups
    )
    ss_total = sum((df["소득"] - grand_mean) ** 2)
    eta_sq = ss_between / ss_total
    print("\n④ 효과 크기 (η²)")
    print("-" * 60)
    print(f"  η² = {eta_sq:.3f}")
    if eta_sq < 0.01:
        판정_a = "무시할 수준"
    elif eta_sq < 0.06:
        판정_a = "작은 효과"
    elif eta_sq < 0.14:
        판정_a = "중간 효과"
    else:
        판정_a = "큰 효과"
    print(f"  판정: {판정_a} (기준: 0.01/0.06/0.14)")

    # ⑤ Tukey 사후검정
    print("\n⑤ Tukey HSD 사후검정")
    print("-" * 60)
    tukey = pairwise_tukeyhsd(df["소득"], df["교육수준"], alpha=0.05)
    print(tukey)

    # ============================================================
    # 과제 3: 비교
    # ============================================================
    print("\n" + "=" * 60)
    print("과제 3: 두 분석 결과 비교")
    print("=" * 60)
    print(f"\n{'항목':>12} {'성별 × 소득':>16} {'교육수준 × 소득':>16}")
    print("-" * 50)
    print(f"  {'검정통계량':>10} {'t='+f'{t_stat:.3f}':>16} {'F='+f'{f_stat:.2f}':>16}")
    print(f"  {'p값':>10} {t_p:>16.4f} {f_p:>16.6f}")
    print(f"  {'효과 크기':>10} {'d='+f'{cohens_d:.3f}':>16} {'η²='+f'{eta_sq:.3f}':>16}")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
