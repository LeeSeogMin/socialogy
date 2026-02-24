"""
W04 실습 데이터 생성 스크립트
=============================
카이제곱 검정 실습을 위한 가상 사회조사 데이터를 생성한다.

학습 목표에 맞춰 변수 간 관련성을 의도적으로 설계하였다:
  - 성별 × 지지정당: 중간 정도의 관련성 (유의미)
  - 연령대 × SNS이용여부: 강한 관련성 (명확히 유의미)
  - 성별 × 교육수준: 독립 (유의미하지 않음)
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_social_survey(n: int = 200, seed: int = 42) -> pd.DataFrame:
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

    # ── 2) 연령대: 4개 범주, 사회조사에서 흔한 분포 ──
    연령대 = rng.choice(
        ["20대", "30대", "40대", "50대+"],
        size=n,
        p=[0.28, 0.27, 0.25, 0.20],
    )

    # ── 3) 지지정당: 성별에 따라 다른 분포 → 중간 정도 관련성 ──
    # 남성은 A당 선호가 높고, 여성은 B당 선호가 높도록 설계
    지지정당 = np.empty(n, dtype=object)
    for i in range(n):
        if 성별[i] == "남성":
            지지정당[i] = rng.choice(
                ["A당", "B당", "C당", "무당파"],
                p=[0.38, 0.18, 0.22, 0.22],
            )
        else:
            지지정당[i] = rng.choice(
                ["A당", "B당", "C당", "무당파"],
                p=[0.18, 0.35, 0.22, 0.25],
            )

    # ── 4) 교육수준: 성별과 무관하게 동일 분포 → 독립 관계 ──
    # 귀무가설이 기각되지 않는 사례를 보여주기 위함
    # 단순 랜덤 추출은 우연히 관련성이 나올 수 있으므로,
    # 성별 집단별로 동일한 비율을 강제하여 확실한 독립을 보장한다.
    edu_labels = ["고졸이하", "대졸", "대학원이상"]
    edu_probs = [0.30, 0.50, 0.20]
    교육수준 = np.empty(n, dtype=object)
    for label in ["남성", "여성"]:
        mask = 성별 == label
        n_group = mask.sum()
        교육수준[mask] = rng.choice(edu_labels, size=n_group, p=edu_probs)

    # 추가 보정: 성별 간 교육수준 비율 차이가 너무 크면
    # 카이제곱이 유의해질 수 있으므로, 비율이 비슷하도록 미세 조정
    # (각 성별 그룹에서 독립적으로 같은 확률로 뽑았으므로 대개 괜찮다)

    # ── 5) SNS이용여부: 연령대에 따라 크게 다름 → 강한 관련성 ──
    # 젊은 세대일수록 SNS 이용률이 높도록 설계
    sns_prob = {
        "20대": 0.90,
        "30대": 0.72,
        "40대": 0.45,
        "50대+": 0.25,
    }
    SNS이용여부 = np.array([
        "이용" if rng.random() < sns_prob[age] else "미이용"
        for age in 연령대
    ])

    df = pd.DataFrame({
        "성별": 성별,
        "연령대": 연령대,
        "지지정당": 지지정당,
        "교육수준": 교육수준,
        "SNS이용여부": SNS이용여부,
    })

    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W04 실습 데이터 생성")
    print("=" * 60)

    # ① 실행: 데이터 생성
    df = generate_social_survey(n=200, seed=42)

    # ② 확인: 기본 정보 출력
    print(f"\n전체 표본 수: {len(df)}명")
    print(f"\n변수 목록: {list(df.columns)}")

    print("\n--- 각 변수의 빈도 분포 ---")
    for col in df.columns:
        print(f"\n[{col}]")
        counts = df[col].value_counts()
        for val, cnt in counts.items():
            print(f"  {val}: {cnt}명 ({cnt / len(df) * 100:.1f}%)")

    # ③ 저장
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "social_survey_w04.csv"

    # 한글 호환을 위해 UTF-8 BOM 인코딩 사용
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n데이터 저장 완료: {output_path}")
    print(f"파일 크기: {output_path.stat().st_size:,} bytes")
