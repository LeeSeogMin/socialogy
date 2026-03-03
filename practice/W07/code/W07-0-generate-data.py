"""
W07 실습 데이터 생성 스크립트
=============================
단순회귀 실습을 위한 가상 사회조사 데이터를 생성한다.

학습 목표에 맞춰 다음과 같이 설계하였다:
  - 교육연수 → 소득: 유의한 양의 관계 (R² ≈ 0.29)
  - 연령 → 생활만족도: 비유의 (약한 음의 관계)
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_survey_w07(n: int = 200, seed: int = 2532) -> pd.DataFrame:
    """단순회귀 실습용 데이터를 생성한다.

    Parameters
    ----------
    n : int
        표본 크기 (기본값 200).
    seed : int
        재현성을 위한 난수 시드.

    Returns
    -------
    pd.DataFrame
        생성된 데이터프레임.
    """
    rng = np.random.default_rng(seed)

    # ── 1) 성별 ──
    성별 = rng.choice(["남성", "여성"], size=n, p=[0.50, 0.50])

    # ── 2) 연령: 20~65세 ──
    연령 = np.clip(np.round(rng.normal(40, 12, size=n)), 20, 65).astype(int)

    # ── 3) 교육연수: 6~18년 (연속형) ──
    교육연수 = np.clip(np.round(rng.normal(13, 3, size=n)), 6, 18).astype(int)

    # ── 4) 소득: 교육연수에 의존 (Y = 85.2 + 45.8*X + noise) ──
    noise_income = rng.normal(0, 218, size=n)
    소득 = 85.2 + 45.8 * 교육연수 + noise_income
    소득 = np.clip(np.round(소득), 50, 1200).astype(int)

    # ── 5) 생활만족도: 연령과 약한 관계 (Y = 3.85 - 0.012*X + noise) ──
    noise_sat = rng.normal(0, 1.1, size=n)
    생활만족도_raw = 3.85 - 0.012 * 연령 + noise_sat
    생활만족도 = np.clip(np.round(생활만족도_raw), 1, 5).astype(int)

    # ── 6) 정치관심도 ──
    정치관심도 = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.12, 0.25, 0.30, 0.20, 0.13])

    df = pd.DataFrame({
        "연령": 연령,
        "교육연수": 교육연수,
        "소득": 소득,
        "생활만족도": 생활만족도,
        "정치관심도": 정치관심도,
        "성별": 성별,
    })

    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W07 실습 데이터 생성")
    print("=" * 60)

    df = generate_survey_w07(n=200, seed=2532)

    print(f"\n전체 표본 수: {len(df)}명")
    print(f"변수 목록: {list(df.columns)}")

    print("\n--- 기본 기술통계 ---")
    print(df.describe())

    # 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w07.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
