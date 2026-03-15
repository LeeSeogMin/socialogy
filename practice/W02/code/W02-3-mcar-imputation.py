"""
W02 실습 ③: MCAR 결측치 대체 + 전후 비교
========================================
원시 데이터의 결측치를 MCAR로 가정하고,
수치형은 중앙값, 범주형은 최빈값으로 대체한 뒤 전후를 비교한다.

학습 목표:
  1. 수치형 결측을 중앙값으로 대체할 수 있다.
  2. 범주형 결측을 최빈값으로 대체할 수 있다.
  3. 대체 전후 평균·표준편차 변화를 해석할 수 있다.
"""

import pandas as pd
from pathlib import Path


def load_raw_data() -> pd.DataFrame:
    """원시 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w02_raw.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("W02 실습 ③: MCAR 결측치 대체 + 전후 비교")
    print("=" * 60)

    df = load_raw_data()

    # ① 대체 전 현황 확인
    print("\n① 대체 전 결측 현황")
    print("-" * 60)
    for col in df.columns:
        cnt = df[col].isnull().sum()
        if cnt > 0:
            pct = cnt / len(df) * 100
            print(f"  {col}: {cnt}건 ({pct:.1f}%)")

    # 소득 대체 전 통계 저장
    before_mean = df["소득"].mean()
    before_std = df["소득"].std()
    print(f"\n  소득 대체 전 — 평균: {before_mean:.1f}, 표준편차: {before_std:.1f}")

    # ② 결측치 대체
    print("\n② 결측치 대체")
    print("-" * 60)

    df_filled = df.copy()

    # 수치형: 중앙값 대체
    for col in ["소득", "생활만족도"]:
        n_miss = df_filled[col].isnull().sum()
        median_val = df_filled[col].median()
        df_filled[col] = df_filled[col].fillna(median_val)
        print(f"  {col}: {n_miss}건 → 중앙값({median_val:.0f})으로 대체")

    # 범주형: 최빈값 대체
    for col in ["성별", "교육수준"]:
        n_miss = df_filled[col].isnull().sum()
        mode_val = df_filled[col].mode()[0]
        df_filled[col] = df_filled[col].fillna(mode_val)
        print(f"  {col}: {n_miss}건 → 최빈값('{mode_val}')으로 대체")

    print(f"\n  남은 결측: {df_filled.isnull().sum().sum()}건")

    # ③ 대체 전후 비교
    after_mean = df_filled["소득"].mean()
    after_std = df_filled["소득"].std()

    print("\n③ 소득 변수 전후 비교")
    print("-" * 60)
    print(f"{'':>14} {'평균':>10} {'표준편차':>10}")
    print(f"{'대체 전':>14} {before_mean:>10.1f} {before_std:>10.1f}")
    print(f"{'대체 후':>14} {after_mean:>10.1f} {after_std:>10.1f}")

    mean_diff = after_mean - before_mean
    std_diff = after_std - before_std
    print(f"\n  평균 변화: {mean_diff:+.1f}")
    print(f"  표준편차 변화: {std_diff:+.1f}")
    print("  → 중앙값 대체는 평균을 크게 바꾸지 않지만,")
    print("    표준편차를 줄인다 (데이터가 중앙으로 몰림).")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
