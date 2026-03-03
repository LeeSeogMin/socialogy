"""
W07 실습 ①: 교육연수 → 소득 (단순회귀)
=========================================
교육연수가 소득을 얼마나 예측하는지 단순회귀분석으로 확인한다.

학습 목표:
  1. OLS 회귀분석을 실행하고 계수를 해석할 수 있다.
  2. 산점도 + 회귀선으로 관계를 시각화할 수 있다.
  3. 잔차 플롯으로 가정을 확인할 수 있다.
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
    print("W07 실습 ①: 교육연수 → 소득 (단순회귀)")
    print("=" * 60)

    df = load_data()

    # ① OLS 회귀분석
    X = sm.add_constant(df["교육연수"])
    y = df["소득"]
    model = sm.OLS(y, X).fit()

    print("\n① 회귀분석 결과")
    print("-" * 60)
    print(f"  β₀ (절편)   = {model.params.iloc[0]:.1f}")
    print(f"  β₁ (교육연수) = {model.params.iloc[1]:.1f}")
    print(f"  R²          = {model.rsquared:.3f}")
    print(f"  p값 (교육연수) = {model.pvalues.iloc[1]:.6f}")

    print("\n  해석: 교육연수가 1년 증가하면 소득이 평균적으로")
    print(f"        약 {model.params.iloc[1]:.1f}만원 증가한다.")
    print(f"        모델은 소득 변동의 {model.rsquared*100:.1f}%를 설명한다.")

    # ② 전체 요약
    print("\n② OLS 전체 요약")
    print("-" * 60)
    print(model.summary())

    # ③ 산점도 + 회귀선
    print("\n③ 산점도 + 회귀선 생성 중...")
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["교육연수"], df["소득"], alpha=0.5, label="관측값")
    x_range = np.linspace(df["교육연수"].min(), df["교육연수"].max(), 100)
    y_pred = model.params.iloc[0] + model.params.iloc[1] * x_range
    ax.plot(x_range, y_pred, "r-", linewidth=2, label=f"회귀선 (R²={model.rsquared:.3f})")
    ax.set_xlabel("교육연수 (년)")
    ax.set_ylabel("소득 (만원)")
    ax.set_title("교육연수 → 소득: 단순회귀")
    ax.legend()
    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w07_scatter_regression.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()

    # ④ 잔차 플롯
    print("\n④ 잔차 플롯 생성 중...")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(model.fittedvalues, model.resid, alpha=0.5)
    ax.axhline(y=0, color="r", linestyle="--")
    ax.set_xlabel("예측값")
    ax.set_ylabel("잔차")
    ax.set_title("잔차 플롯 (패턴이 없으면 가정 충족)")
    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w07_residual_plot.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
