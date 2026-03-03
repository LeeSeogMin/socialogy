"""
W02 실습 ②: 결측치·이상치 처리 + 전후 비교
============================================
이상치를 NaN으로 변환하고, 결측치를 대체한 뒤 전후 기술통계를 비교한다.

학습 목표:
  1. 이상치를 NaN으로 변환할 수 있다.
  2. 수치형은 중앙값, 범주형은 최빈값으로 결측치를 대체할 수 있다.
  3. 처리 전후 기술통계를 비교하여 처리의 영향을 서술할 수 있다.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data() -> pd.DataFrame:
    """원시 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w02_raw.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W02 실습 ②: 결측치·이상치 처리 + 전후 비교")
    print("=" * 60)

    df = load_raw_data()

    # 원본 보관
    df_raw = df.copy()

    # ① 처리 전 기술통계 저장
    before = df.describe()
    before_missing = df.isnull().sum().sum()

    print("\n① 처리 전 기술통계")
    print("-" * 60)
    print(before)
    print(f"\n  전체 결측: {before_missing}건")

    # ② 이상치 처리: NaN으로 변환
    print("\n② 이상치 처리")
    print("-" * 60)

    # 연령 이상치 (100 초과 또는 0 미만)
    age_outlier_mask = (df["연령"] > 100) | (df["연령"] < 0)
    n_age_outliers = age_outlier_mask.sum()
    df.loc[age_outlier_mask, "연령"] = np.nan
    print(f"  연령 이상치 {n_age_outliers}건 → NaN 변환")

    # 소득 극단 이상치 (IQR 기준)
    income_valid = df["소득"].dropna()
    q1 = income_valid.quantile(0.25)
    q3 = income_valid.quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    income_outlier_mask = df["소득"] > upper_bound
    n_income_outliers = income_outlier_mask.sum()
    df.loc[income_outlier_mask, "소득"] = np.nan
    print(f"  소득 이상치 {n_income_outliers}건 → NaN 변환 (상한: {upper_bound:.0f}만원)")

    # ③ 결측치 처리: 수치형은 중앙값, 범주형은 최빈값
    print("\n③ 결측치 대체")
    print("-" * 60)

    # 수치형 변수: 중앙값 대체
    for col in ["연령", "소득", "생활만족도"]:
        n_missing = df[col].isnull().sum()
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"  {col}: {n_missing}건 → 중앙값({median_val:.0f})으로 대체")

    # 범주형 변수: 최빈값 대체
    for col in ["성별", "교육수준"]:
        n_missing = df[col].isnull().sum()
        mode_val = df[col].mode()[0]
        df[col] = df[col].fillna(mode_val)
        print(f"  {col}: {n_missing}건 → 최빈값('{mode_val}')으로 대체")

    # ④ 처리 후 기술통계
    after = df.describe()
    after_missing = df.isnull().sum().sum()

    print("\n④ 처리 후 기술통계")
    print("-" * 60)
    print(after)
    print(f"\n  남은 결측: {after_missing}건")

    # ⑤ 전후 비교
    print("\n⑤ 전후 비교")
    print("-" * 60)
    print(f"{'항목':>14} {'처리 전':>12} {'처리 후':>12} {'변화':>12}")
    print("-" * 60)

    items = [
        ("연령 평균", before.loc["mean", "연령"], after.loc["mean", "연령"]),
        ("연령 표준편차", before.loc["std", "연령"], after.loc["std", "연령"]),
        ("소득 평균", before.loc["mean", "소득"], after.loc["mean", "소득"]),
        ("소득 표준편차", before.loc["std", "소득"], after.loc["std", "소득"]),
    ]
    for name, bef, aft in items:
        diff = aft - bef
        direction = "↑" if diff > 0 else "↓"
        print(f"  {name:>12} {bef:>12.1f} {aft:>12.1f} {direction}{abs(diff):>10.1f}")

    print(f"  {'전체 결측 수':>12} {before_missing:>12} {after_missing:>12} {'':>12}")

    print("\n" + "=" * 60)
    print("처리 완료!")
    print("=" * 60)
