"""
W01 실습: CSV 로드 + 기본 요약통계
==================================
social_survey_w01.csv 파일을 불러와 데이터 구조를 파악한다.

학습 목표:
  1. pandas로 CSV를 불러올 수 있다.
  2. df.describe()로 요약통계를 출력할 수 있다.
  3. 변수별 결측치와 척도를 확인할 수 있다.
"""

import pandas as pd
from pathlib import Path


def load_data() -> pd.DataFrame:
    """실습 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w01.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W01 실습: CSV 로드 + 기본 요약통계")
    print("=" * 60)

    df = load_data()

    # ① 데이터 크기 확인
    print(f"\n① 데이터 크기: {df.shape[0]}행 x {df.shape[1]}열")
    print(f"   변수 목록: {list(df.columns)}")

    # ② 기본 요약통계 (숫자형 변수)
    print("\n② 기본 요약통계 (숫자형 변수)")
    print("-" * 60)
    print(df.describe())

    # ③ 결측치 현황
    print("\n③ 변수별 결측치 현황")
    print("-" * 60)
    missing = df.isnull().sum()
    print(missing)
    print(f"\n   → 결측치가 있는 변수: ", end="")
    has_missing = missing[missing > 0]
    if len(has_missing) > 0:
        for var, cnt in has_missing.items():
            print(f"{var}({cnt}건) ", end="")
        print()
    else:
        print("없음")

    # ④ 변수별 척도 분류 참고
    print("\n④ 변수별 척도 분류 (참고)")
    print("-" * 60)
    척도_분류 = {
        "성별": "명목(nominal) — 범주 간 순서 없음",
        "연령": "비율(ratio) — 절대 영점(0세) 존재",
        "교육수준": "서열(ordinal) — 고졸이하 < 대졸 < 대학원이상",
        "소득": "비율(ratio) — 절대 영점(0원) 존재",
        "생활만족도": "서열(ordinal) — 1~5점 순서 있으나 간격 동일 보장 불가",
        "정치관심도": "서열(ordinal) — 생활만족도와 동일한 논리",
    }
    for var, desc in 척도_분류.items():
        print(f"  {var}: {desc}")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
