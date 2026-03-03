"""
W02 실습 데이터 생성 스크립트
=============================
데이터 정리 실습을 위한 의도적 결측·이상치가 포함된 원시 데이터를 생성한다.

의도적 문제 설계:
  - 성별: 결측 5건
  - 연령: 이상치 3건 (999, -1, 200)
  - 교육수준: 결측 8건
  - 소득: 결측 25건(12.5%), 극단 이상치 2건
  - 생활만족도: 결측 10건
  - 정치관심도: 정상 (문제 없음)
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_raw_survey(n: int = 200, seed: int = 42) -> pd.DataFrame:
    """의도적 결측·이상치가 포함된 원시 데이터를 생성한다.

    Parameters
    ----------
    n : int
        표본 크기 (기본값 200).
    seed : int
        재현성을 위한 난수 시드.

    Returns
    -------
    pd.DataFrame
        결측·이상치가 포함된 원시 데이터프레임.
    """
    rng = np.random.default_rng(seed)

    # ── 1) 성별: 50/50 비율, 이후 5건 결측 삽입 ──
    성별 = rng.choice(["남성", "여성"], size=n, p=[0.50, 0.50])
    성별 = 성별.astype(object)
    missing_gender_idx = rng.choice(n, size=5, replace=False)
    성별[missing_gender_idx] = None

    # ── 2) 연령: 정상 데이터 생성 후 이상치 3건 삽입 ──
    연령_raw = rng.normal(loc=39, scale=12, size=n)
    연령 = np.clip(np.round(연령_raw), 19, 65).astype(float)
    # 이상치 삽입: 999, -1, 200
    outlier_idx = rng.choice(n, size=3, replace=False)
    연령[outlier_idx[0]] = 999
    연령[outlier_idx[1]] = -1
    연령[outlier_idx[2]] = 200

    # ── 3) 교육수준: 8건 결측 삽입 ──
    교육수준 = rng.choice(
        ["고졸이하", "대졸", "대학원이상"],
        size=n,
        p=[0.30, 0.45, 0.25],
    )
    교육수준 = 교육수준.astype(object)
    missing_edu_idx = rng.choice(n, size=8, replace=False)
    교육수준[missing_edu_idx] = None

    # ── 4) 소득: 결측 25건 + 극단 이상치 2건 ──
    소득_base = {"고졸이하": 220, "대졸": 310, "대학원이상": 480}
    소득 = np.array([
        max(50, min(850, int(rng.normal(
            loc=소득_base.get(edu, 300), scale=130
        ))))
        for edu in 교육수준
    ], dtype=float)

    # 극단 이상치 2건 삽입 (매우 높은 값)
    outlier_income_idx = rng.choice(n, size=2, replace=False)
    소득[outlier_income_idx[0]] = 5000  # 극단적으로 높은 값
    소득[outlier_income_idx[1]] = 3500  # 극단적으로 높은 값

    # 결측 25건 삽입
    missing_income_idx = rng.choice(n, size=25, replace=False)
    소득[missing_income_idx] = np.nan

    # ── 5) 생활만족도: 결측 10건 삽입 ──
    생활만족도 = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.12, 0.20, 0.32, 0.24, 0.12])
    생활만족도 = 생활만족도.astype(float)
    missing_sat_idx = rng.choice(n, size=10, replace=False)
    생활만족도[missing_sat_idx] = np.nan

    # ── 6) 정치관심도: 결측 없음 (정상) ──
    정치관심도 = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.12, 0.25, 0.30, 0.20, 0.13])

    df = pd.DataFrame({
        "성별": 성별,
        "연령": 연령,
        "교육수준": 교육수준,
        "소득": 소득,
        "생활만족도": 생활만족도,
        "정치관심도": 정치관심도,
    })

    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W02 실습 데이터 생성 (의도적 결측·이상치 포함)")
    print("=" * 60)

    # ① 실행: 데이터 생성
    df = generate_raw_survey(n=200, seed=42)

    # ② 확인: 결측·이상치 현황
    print(f"\n전체 표본 수: {len(df)}명")
    print(f"변수 목록: {list(df.columns)}")

    print("\n--- 결측치 현황 ---")
    missing = df.isnull().sum()
    for col, cnt in missing.items():
        pct = cnt / len(df) * 100
        print(f"  {col}: {cnt}건 ({pct:.1f}%)")

    print("\n--- 수치형 변수 기술통계 ---")
    print(df.describe())

    print("\n--- 연령 이상치 확인 ---")
    age_outliers = df[(df["연령"] > 100) | (df["연령"] < 0)]
    print(f"  이상치 {len(age_outliers)}건 발견")
    if len(age_outliers) > 0:
        print(age_outliers[["연령"]].to_string())

    # ③ 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w02_raw.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
