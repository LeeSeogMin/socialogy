"""
W03 실습 ①: 기술통계 + 히스토그램
==================================
수치형 변수의 기술통계와 히스토그램으로 분포를 파악한다.

학습 목표:
  1. 평균, 중앙값, 표준편차를 계산하고 비교할 수 있다.
  2. 히스토그램에 평균/중앙값 선을 표시할 수 있다.
  3. 평균-중앙값 차이로 분포의 치우침을 판단할 수 있다.
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
    print("W03 실습 ①: 기술통계 + 히스토그램")
    print("=" * 60)

    df = load_data()

    # ① 수치형 변수 기술통계
    target_cols = ["연령", "소득", "생활만족도"]
    print("\n① 수치형 변수 기술통계")
    print("-" * 60)
    print(df[target_cols].describe())

    # ② 평균 vs 중앙값 비교 (분포 형태 판정)
    print("\n② 평균 vs 중앙값 비교")
    print("-" * 60)
    print(f"{'변수':>8} {'평균':>8} {'중앙값':>8} {'표준편차':>8} {'차이':>8} {'판정':>12}")
    for col in target_cols:
        mean_val = df[col].mean()
        med_val = df[col].median()
        std_val = df[col].std()
        diff = mean_val - med_val
        # 판정: 차이가 표준편차의 10% 이내면 대체로 대칭
        if abs(diff) < std_val * 0.15:
            shape = "대체로 대칭"
        elif diff > 0:
            shape = "우치우침"
        else:
            shape = "좌치우침"
        print(f"  {col:>6} {mean_val:>8.1f} {med_val:>8.1f} {std_val:>8.1f} {diff:>+8.1f} {shape:>12}")

    # ③ 히스토그램 (평균/중앙값 선 포함)
    print("\n③ 히스토그램 생성 중...")
    # 한글 폰트 설정 (Windows)
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, col in enumerate(target_cols):
        df[col].hist(bins=15, ax=axes[i], edgecolor="black", alpha=0.7)
        mean_val = df[col].mean()
        med_val = df[col].median()
        axes[i].axvline(mean_val, color="r", linestyle="--", linewidth=1.5, label=f"평균({mean_val:.1f})")
        axes[i].axvline(med_val, color="g", linestyle="-", linewidth=1.5, label=f"중앙값({med_val:.1f})")
        axes[i].set_title(f"{col} 분포")
        axes[i].legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(
        Path(__file__).resolve().parent.parent / "data" / "w03_histograms.png",
        dpi=150, bbox_inches="tight",
    )
    plt.show()
    print("  히스토그램 저장 완료: data/w03_histograms.png")

    print("\n" + "=" * 60)
    print("실습 완료!")
    print("=" * 60)
