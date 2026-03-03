"""
W08 실습: 단순회귀 → 중다회귀 비교 + VIF + 표준화계수
====================================================
교육연수만으로 소득을 예측하는 단순회귀에서 출발하여,
경력연수와 성별을 추가한 중다회귀를 비교한다.

학습 목표:
  1. 단순회귀와 중다회귀의 계수 차이를 해석할 수 있다.
  2. VIF로 다중공선성을 확인할 수 있다.
  3. 변수 추가에 따른 R² 변화를 설명할 수 있다.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from pathlib import Path


def load_data() -> pd.DataFrame:
    """실습 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w08.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W08 실습: 단순회귀 → 중다회귀 비교")
    print("=" * 60)

    df = load_data()
    df["성별_더미"] = (df["성별"] == "남성").astype(int)

    # ============================================================
    # 과제 1: 단순회귀 → 중다회귀 계수 변화
    # ============================================================

    # ── 모델 1: 단순회귀 (교육연수 → 소득) ──
    print("\n" + "=" * 60)
    print("모델 1: 단순회귀 (소득 ~ 교육연수)")
    print("=" * 60)

    X1 = sm.add_constant(df["교육연수"])
    model1 = sm.OLS(df["소득"], X1).fit()
    print(f"  β₀ = {model1.params.iloc[0]:.1f}")
    print(f"  교육연수 β₁ = {model1.params.iloc[1]:.1f}")
    print(f"  R² = {model1.rsquared:.3f}")
    print(f"  교육연수 p = {model1.pvalues.iloc[1]:.6f}")

    # ── 모델 2: 중다회귀 2변수 (교육연수 + 경력연수 → 소득) ──
    print("\n" + "=" * 60)
    print("모델 2: 중다회귀 (소득 ~ 교육연수 + 경력연수)")
    print("=" * 60)

    X2 = sm.add_constant(df[["교육연수", "경력연수"]])
    model2 = sm.OLS(df["소득"], X2).fit()
    print(f"  β₀ = {model2.params.iloc[0]:.1f}")
    print(f"  교육연수 β₁ = {model2.params.iloc[1]:.1f}")
    print(f"  경력연수 β₂ = {model2.params.iloc[2]:.1f}")
    print(f"  R² = {model2.rsquared:.3f}")
    print(f"  교육연수 p = {model2.pvalues.iloc[1]:.6f}")
    print(f"  경력연수 p = {model2.pvalues.iloc[2]:.6f}")

    # ============================================================
    # 과제 2: 3변수 중다회귀 + VIF
    # ============================================================
    print("\n" + "=" * 60)
    print("모델 3: 중다회귀 (소득 ~ 교육연수 + 경력연수 + 성별)")
    print("=" * 60)

    X3 = sm.add_constant(df[["교육연수", "경력연수", "성별_더미"]])
    model3 = sm.OLS(df["소득"], X3).fit()
    print(f"  β₀ = {model3.params.iloc[0]:.1f}")
    print(f"  교육연수 β₁ = {model3.params.iloc[1]:.1f}")
    print(f"  경력연수 β₂ = {model3.params.iloc[2]:.1f}")
    print(f"  성별_더미 β₃ = {model3.params.iloc[3]:.1f}")
    print(f"  R² = {model3.rsquared:.3f}")
    print(f"  교육연수 p = {model3.pvalues.iloc[1]:.6f}")
    print(f"  경력연수 p = {model3.pvalues.iloc[2]:.6f}")
    print(f"  성별_더미 p = {model3.pvalues.iloc[3]:.6f}")

    # ── VIF 확인 ──
    print("\n" + "-" * 40)
    print("VIF (다중공선성 확인)")
    print("-" * 40)
    for i, col in enumerate(X3.columns[1:]):
        vif = variance_inflation_factor(X3.values, i + 1)
        label = "문제 없음" if vif < 5 else ("주의" if vif < 10 else "심각")
        print(f"  {col}: VIF = {vif:.2f} ({label})")

    # ============================================================
    # 과제 3: 교육연수 계수 변화 추적
    # ============================================================
    print("\n" + "=" * 60)
    print("교육연수 계수 변화 추적")
    print("=" * 60)

    print(f"\n{'모형':>25} {'교육연수 β₁':>12} {'R²':>8}")
    print("-" * 50)
    print(f"  {'단순회귀 (교육연수)':>23} {model1.params.iloc[1]:>12.1f} {model1.rsquared:>8.3f}")
    print(f"  {'중다 (교육+경력)':>23} {model2.params.iloc[1]:>12.1f} {model2.rsquared:>8.3f}")
    print(f"  {'중다 (교육+경력+성별)':>23} {model3.params.iloc[1]:>12.1f} {model3.rsquared:>8.3f}")

    print("\n  해석:")
    print(f"  - 교육연수의 β₁이 {model1.params.iloc[1]:.1f} → "
          f"{model2.params.iloc[1]:.1f} → {model3.params.iloc[1]:.1f}로 감소했다.")
    print("  - 단순회귀에서 교육연수의 계수에 경력연수·성별의 효과가 포함되어 있었다.")
    print("  - 변수를 추가할수록 교육연수의 '순수한' 연관만 남는다.")
    print(f"  - R²는 {model1.rsquared:.3f} → {model2.rsquared:.3f} → "
          f"{model3.rsquared:.3f}로 증가하여, 추가 변수가 소득 변동을 더 설명한다.")
    print("  - 이 결과는 인과관계가 아닌 예측 관계(연관)만 확인한 것이다.")

    # ============================================================
    # 확장: 표준화 계수 비교
    # ============================================================
    print("\n" + "=" * 60)
    print("확장: 표준화 계수 비교 (3변수 모형)")
    print("=" * 60)

    df_std = df[["교육연수", "경력연수", "성별_더미", "소득"]].copy()
    for col in df_std.columns:
        df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()

    X_std = sm.add_constant(df_std[["교육연수", "경력연수", "성별_더미"]])
    model_std = sm.OLS(df_std["소득"], X_std).fit()

    print(f"\n{'변수':>12} {'비표준화 β':>12} {'표준화 β':>12}")
    print("-" * 40)
    for i, col in enumerate(["교육연수", "경력연수", "성별_더미"]):
        print(f"  {col:>10} {model3.params.iloc[i+1]:>12.1f} {model_std.params.iloc[i+1]:>12.3f}")
    print("\n  → 표준화 계수로 비교하면 교육연수의 상대적 연관이 가장 크다.")

    # ============================================================
    # 시각화: 모형별 계수 비교
    # ============================================================
    print("\n시각화 생성 중...")
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ── (좌) 교육연수 계수 변화 ──
    models = ["단순회귀", "2변수 중다", "3변수 중다"]
    betas = [model1.params.iloc[1], model2.params.iloc[1], model3.params.iloc[1]]
    axes[0].bar(models, betas, color=["#4C72B0", "#55A868", "#C44E52"])
    axes[0].set_ylabel("교육연수 β₁")
    axes[0].set_title("변수 추가에 따른 교육연수 계수 변화")
    for i, v in enumerate(betas):
        axes[0].text(i, v + 0.5, f"{v:.1f}", ha="center", fontweight="bold")

    # ── (우) R² 변화 ──
    r2s = [model1.rsquared, model2.rsquared, model3.rsquared]
    axes[1].bar(models, r2s, color=["#4C72B0", "#55A868", "#C44E52"])
    axes[1].set_ylabel("R²")
    axes[1].set_title("변수 추가에 따른 R² 변화")
    for i, v in enumerate(r2s):
        axes[1].text(i, v + 0.005, f"{v:.3f}", ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w08_comparison.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
