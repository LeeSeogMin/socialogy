"""
W06 실습 데이터 생성 스크립트
=============================
t-검정 및 ANOVA 실습을 위한 가상 사회조사 데이터를 생성한다.

학습 목표에 맞춰 다음과 같이 설계하였다:
  - 성별 × 소득: 유의한 차이 (t-검정, 작은~중간 효과)
  - 교육수준 × 소득: 유의한 차이 (ANOVA, 큰 효과)
  - 정규성(Shapiro-Wilk), 등분산(Levene) 가정 충족
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_survey_w06(n: int = 200, seed: int = 5482) -> pd.DataFrame:
    """t-검정/ANOVA 실습용 데이터를 생성한다.

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

    # ── 1) 성별: 정확히 100/100 비율 ──
    성별 = np.array(["남성"] * 100 + ["여성"] * 100)
    rng.shuffle(성별)

    # ── 2) 교육수준: 3개 범주, 대략 균등 ──
    교육수준 = rng.choice(
        ["고졸", "대졸", "대학원"],
        size=n,
        p=[0.335, 0.335, 0.330],
    )

    # ── 3) 소득: 교육수준 + 성별 효과 + 정규 노이즈 ──
    # 교육수준별 기저값 + 성별 조정 + 무작위 변동
    edu_base = {"고졸": 270, "대졸": 340, "대학원": 440}
    gender_adj = {"남성": 22, "여성": -22}

    소득 = np.array([
        edu_base[e] + gender_adj[g] + rng.normal(0, 140)
        for e, g in zip(교육수준, 성별)
    ])
    소득 = np.clip(np.round(소득), 50, 900).astype(int)

    # ── 4) 연령대: 4개 범주 ──
    연령대 = rng.choice(
        ["20대", "30대", "40대", "50대+"],
        size=n,
        p=[0.28, 0.27, 0.25, 0.20],
    )

    # ── 5) 생활만족도: 1~10점 스케일 ──
    생활만족도 = rng.choice(
        list(range(1, 11)), size=n,
        p=[0.03, 0.05, 0.08, 0.12, 0.17, 0.20, 0.15, 0.10, 0.06, 0.04],
    )

    # ── 6) 정치관심도: 1~10점 스케일 ──
    정치관심도 = rng.choice(
        list(range(1, 11)), size=n,
        p=[0.05, 0.08, 0.12, 0.15, 0.18, 0.15, 0.12, 0.08, 0.04, 0.03],
    )

    df = pd.DataFrame({
        "성별": 성별,
        "연령대": 연령대,
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
    print("W06 실습 데이터 생성")
    print("=" * 60)

    # ① 실행: 데이터 생성
    df = generate_survey_w06(n=200, seed=5482)

    # ② 확인: 기본 정보
    print(f"\n전체 표본 수: {len(df)}명")
    print(f"변수 목록: {list(df.columns)}")

    print("\n--- 성별별 소득 ---")
    for g in ["남성", "여성"]:
        subset = df[df["성별"] == g]["소득"]
        print(f"  {g}: n={len(subset)}, 평균={subset.mean():.1f}, SD={subset.std():.1f}")

    print("\n--- 교육수준별 소득 ---")
    for e in ["고졸", "대졸", "대학원"]:
        subset = df[df["교육수준"] == e]["소득"]
        print(f"  {e}: n={len(subset)}, 평균={subset.mean():.1f}, SD={subset.std():.1f}")

    # ③ 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w06.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
