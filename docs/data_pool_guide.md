# 공공 마이크로데이터 풀 접근 가이드

> 개인 리서치 브리프(10-15주)를 위한 6종 공공 데이터의 접근, 코드북, pandas 로딩 방법을 정리한 참고 자료.

**이 가이드의 용도**: 10주 CP1(데이터 확정) 시 본인이 분석할 데이터를 한 번 로드해볼 때 사용한다. 모든 데이터는 **회원가입 후 이용 신청**이 필요하며, 승인까지 1~3일 소요될 수 있으므로 **10주차 이전에 미리 신청**해 두어야 한다.

---

## 전체 비교표

| 데이터 | 조사 주기 | 표본 크기 | 주요 파일 형식 | 회원가입 | 분석 권장 주제 |
|---|---|---|---|---|---|
| KGSS | 매년 | 약 1,500명 | SPSS(.sav), Stata(.dta) | 필요 | 사회의식·정치·가족·노동 |
| KOWEPS | 매년 | 약 15,000명 | SPSS, SAS | 필요 | 빈곤·불평등·복지 |
| KELS | 3-6년 추적 | 약 5,000명 | SPSS | 필요 | 교육·학업·진로 |
| 청소년정책연구원 패널 | 매년 | 약 2,000명 | SPSS | 필요 | 청소년·진학·가족 |
| 지역사회건강조사 | 매년 | 약 23만명 | SAS, SPSS | 필요 | 건강행동·의료 |
| KOSIS 마이크로데이터 | 조사별 상이 | 다양 | 다양 | 필요 (MDIS) | 경제·인구·사회 |

**권장**: 학부 사회학 리서치 브리프는 **KGSS 또는 KOWEPS**로 시작하는 것이 가장 무난하다. 변수가 풍부하고 학술 선행연구도 많다.

---

## 1. KGSS (한국종합사회조사)

**URL**: https://kgss.skku.edu

**특징**
- 미국 GSS(General Social Survey)의 한국판. 사회학 학부 표준 데이터.
- 사회의식, 정치참여, 가족, 노동, 종교, 불평등 인식 등 사회학 전반 변수.
- 매년 조사되며, 누적 cumulative 파일 제공.

**접근 절차**
1. 성균관대학교 서베이리서치센터 웹사이트에서 회원가입
2. "데이터 신청" 메뉴에서 연구계획서 양식 작성 (수업 과제임을 명시)
3. 승인 후 다운로드 (보통 1-2일)

**파일 형식**: `.sav` (SPSS) 또는 `.dta` (Stata)

**pandas 로딩 예시**
```python
import pandas as pd

# SPSS 파일 로드 (pyreadstat 사용)
# pip install pyreadstat
import pyreadstat
df, meta = pyreadstat.read_sav("KGSS2022.sav")

# 변수 레이블 확인
print(meta.column_labels[:10])

# 결측 코드 NaN 변환 (KGSS는 -1, 99 등 사용)
import numpy as np
df = df.replace([-1, -8, -9, 99], np.nan)

print(df.shape)
print(df.head())
```

**코드북**: 다운로드 파일에 PDF 코드북 포함. **반드시 먼저 읽을 것**.

---

## 2. KOWEPS (한국복지패널)

**URL**: https://www.koweps.re.kr

**특징**
- 한국보건사회연구원 주관. 빈곤·불평등·복지 연구의 국내 표준.
- 가구 단위 + 가구원 단위 파일. 가구소득·지출·자산·복지수급 변수 풍부.
- 종단 자료지만, 학부 수준에서는 **1개 연도 횡단면**으로 분석해도 충분.

**접근 절차**
1. 회원가입 → 자료 신청
2. 신청서에 "학부 사회통계 수업 과제" 명시
3. 승인 후 원자료 다운로드

**파일 형식**: `.sav`, `.sas7bdat`

**pandas 로딩 예시**
```python
import pyreadstat
import numpy as np

# 가구원 파일 로드
df_person, meta = pyreadstat.read_sav("koweps_h18_2023_beta1.sav")

# KOWEPS 결측 코드
df_person = df_person.replace([-9, 999, 9999], np.nan)

# 가구 단위 파일과 병합 (hid 키)
df_house, _ = pyreadstat.read_sav("koweps_hp18_2023_beta1.sav")
merged = df_person.merge(df_house, on="h18_hid", suffixes=("", "_h"))
```

**주의**: 가구 파일과 가구원 파일을 병합해야 완전한 분석이 가능하다. 병합 키는 연도 wave에 따라 다름 (`h18_hid` 등).

---

## 3. KELS (한국교육종단연구)

