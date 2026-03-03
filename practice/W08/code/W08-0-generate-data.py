"""
W08 실습 데이터 생성 스크립트
=============================
중다회귀 실습을 위한 가상 사회조사 데이터를 생성한다.

학습 목표에 맞춰 다음과 같이 설계하였다:
  - 교육연수 → 소득: 유의한 양의 관계
  - 경력연수: 교육연수와 상관 (VIF ≈ 1.7)
  - 성별: 소득에 유의한 효과 + 교육연수와 약한 상관
  - 단순 → 중다회귀 비교 시 교육연수 계수 감소 패턴 확인
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_survey_w08(n: int = 200, seed: int = 8072) -> pd.DataFrame:
    """중다회귀 실습용 데이터를 생성한다.

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

    # ── 1) 성별: 약 50/50 비율 ──
    성별 = rng.choice(["남성", "여성"], size=n, p=[0.50, 0.50])

    # ── 2) 연령: 20~65세 ──
    연령 = np.clip(np.round(rng.normal(40, 12, size=n)), 20, 65).astype(int)

    # ── 3) 교육연수: 6~18년 (성별에 따라 평균 약간 다름) ──
    #    남성 평균 14, 여성 평균 12 → 성별-교육연수 상관 유도
    edu_base = rng.normal(13, 3, size=n)
    edu_adj = np.where(성별 == "남성", edu_base + 1.0, edu_base - 1.0)
    교육연수 = np.clip(np.round(edu_adj), 6, 18).astype(int)

    # ── 4) 경력연수: 교육연수와 상관 ──
    경력연수 = np.clip(
        np.round(1.4 * 교육연수 - 8 + rng.normal(0, 4.6, size=n)),
        0, 40,
    ).astype(int)

    # ── 5) 소득: 교육연수 + 경력연수 + 성별 효과 + 노이즈 ──
    성별_더미 = (성별 == "남성").astype(float)
    noise = rng.normal(0, 150, size=n)
    소득 = 120 + 36.2 * 교육연수 + 11.5 * 경력연수 + 18 * 성별_더미 + noise
    소득 = np.clip(np.round(소득), 50, 1200).astype(int)

    # ── 6) 생활만족도: 1~5점 ──
    생활만족도 = rng.choice(
        [1, 2, 3, 4, 5], size=n,
        p=[0.08, 0.20, 0.35, 0.25, 0.12],
    )

    # ── 7) 정치관심도: 1~5점 ──
    정치관심도 = rng.choice(
        [1, 2, 3, 4, 5], size=n,
        p=[0.12, 0.25, 0.30, 0.20, 0.13],
    )

    df = pd.DataFrame({
        "성별": 성별,
        "연령": 연령,
        "교육연수": 교육연수,
        "경력연수": 경력연수,
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
    print("W08 실습 데이터 생성")
    print("=" * 60)

    df = generate_survey_w08(n=200, seed=8072)

    print(f"\n전체 표본 수: {len(df)}명")
    print(f"변수 목록: {list(df.columns)}")

    print("\n--- 기본 기술통계 ---")
    print(df[["연령", "교육연수", "경력연수", "소득"]].describe())

    print("\n--- 성별별 교육연수·소득 ---")
    for g in ["남성", "여성"]:
        sub = df[df["성별"] == g]
        print(f"  {g}: n={len(sub)}, "
              f"교육연수 평균={sub['교육연수'].mean():.1f}, "
              f"소득 평균={sub['소득'].mean():.1f}")

    # 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w08.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
