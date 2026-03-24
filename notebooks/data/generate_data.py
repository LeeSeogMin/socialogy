"""
사회조사 데이터 생성 스크립트
- 각 주차별 분석 방법에 맞는 유의미한 상관관계를 가진 데이터 생성
- W03: 기술통계 (소득 우편향, 연령-소득, 소득-만족도 상관)
- W04: 카이제곱 (성별-정당, 연령-SNS 연관)
- W06: t검정 & ANOVA (성별-소득 차이, 교육수준-소득 차이)
- W07: 단순회귀 (교육연수→소득)
- W08: 다중회귀 (교육연수+경력연수+성별→소득)
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 200


# ============================================================
# W03: 기술통계 - 중심경향치와 산포도
# 필요 컬럼: 성별, 연령, 교육수준, 소득, 생활만족도, 정치관심도
# 핵심: 소득 우편향(mean > median), 연령-소득 관계, 소득-만족도 관계
# ============================================================
def generate_w03():
    # 성별
    gender = np.random.choice(["남성", "여성"], N, p=[0.5, 0.5])

    # 연령: 정규분포, 20-65세
    age = np.random.normal(38, 10, N).clip(20, 65).astype(int)

    # 교육수준: 연령과 약간 관련 (젊은층 대졸 비율 높음)
    edu = []
    for a in age:
        if a < 30:
            edu.append(np.random.choice(["고졸이하", "대졸", "대학원이상"], p=[0.15, 0.65, 0.20]))
        elif a < 45:
            edu.append(np.random.choice(["고졸이하", "대졸", "대학원이상"], p=[0.25, 0.55, 0.20]))
        else:
            edu.append(np.random.choice(["고졸이하", "대졸", "대학원이상"], p=[0.40, 0.45, 0.15]))
    edu = np.array(edu)

    # 교육수준 숫자 매핑 (내부용)
    edu_num = np.where(edu == "고졸이하", 0, np.where(edu == "대졸", 1, 2))

    # 소득: 우편향 분포 + 교육수준/연령/성별 영향
    # 기본 소득 = 로그정규분포 (자연스러운 우편향)
    base_income = np.random.lognormal(mean=5.6, sigma=0.55, size=N)
    # 교육 효과: 고졸 -60, 대졸 +0, 대학원 +100
    edu_effect = np.where(edu == "고졸이하", -60, np.where(edu == "대졸", 0, 100))
    # 연령 효과: 역U자형 (40대 정점)
    age_effect = -0.15 * (age - 42) ** 2 + 30
    # 성별 효과: 남성 약간 높음
    gender_effect = np.where(gender == "남성", 25, -25)
    # 최종 소득
    income = (base_income + edu_effect + age_effect + gender_effect).clip(80, 1200).astype(int)

    # 생활만족도: 소득과 양의 상관 (r ≈ 0.3~0.4)
    satisfaction_latent = 0.002 * income + np.random.normal(0, 0.9, N)
    satisfaction = np.digitize(satisfaction_latent, bins=np.percentile(satisfaction_latent, [20, 40, 60, 80])) + 1

    # 정치관심도: 연령과 양의 상관 (r ≈ 0.3)
    political_latent = 0.03 * age + np.random.normal(0, 0.8, N)
    political = np.digitize(political_latent, bins=np.percentile(political_latent, [20, 40, 60, 80])) + 1

    df = pd.DataFrame({
        "성별": gender,
        "연령": age,
        "교육수준": edu,
        "소득": income,
        "생활만족도": satisfaction,
        "정치관심도": political
    })
    return df


# ============================================================
# W04: 카이제곱 검정 - 범주형 변수 간 연관성
# 필요 컬럼: 성별, 연령대, 지지정당, 교육수준, SNS이용여부
# 핵심: 성별-정당 연관(Cramér's V ≈ 0.25), 연령대-SNS 연관
# ============================================================
def generate_w04():
    gender = np.random.choice(["남성", "여성"], N, p=[0.5, 0.5])

    # 연령대
    age_group = np.random.choice(["20대", "30대", "40대", "50대+"], N, p=[0.25, 0.25, 0.25, 0.25])

    # 지지정당: 성별에 따라 다른 확률 (성별-정당 연관성)
    party = []
    for g in gender:
        if g == "남성":
            party.append(np.random.choice(["A당", "B당", "C당", "무당파"], p=[0.35, 0.15, 0.20, 0.30]))
        else:
            party.append(np.random.choice(["A당", "B당", "C당", "무당파"], p=[0.15, 0.35, 0.25, 0.25]))
    party = np.array(party)

    # 교육수준
    edu = np.random.choice(["고졸이하", "대졸", "대학원이상"], N, p=[0.30, 0.50, 0.20])

    # SNS이용여부: 연령대와 강한 연관
    sns = []
    for ag in age_group:
        if ag == "20대":
            sns.append(np.random.choice(["이용", "미이용"], p=[0.85, 0.15]))
        elif ag == "30대":
            sns.append(np.random.choice(["이용", "미이용"], p=[0.70, 0.30]))
        elif ag == "40대":
            sns.append(np.random.choice(["이용", "미이용"], p=[0.50, 0.50]))
        else:
            sns.append(np.random.choice(["이용", "미이용"], p=[0.30, 0.70]))
    sns = np.array(sns)

    df = pd.DataFrame({
        "성별": gender,
        "연령대": age_group,
        "지지정당": party,
        "교육수준": edu,
        "SNS이용여부": sns
    })
    return df


# ============================================================
# W06: t검정 & ANOVA
# 필요 컬럼: 성별, 연령대, 교육수준, 소득, 생활만족도, 정치관심도
# 핵심: 성별-소득 유의한 차이(Cohen's d ≈ 0.35), 교육수준-소득 ANOVA 유의
# ============================================================
def generate_w06():
    gender = np.random.choice(["남성", "여성"], N, p=[0.5, 0.5])
    age_group = np.random.choice(["20대", "30대", "40대", "50대+"], N, p=[0.25, 0.25, 0.25, 0.25])

    # 교육수준
    edu = np.random.choice(["고졸", "대졸", "대학원"], N, p=[0.30, 0.50, 0.20])

    # 소득: 성별 + 교육수준에 따른 차이
    income = np.zeros(N)
    for i in range(N):
        # 기본 소득
        base = np.random.normal(330, 100)
        # 성별 효과: 남성 +18, 여성 -18 → 차이 약 36 (Cohen's d ≈ 0.35 with SD~105)
        if gender[i] == "남성":
            base += 18
        else:
            base -= 18
        # 교육수준 효과: 고졸 -80, 대졸 +0, 대학원 +100
        if edu[i] == "고졸":
            base -= 80
        elif edu[i] == "대학원":
            base += 100
        income[i] = base
    income = income.clip(80, 800).astype(int)

    # 생활만족도 (1-10): 소득과 양의 상관
    sat_latent = 0.008 * income + np.random.normal(0, 1.5, N)
    satisfaction = np.digitize(sat_latent, bins=np.percentile(sat_latent, np.arange(10, 100, 10))) + 1

    # 정치관심도 (1-10)
    pol_latent = np.random.normal(5.5, 2, N)
    # 연령대 효과
    for i, ag in enumerate(age_group):
        if ag == "50대+":
            pol_latent[i] += 1.5
        elif ag == "40대":
            pol_latent[i] += 0.5
        elif ag == "20대":
            pol_latent[i] -= 1.0
    political = pol_latent.clip(1, 10).round().astype(int)

    df = pd.DataFrame({
        "성별": gender,
        "연령대": age_group,
        "교육수준": edu,
        "소득": income,
        "생활만족도": satisfaction,
        "정치관심도": political
    })
    return df


# ============================================================
# W07: 단순 선형 회귀
# 필요 컬럼: 연령, 교육연수, 소득, 생활만족도, 정치관심도, 성별
# 핵심: 교육연수→소득 (β₁ ≈ 45, R² ≈ 0.28)
# ============================================================
def generate_w07():
    gender = np.random.choice(["남성", "여성"], N, p=[0.5, 0.5])

    # 연령: 20-65
    age = np.random.normal(38, 10, N).clip(20, 65).astype(int)

    # 교육연수: 6-18 (연령과 약간 음의 상관 - 젊은 세대가 교육 더 받음)
    edu_years = np.zeros(N)
    for i in range(N):
        if age[i] < 30:
            edu_years[i] = np.random.normal(15, 2)
        elif age[i] < 45:
            edu_years[i] = np.random.normal(14, 2.5)
        else:
            edu_years[i] = np.random.normal(12.5, 3)
    edu_years = edu_years.clip(6, 18).astype(int)

    # 소득: 교육연수 + 연령 + 노이즈
    # 목표: 교육연수 β ≈ 45, R² ≈ 0.28
    # 소득 = 100 + 45*교육연수 + noise(SD≈180)
    income = 100 + 45 * edu_years + np.random.normal(0, 180, N)
    # 연령 효과 (약간의 추가 효과)
    income += 2 * age
    # 성별 효과
    income += np.where(gender == "남성", 30, -30)
    income = income.clip(100, 1200).astype(int)

    # 생활만족도: 소득과 양의 상관
    sat_latent = 0.002 * income + 0.01 * edu_years + np.random.normal(0, 0.7, N)
    satisfaction = np.digitize(sat_latent, bins=np.percentile(sat_latent, [20, 40, 60, 80])) + 1

    # 정치관심도: 연령과 양의 상관
    pol_latent = 0.03 * age + np.random.normal(0, 0.8, N)
    political = np.digitize(pol_latent, bins=np.percentile(pol_latent, [20, 40, 60, 80])) + 1

    df = pd.DataFrame({
        "연령": age,
        "교육연수": edu_years,
        "소득": income,
        "생활만족도": satisfaction,
        "정치관심도": political,
        "성별": gender
    })
    return df


# ============================================================
# W08: 다중 회귀
# 필요 컬럼: 성별, 연령, 교육연수, 경력연수, 소득, 생활만족도, 정치관심도
# 핵심: 교육연수+경력연수+성별→소득, VIF<5, R²≈0.62
# ============================================================
def generate_w08():
    gender = np.random.choice(["남성", "여성"], N, p=[0.5, 0.5])
    gender_dummy = np.where(np.array(gender) == "남성", 1, 0)

    # 연령: 20-65
    age = np.random.normal(40, 10, N).clip(22, 65).astype(int)

    # 교육연수: 6-18 (연령과 약간 상관)
    edu_years = np.zeros(N)
    for i in range(N):
        if age[i] < 30:
            edu_years[i] = np.random.normal(15, 2)
        elif age[i] < 45:
            edu_years[i] = np.random.normal(14, 2.5)
        else:
            edu_years[i] = np.random.normal(12.5, 2.5)
    edu_years = edu_years.clip(6, 18).astype(int)

    # 경력연수: 교육연수와 양의 상관 (교육↑ → 전문경력↑)
    # 이렇게 해야 단순회귀→다중회귀 시 교육연수 계수가 '감소'하는 패턴이 나옴
    career_years = (edu_years * 0.6 + np.random.normal(6, 4, N)).clip(0, 30).astype(int)

    # 소득: 교육연수 + 경력연수 + 성별 → 소득
    # 단순회귀 시 교육β ≈ 37 + 15*0.6 = 46 (경력 효과 포함)
    # 다중회귀 시 교육β ≈ 37, 경력β ≈ 15 (분리됨)
    income = (100
              + 37 * edu_years
              + 15 * career_years
              + 42 * gender_dummy
              + np.random.normal(0, 80, N))
    income = income.clip(150, 1200).astype(int)

    # 생활만족도
    sat_latent = 0.002 * income + np.random.normal(0, 0.7, N)
    satisfaction = np.digitize(sat_latent, bins=np.percentile(sat_latent, [20, 40, 60, 80])) + 1

    # 정치관심도
    pol_latent = 0.025 * age + np.random.normal(0, 0.8, N)
    political = np.digitize(pol_latent, bins=np.percentile(pol_latent, [20, 40, 60, 80])) + 1

    df = pd.DataFrame({
        "성별": gender,
        "연령": age,
        "교육연수": edu_years,
        "경력연수": career_years,
        "소득": income,
        "생활만족도": satisfaction,
        "정치관심도": political
    })
    return df


# ============================================================
# 데이터 생성 및 저장
# ============================================================
if __name__ == "__main__":
    import os
    from scipy import stats
    from scipy.stats import chi2_contingency

    output_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("사회조사 데이터 생성")
    print("=" * 60)

    # --- W03 ---
    df03 = generate_w03()
    df03.to_csv(os.path.join(output_dir, "social_survey_w03.csv"), index=False, encoding="utf-8-sig")
    print("\n[W03] 기술통계 데이터")
    print(f"  소득 평균: {df03['소득'].mean():.1f}, 중앙값: {df03['소득'].median():.1f} (우편향: mean > median)")
    print(f"  연령 평균: {df03['연령'].mean():.1f}, 중앙값: {df03['연령'].median():.1f}")
    print(f"  소득-생활만족도 상관: {df03['소득'].corr(df03['생활만족도']):.3f}")
    print(f"  연령-정치관심도 상관: {df03['연령'].corr(df03['정치관심도']):.3f}")

    # --- W04 ---
    df04 = generate_w04()
    df04.to_csv(os.path.join(output_dir, "social_survey_w04.csv"), index=False, encoding="utf-8-sig")
    ct_gender_party = pd.crosstab(df04["성별"], df04["지지정당"])
    chi2, p, dof, _ = chi2_contingency(ct_gender_party)
    V = np.sqrt(chi2 / (N * (min(ct_gender_party.shape) - 1)))
    print(f"\n[W04] 카이제곱 데이터")
    print(f"  성별×정당 카이제곱: χ²={chi2:.2f}, p={p:.4f}, Cramér's V={V:.3f}")
    ct_age_sns = pd.crosstab(df04["연령대"], df04["SNS이용여부"])
    chi2_sns, p_sns, _, _ = chi2_contingency(ct_age_sns)
    V_sns = np.sqrt(chi2_sns / (N * (min(ct_age_sns.shape) - 1)))
    print(f"  연령대×SNS 카이제곱: χ²={chi2_sns:.2f}, p={p_sns:.4f}, Cramér's V={V_sns:.3f}")

    # --- W06 ---
    df06 = generate_w06()
    df06.to_csv(os.path.join(output_dir, "social_survey_w06.csv"), index=False, encoding="utf-8-sig")
    male_inc = df06[df06["성별"] == "남성"]["소득"]
    female_inc = df06[df06["성별"] == "여성"]["소득"]
    t_stat, t_p = stats.ttest_ind(male_inc, female_inc)
    pooled_sd = np.sqrt((male_inc.var() + female_inc.var()) / 2)
    cohens_d = (male_inc.mean() - female_inc.mean()) / pooled_sd
    print(f"\n[W06] t검정 & ANOVA 데이터")
    print(f"  남성 소득 평균: {male_inc.mean():.1f}, 여성: {female_inc.mean():.1f}")
    print(f"  t검정: t={t_stat:.2f}, p={t_p:.4f}, Cohen's d={cohens_d:.3f}")
    groups_edu = [df06[df06["교육수준"] == e]["소득"] for e in ["고졸", "대졸", "대학원"]]
    f_stat, f_p = stats.f_oneway(*groups_edu)
    print(f"  ANOVA(교육수준→소득): F={f_stat:.2f}, p={f_p:.4f}")
    for e in ["고졸", "대졸", "대학원"]:
        g = df06[df06["교육수준"] == e]["소득"]
        print(f"    {e} 평균: {g.mean():.1f} (SD={g.std():.1f})")

    # --- W07 ---
    df07 = generate_w07()
    df07.to_csv(os.path.join(output_dir, "social_survey_w07.csv"), index=False, encoding="utf-8-sig")
    # scipy로 간단 회귀 검증
    slope07, intercept07, r07, p07, se07 = stats.linregress(df07["교육연수"], df07["소득"])
    print(f"\n[W07] 단순회귀 데이터")
    print(f"  교육연수→소득: β₁={slope07:.1f}, p={p07:.4f}")
    print(f"  R²={r07**2:.3f}")
    print(f"  교육연수-소득 상관: {df07['교육연수'].corr(df07['소득']):.3f}")
    print(f"  연령-소득 상관: {df07['연령'].corr(df07['소득']):.3f}")

    # --- W08 ---
    df08 = generate_w08()
    df08.to_csv(os.path.join(output_dir, "social_survey_w08.csv"), index=False, encoding="utf-8-sig")
    # 단순 상관으로 검증
    print(f"\n[W08] 다중회귀 데이터")
    print(f"  교육연수-소득 상관: {df08['교육연수'].corr(df08['소득']):.3f}")
    print(f"  경력연수-소득 상관: {df08['경력연수'].corr(df08['소득']):.3f}")
    male08 = df08[df08['성별'] == '남성']['소득']
    female08 = df08[df08['성별'] == '여성']['소득']
    print(f"  남성 소득: {male08.mean():.1f}, 여성: {female08.mean():.1f}")
    # numpy 다중회귀 검증
    df08_temp = df08.copy()
    df08_temp["성별_더미"] = (df08_temp["성별"] == "남성").astype(int)
    X = np.column_stack([np.ones(N), df08_temp["교육연수"], df08_temp["경력연수"], df08_temp["성별_더미"]])
    y = df08_temp["소득"].values
    betas = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ betas
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    print(f"  다중회귀 β: 절편={betas[0]:.1f}, 교육연수={betas[1]:.1f}, 경력연수={betas[2]:.1f}, 성별={betas[3]:.1f}")
    print(f"  R²={r2:.3f}")

    print("\n" + "=" * 60)
    print("모든 데이터 생성 완료!")
    print("=" * 60)