**URL**: https://www.kedi.re.kr (한국교육개발원)

**특징**
- 초등학교 5학년부터 추적하는 교육 종단 연구.
- 학업성취, 진학, 가정환경, 진로 변수.
- 교육사회학 주제(가정배경-학업성취 관계 등)에 적합.

**접근 절차**
1. 한국교육개발원 교육통계 사이트에서 회원가입
2. KELS 데이터 신청 (학위 과제/연구 목적 명시)
3. 승인 후 다운로드

**파일 형식**: `.sav`

**pandas 로딩 예시**
```python
import pyreadstat
import numpy as np

df, meta = pyreadstat.read_sav("KELS2013_2_final.sav")
df = df.replace([-9, -8, -1, 99999], np.nan)
print(df.shape)
```

---

## 4. 청소년정책연구원 패널 (NYPI)

**URL**: https://www.nypi.re.kr → "데이터아카이브"

**특징**
- 한국청소년정책연구원의 대표 패널 자료.
- 아동·청소년 패널, 청년 사회·경제실태 조사 등 다양.
- 청소년 진학·가족·심리적응·진로 주제에 적합.

**접근 절차**
1. 데이터아카이브 회원가입
2. 원하는 조사 선택 후 "이용 신청"
3. 승인 후 다운로드

**파일 형식**: `.sav`, `.sas7bdat`

---

## 5. 지역사회건강조사

**URL**: https://chs.kdca.go.kr (질병관리청)

**특징**
- 전국 17개 시·도의 건강행태 조사. 표본 크기 매우 큼(약 23만명).
- 흡연, 음주, 운동, 정신건강, 의료이용 변수.
- **지역 비교** 연구에 적합 (시·군·구 단위 분석 가능).

**접근 절차**
1. 원시자료 이용 신청 페이지에서 회원가입
2. 이용 신청서 제출 (수업 과제 명시)
3. 승인 후 다운로드

**파일 형식**: `.sas7bdat`, `.sav`

**주의**: 표본 크기가 크기 때문에 거의 모든 검정이 유의하게 나온다. **효과크기(Cohen's d, Cramer's V)** 보고가 특히 중요하다.

---

## 6. KOSIS 마이크로데이터 (MDIS)

**URL**: https://mdis.kostat.go.kr

**특징**
- 통계청 마이크로데이터 통합서비스. 사회조사, 가계동향조사, 인구주택총조사 등 제공.
- 조사마다 성격과 변수가 크게 다르므로 **조사 단위로 접근**한다.
- 추천 조사: **사회조사** (격년, 삶의 질·가치관 중심), **가계동향조사** (소득·지출).

**접근 절차**
1. MDIS 회원가입 후 본인 인증
2. 원하는 조사 선택 → "이용 신청"
3. 일부 민감 자료는 KOSIS 통계데이터센터 방문 이용 필요 (학부 수업은 공개 자료만 사용)

**파일 형식**: 조사별 상이 (`.csv`, `.sav`, `.sas7bdat`)

---

## 공통: 대안 — KOSSDA (직접 발굴)

**URL**: https://kossda.snu.ac.kr

서울대학교 한국사회과학자료원. 위 6종에 포함되지 않는 다양한 학술 조사를 보관. 본인이 직접 발굴하여 사용할 경우 10주 CP1에서 교수 승인을 받는다 (가산점).

---

## Python 환경 준비 (공통)

`.sav`, `.dta`, `.sas7bdat` 등 통계 패키지 파일을 pandas로 읽으려면 **`pyreadstat`** 이 가장 안정적이다.

```bash
pip install pyreadstat
```

`.sav` 파일 빠른 로드:
```python
import pyreadstat

df, meta = pyreadstat.read_sav("file.sav")
# meta.column_names: 변수명
# meta.column_labels: 변수 설명 (한국어)
# meta.variable_value_labels: 값 레이블 딕셔너리
```

대안: `pd.read_spss("file.sav")` (단, `pyreadstat`이 내부 백엔드).

---

## 데이터 확정 체크리스트 (10주 CP1 직전)

- [ ] 회원가입 및 이용 신청 완료
- [ ] 승인 후 원자료 다운로드
- [ ] **코드북 PDF 확보 및 1회 통독**
- [ ] pandas 로드 성공 (스크린샷)
- [ ] 관심 변수 3-5개 이름·척도 확인
- [ ] 결측 코드 목록 파악 (코드북에서)

**이 체크리스트를 완료하지 않고 10주 CP1을 제출하는 것은 의미가 없다.** 데이터 확보는 CP1의 전제이지, CP1 과제의 일부가 아니다.
