"""
W03 실습 데이터 생성 스크립트
=============================
EDA(탐색적 데이터 분석) 실습을 위한 정제된 사회조사 데이터를 생성한다.

학습 목표에 맞춰 다음과 같이 설계하였다:
  - 200명, 6개 변수, 결측 없음 (정제 완료 상태)
  - 소득: 우측 치우침(right-skewed) 분포
  - 교육수준별 소득 차이 관찰 가능
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_clean_survey(n: int = 200, seed: int = 1974) -> pd.DataFrame:
    """정제된 사회조사 데이터를 생성한다.

    Parameters
    ----------
    n : int
        표본 크기 (기본값 200).
    seed : int
        재현성을 위한 난수 시드.

    Returns
    -------
    pd.DataFrame
        결측 없는 정제 데이터프레임.
    """
    rng = np.random.default_rng(seed)

    # ── 1) 성별: 대략 50/50 비율 ──
    성별 = rng.choice(["남성", "여성"], size=n, p=[0.50, 0.50])

    # ── 2) 연령: 20~65세, 대체로 대칭 분포 ──
    연령_raw = rng.normal(loc=38.2, scale=11.8, size=n)
    연령 = np.clip(np.round(연령_raw), 20, 65).astype(int)

    # ── 3) 교육수준: 고졸이하 30%, 대졸 45%, 대학원이상 25% ──
    교육수준 = rng.choice(
        ["고졸이하", "대졸", "대학원이상"],
        size=n,
        p=[0.30, 0.45, 0.25],
    )

    # ── 4) 소득: 교육수준별 로그정규 분포 → 우측 치우침 ──
    # 교육수준별 소득: 고졸이하 ~220, 대졸 ~330, 대학원이상 ~530
    소득_params = {
        "고졸이하": (5.28, 0.45),     # lognormal(mu, sigma)
        "대졸": (5.65, 0.50),
        "대학원이상": (6.15, 0.40),
    }
    소득 = np.zeros(n)
    for edu_level, (mu, sigma) in 소득_params.items():
        mask = 교육수준 == edu_level
        n_group = mask.sum()
        vals = rng.lognormal(mean=mu, sigma=sigma, size=n_group)
        vals = np.clip(np.round(vals), 80, 1200)
        소득[mask] = vals

    # ── 5) 생활만족도: 1~5점, 대체로 대칭 ──
    생활만족도 = rng.choice(
        [1, 2, 3, 4, 5], size=n,
        p=[0.08, 0.18, 0.35, 0.25, 0.14],
    )

    # ── 6) 정치관심도: 1~5점 ──
    정치관심도 = rng.choice(
        [1, 2, 3, 4, 5], size=n,
        p=[0.12, 0.25, 0.30, 0.20, 0.13],
    )

    df = pd.DataFrame({
        "성별": 성별,
        "연령": 연령,
        "교육수준": 교육수준,
        "소득": 소득.astype(int),
        "생활만족도": 생활만족도,
        "정치관심도": 정치관심도,
    })

    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W03 실습 데이터 생성 (정제 데이터)")
    print("=" * 60)

    # ① 실행: 데이터 생성
    df = generate_clean_survey(n=200, seed=1974)

    # ② 확인: 기본 정보
    print(f"\n전체 표본 수: {len(df)}명")
    print(f"결측치: {df.isnull().sum().sum()}건 (결측 없음)")

    print("\n--- 수치형 변수 기술통계 ---")
    desc = df[["연령", "소득", "생활만족도"]].describe()
    print(desc)

    print("\n--- 평균 vs 중앙값 비교 ---")
    for col in ["연령", "소득", "생활만족도"]:
        mean_val = df[col].mean()
        med_val = df[col].median()
        diff = mean_val - med_val
        print(f"  {col}: 평균={mean_val:.1f}, 중앙값={med_val:.1f}, 차이={diff:+.1f}")

    print("\n--- 교육수준별 소득 ---")
    grouped = df.groupby("교육수준")["소득"].agg(["count", "mean", "median"])
    # 순서 지정
    for edu in ["고졸이하", "대졸", "대학원이상"]:
        if edu in grouped.index:
            row = grouped.loc[edu]
            print(f"  {edu}: {int(row['count'])}명, 평균={row['mean']:.1f}, 중앙값={row['median']:.1f}")

    # ③ 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w03.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
