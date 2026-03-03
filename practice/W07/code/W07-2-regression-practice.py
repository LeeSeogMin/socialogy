"""
W07 실습 ②: 연령 → 생활만족도 (단순회귀) + 두 모델 비교
========================================================
두 번째 회귀 모델을 실행하고, 첫 번째 모델과 R²를 비교한다.

학습 목표:
  1. 비유의한 회귀 결과를 올바르게 해석할 수 있다.
  2. 두 모델의 R²를 비교하여 예측력 차이를 서술할 수 있다.
  3. 회귀 결과가 인과관계를 의미하지 않음을 이해한다.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pathlib import Path


def load_data() -> pd.DataFrame:
    """실습 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w07.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W07 실습 ②: 두 회귀 모델 비교")
    print("=" * 60)

    df = load_data()

    # ============================================================
    # 모델 1: 교육연수 → 소득
    # ============================================================
    print("\n" + "=" * 60)
    print("모델 1: 교육연수 → 소득")
    print("=" * 60)

    X1 = sm.add_constant(df["교육연수"])
    m1 = sm.OLS(df["소득"], X1).fit()
    print(f"  β₀ = {m1.params.iloc[0]:.1f}, β₁ = {m1.params.iloc[1]:.1f}")
    print(f"  R² = {m1.rsquared:.3f}, p = {m1.pvalues.iloc[1]:.6f}")
    sig1 = "유의" if m1.pvalues.iloc[1] < 0.05 else "비유의"
    print(f"  판정: {sig1}")

    # ============================================================
    # 모델 2: 연령 → 생활만족도
    # ============================================================
    print("\n" + "=" * 60)
    print("모델 2: 연령 → 생활만족도")
    print("=" * 60)

    X2 = sm.add_constant(df["연령"])
    m2 = sm.OLS(df["생활만족도"], X2).fit()
    print(f"  β₀ = {m2.params.iloc[0]:.2f}, β₁ = {m2.params.iloc[1]:.4f}")
    print(f"  R² = {m2.rsquared:.3f}, p = {m2.pvalues.iloc[1]:.4f}")
    sig2 = "유의" if m2.pvalues.iloc[1] < 0.05 else "비유의"
    print(f"  판정: {sig2}")

    if m2.pvalues.iloc[1] >= 0.05:
        print("\n  → 연령은 생활만족도의 유의한 예측변수가 아니다.")
        print("    β₁이 0에 가깝고 R²도 매우 낮아, 연령만으로는")
        print("    생활만족도를 설명할 수 없다.")

    # ============================================================
    # 두 모델 비교
    # ============================================================
    print("\n" + "=" * 60)
    print("두 모델 비교")
    print("=" * 60)
    print(f"\n{'항목':>10} {'모델 1 (교육→소득)':>20} {'모델 2 (연령→만족)':>20}")
    print("-" * 55)
    print(f"  {'β₁':>8} {m1.params.iloc[1]:>20.1f} {m2.params.iloc[1]:>20.4f}")
    print(f"  {'R²':>8} {m1.rsquared:>20.3f} {m2.rsquared:>20.3f}")
    print(f"  {'p값':>8} {m1.pvalues.iloc[1]:>20.6f} {m2.pvalues.iloc[1]:>20.4f}")
    print(f"  {'판정':>8} {sig1:>20} {sig2:>20}")

    print("\n  해석:")
    print(f"  - 교육연수는 소득 변동의 {m1.rsquared*100:.1f}%를 설명한다.")
    print(f"  - 연령은 생활만족도 변동의 {m2.rsquared*100:.1f}%만 설명하며 유의하지 않다.")
    print("  - 두 결과 모두 인과관계를 의미하지 않는다.")

    # ============================================================
    # 시각화: 2개 산점도 비교
    # ============================================================
    print("\n산점도 비교 생성 중...")
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 모델 1
    axes[0].scatter(df["교육연수"], df["소득"], alpha=0.5)
    x_range1 = np.linspace(df["교육연수"].min(), df["교육연수"].max(), 100)
    axes[0].plot(x_range1, m1.params.iloc[0] + m1.params.iloc[1] * x_range1,
                 "r-", linewidth=2)
    axes[0].set_xlabel("교육연수 (년)")
    axes[0].set_ylabel("소득 (만원)")
    axes[0].set_title(f"교육연수 → 소득 (R²={m1.rsquared:.3f}, p<0.001)")

    # 모델 2
    axes[1].scatter(df["연령"], df["생활만족도"], alpha=0.5)
    x_range2 = np.linspace(df["연령"].min(), df["연령"].max(), 100)
    axes[1].plot(x_range2, m2.params.iloc[0] + m2.params.iloc[1] * x_range2,
                 "r-", linewidth=2)
    axes[1].set_xlabel("연령 (세)")
    axes[1].set_ylabel("생활만족도 (1-5)")
    axes[1].set_title(f"연령 → 생활만족도 (R²={m2.rsquared:.3f}, p={m2.pvalues.iloc[1]:.3f})")

    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w07_comparison.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
