"""
W02 실습 ③: MCAR 결측치 생성 + 중앙값 대체 + 원본 비교
======================================================
정제 데이터에서 무작위 결측(MCAR)을 만들고,
중앙값으로 보완한 뒤 원본과 비교한다.

학습 목표:
  1. MCAR 결측치를 직접 생성할 수 있다.
  2. 중앙값 대체로 결측을 보완할 수 있다.
  3. 보완 전후 평균·표준편차 변화를 해석할 수 있다.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_clean_data() -> pd.DataFrame:
    """정제 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w02_clean.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("W02 실습 ③: MCAR 결측 생성 + 중앙값 대체 + 원본 비교")
    print("=" * 60)

    df_clean = load_clean_data()
    print(f"\n원본 행 수: {len(df_clean)}, 결측 수: {df_clean.isnull().sum().sum()}")

    # ① MCAR 결측 생성: 소득 변수에서 무작위 20% 결측
    print("\n① MCAR 결측 생성 (소득 변수, 20%)")
    print("-" * 60)

    np.random.seed(42)
    mask = np.random.rand(len(df_clean)) < 0.2
    df_missing = df_clean.copy()
    df_missing.loc[mask, "소득"] = np.nan

    n_missing = df_missing["소득"].isnull().sum()
    pct_missing = df_missing["소득"].isnull().mean() * 100
    print(f"  결측 생성: {n_missing}건 ({pct_missing:.1f}%)")

    # ② 중앙값 대체
    print("\n② 중앙값 대체")
    print("-" * 60)

    before_mean = df_missing["소득"].mean()
    before_std = df_missing["소득"].std()

    median_val = df_missing["소득"].median()
    df_filled = df_missing.copy()
    df_filled["소득"] = df_filled["소득"].fillna(median_val)
    print(f"  대체값(중앙값): {median_val:.0f}만원")

    after_mean = df_filled["소득"].mean()
    after_std = df_filled["소득"].std()

    # ③ 원본과 비교
    original_mean = df_clean["소득"].mean()
    original_std = df_clean["소득"].std()

    print("\n③ 소득 변수 전후 비교")
    print("-" * 60)
    print(f"{'':>14} {'평균':>10} {'표준편차':>10}")
    print(f"{'원본(정답)':>14} {original_mean:>10.1f} {original_std:>10.1f}")
    print(f"{'결측 상태':>14} {before_mean:>10.1f} {before_std:>10.1f}")
    print(f"{'중앙값 대체':>14} {after_mean:>10.1f} {after_std:>10.1f}")

    # ④ 해석 포인트
    print("\n④ 해석 포인트")
    print("-" * 60)
    mean_diff = after_mean - original_mean
    std_diff = after_std - original_std
    print(f"  평균 변화: {mean_diff:+.1f} (원본 대비)")
    print(f"  표준편차 변화: {std_diff:+.1f} (원본 대비)")
    print("  → 중앙값 대체는 평균을 크게 바꾸지 않지만,")
    print("    표준편차를 줄인다 (데이터가 중앙으로 몰림).")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
