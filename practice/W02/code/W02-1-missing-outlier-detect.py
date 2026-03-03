"""
W02 실습 ①: 결측치·이상치 탐색
================================
원시 데이터에서 결측치와 이상치를 발견하고 현황을 보고한다.

학습 목표:
  1. 변수별 결측치 수와 비율을 확인할 수 있다.
  2. describe()의 min/max로 이상치를 탐지할 수 있다.
  3. 필터링으로 구체적인 이상치 행을 식별할 수 있다.
"""

import pandas as pd
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
    print("W02 실습 ①: 결측치·이상치 탐색")
    print("=" * 60)

    df = load_raw_data()

    # ① 결측치 현황
    print("\n① 변수별 결측치 현황")
    print("-" * 60)
    for col in df.columns:
        cnt = df[col].isnull().sum()
        pct = cnt / len(df) * 100
        print(f"  {col}: {cnt}건 ({pct:.1f}%)")

    total_missing = df.isnull().sum().sum()
    print(f"\n  전체 결측: {total_missing}건")

    # ② 수치형 변수 기술통계 (min/max로 이상치 탐지)
    print("\n② 수치형 변수 기술통계 (이상치 탐지용)")
    print("-" * 60)
    print(df.describe())

    # ③ 연령 이상치 필터링
    print("\n③ 연령 이상치 필터링 (100 이상 또는 0 미만)")
    print("-" * 60)
    age_outliers = df[(df["연령"] > 100) | (df["연령"] < 0)]
    if len(age_outliers) > 0:
        print(f"  이상치 {len(age_outliers)}건 발견:")
        for idx, row in age_outliers.iterrows():
            print(f"  행 {idx}: 연령 = {row['연령']}")
    else:
        print("  이상치 없음")

    # ④ 소득 이상치 필터링 (극단값)
    print("\n④ 소득 극단값 확인")
    print("-" * 60)
    income_valid = df["소득"].dropna()
    q1 = income_valid.quantile(0.25)
    q3 = income_valid.quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    income_outliers = df[df["소득"] > upper_bound]
    if len(income_outliers) > 0:
        print(f"  IQR 기준 상한({upper_bound:.0f}) 초과 {len(income_outliers)}건:")
        for idx, row in income_outliers.iterrows():
            print(f"  행 {idx}: 소득 = {row['소득']:.0f}만원")
    else:
        print("  극단값 없음")

    # ⑤ 현황 보고표 요약
    print("\n⑤ 현황 보고표 요약")
    print("-" * 60)
    print(f"{'변수명':>8} {'척도':>6} {'결측 수':>6} {'결측 비율':>8} {'이상치':>6}")
    report = [
        ("성별", "명목", 5, "2.5%", "X"),
        ("연령", "비율", 0, "0.0%", f"O ({len(age_outliers)}건)"),
        ("교육수준", "서열", 8, "4.0%", "X"),
        ("소득", "비율", 25, "12.5%", f"O ({len(income_outliers)}건)"),
        ("생활만족도", "서열", 10, "5.0%", "X"),
        ("정치관심도", "서열", 0, "0.0%", "X"),
    ]
    for name, scale, miss, pct, outlier in report:
        print(f"  {name:>6} {scale:>6} {miss:>6} {pct:>8} {outlier:>8}")

    print("\n" + "=" * 60)
    print("탐색 완료!")
    print("=" * 60)
