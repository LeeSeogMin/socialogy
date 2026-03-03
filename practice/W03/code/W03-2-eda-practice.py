"""
W03 실습 ②: 범주형 빈도표 + 집단별 박스플롯
=============================================
범주형 변수의 빈도를 확인하고, 교육수준별 소득 분포를 비교한다.

학습 목표:
  1. value_counts()로 범주형 변수의 빈도표를 만들 수 있다.
  2. groupby()로 집단별 기술통계를 구할 수 있다.
  3. 박스플롯으로 집단 간 분포 차이를 시각적으로 비교할 수 있다.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data() -> pd.DataFrame:
    """정제된 실습 데이터를 불러온다."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "social_survey_w03.csv"
    df = pd.read_csv(data_path, encoding="utf-8-sig")
    return df


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("W03 실습 ②: 범주형 빈도표 + 집단별 박스플롯")
    print("=" * 60)

    df = load_data()

    # ① 교육수준 빈도표
    print("\n① 교육수준 빈도표")
    print("-" * 60)
    freq = df["교육수준"].value_counts()
    freq_pct = df["교육수준"].value_counts(normalize=True)
    for edu in ["고졸이하", "대졸", "대학원이상"]:
        if edu in freq.index:
            print(f"  {edu}: {freq[edu]}명 ({freq_pct[edu]*100:.1f}%)")

    # ② 교육수준별 소득 집단 통계
    print("\n② 교육수준별 소득 요약")
    print("-" * 60)
    grouped = df.groupby("교육수준")["소득"].agg(["count", "mean", "median", "std"])
    for edu in ["고졸이하", "대졸", "대학원이상"]:
        if edu in grouped.index:
            row = grouped.loc[edu]
            print(f"  {edu}: {int(row['count'])}명, "
                  f"평균={row['mean']:.1f}, 중앙값={row['median']:.1f}, "
                  f"표준편차={row['std']:.1f}")

    # ③ 성별 빈도표
    print("\n③ 성별 빈도표")
    print("-" * 60)
    gender_freq = df["성별"].value_counts()
    for g in ["남성", "여성"]:
        if g in gender_freq.index:
            print(f"  {g}: {gender_freq[g]}명 ({gender_freq[g]/len(df)*100:.1f}%)")

    # ④ 집단별 박스플롯
    print("\n④ 교육수준별 소득 박스플롯 생성 중...")
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 5))
    # 교육수준 순서 지정
    edu_order = ["고졸이하", "대졸", "대학원이상"]
    data_groups = [df[df["교육수준"] == edu]["소득"] for edu in edu_order]
    bp = ax.boxplot(data_groups, labels=edu_order, patch_artist=True)

    # 색상 지정
    colors = ["#AEC6CF", "#B4D7A8", "#F4C2C2"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    ax.set_title("교육수준별 소득 분포")
    ax.set_ylabel("소득(만원)")
    ax.set_xlabel("교육수준")

    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w03_boxplot.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()
    print("  박스플롯 저장 완료: data/w03_boxplot.png")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
