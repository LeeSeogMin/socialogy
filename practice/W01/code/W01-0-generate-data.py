"""
W01 실습 데이터 생성 스크립트
=============================
환경 점검 + 미니 실습을 위한 가상 사회조사 데이터를 생성한다.

학습 목표에 맞춰 다음과 같이 설계하였다:
  - 200명의 가상 응답자, 6개 변수
  - 소득 변수에 결측치 8건, 생활만족도에 결측치 3건
  - 연령 평균 ~39세, 소득 평균 ~320만원
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_social_survey(n: int = 200, seed: int = 260) -> pd.DataFrame:
    """가상 사회조사 데이터를 생성한다.

    Parameters
    ----------
    n : int
        표본 크기 (기본값 200).
    seed : int
        재현성을 위한 난수 시드.

    Returns
    -------
    pd.DataFrame
        생성된 사회조사 데이터프레임.
    """
    rng = np.random.default_rng(seed)

    # ── 1) 성별: 대략 50/50 비율 ──
    성별 = rng.choice(["남성", "여성"], size=n, p=[0.50, 0.50])

    # ── 2) 연령: 19~65세, 평균 ~39, 표준편차 ~12 ──
    연령_raw = rng.normal(loc=39, scale=12, size=n)
    연령 = np.clip(np.round(연령_raw), 19, 65).astype(int)

    # ── 3) 교육수준: 고졸이하 30%, 대졸 45%, 대학원이상 25% ──
    교육수준 = rng.choice(
        ["고졸이하", "대졸", "대학원이상"],
        size=n,
        p=[0.30, 0.45, 0.25],
    )

    # ── 4) 소득: 교육수준에 따라 다른 분포, 전체 평균 ~320만원 ──
    소득_base = {
        "고졸이하": 220,
        "대졸": 310,
        "대학원이상": 480,
    }
    소득 = np.array([
        max(50, min(850, int(rng.normal(loc=소득_base[edu], scale=130))))
        for edu in 교육수준
    ], dtype=float)

    # 소득 결측치 8건 삽입
    missing_income_idx = rng.choice(n, size=8, replace=False)
    소득[missing_income_idx] = np.nan

    # ── 5) 생활만족도: 1~5점 리커트 척도 ──
    생활만족도 = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.12, 0.20, 0.32, 0.24, 0.12])
    생활만족도 = 생활만족도.astype(float)

    # 생활만족도 결측치 3건 삽입
    missing_sat_idx = rng.choice(n, size=3, replace=False)
    생활만족도[missing_sat_idx] = np.nan

    # ── 6) 정치관심도: 1~5점 리커트 척도, 결측 없음 ──
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
    print("W01 실습 데이터 생성")
    print("=" * 60)

    # ① 실행: 데이터 생성
    df = generate_social_survey(n=200, seed=260)

    # ② 확인: 기본 정보 출력
    print(f"\n전체 표본 수: {len(df)}명")
    print(f"변수 목록: {list(df.columns)}")

    print("\n--- 기본 요약통계 ---")
    print(df.describe())

    print("\n--- 결측치 현황 ---")
    print(df.isnull().sum())

    print("\n--- 범주형 변수 빈도 ---")
    for col in ["성별", "교육수준"]:
        print(f"\n[{col}]")
        counts = df[col].value_counts()
        for val, cnt in counts.items():
            print(f"  {val}: {cnt}명 ({cnt / len(df) * 100:.1f}%)")

    # ③ 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w01.csv"

    # 한글 호환을 위해 UTF-8 BOM 인코딩 사용
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
