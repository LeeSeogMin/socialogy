### 주의사항: 모든 컴퓨터 조작에서 한글 사용금지하고 반드시 영어문자를 사용해야 한다. 폴더명, 파일명 등등. 한글 사랑과 별개의 문제로서 피할 수 없는 문제이다. 

### 검색 - cmd - 작업표시줄에 고정 

# Git & GitHub & Copilit 가이드

## 1단계: Git 설치 (3분)

**Windows**: https://git-scm.com/download/win → 다운로드 후 설치 (기본값 OK)

**macOS**: 터미널에서 실행

```bash
xcode-select --install
```

설치 확인:

```bash
git --version
```

## 2단계: GitHub 가입 (2분)

1. https://github.com 접속
2. "Sign up" → 학교 이메일로 가입
3. 이메일 인증 

또는 구글 아이디 로그인도 됨

username 반드시 복사해놓을것 

## 3단계: 로컬 연결 (1분)

> VSCode 통합 터미널(Ctrl+`), CMD, PowerShell 중 어디서든 실행 가능

```bash
git config --global user.name "홍길동"   <- 복사해놓은 유저네임 사용
git config --global user.email "학교이메일@ac.kr"
```


# GitHub Copilot 대학생 무료 사용 방법

GitHub는 **Copilot Free** (제한된 무료 플랜)와 **Copilot Pro** (고급 기능 풀버전)을 구분해서 운영하고 있으며,

**검증된 학생**은 **Copilot Pro**를 **학생 신분 유지 기간 동안 완전 무료**로 사용할 수 있습니다.

### 현재(2026년) 상황 요약

| 구분               | 대상자                     | 가격     | 주요 제한사항                                   | 모델/기능 수준          |
| ------------------ | -------------------------- | -------- | ----------------------------------------------- | ----------------------- |
| Copilot Free       | 누구나                     | 무료     | 월 2,000 코드 완성, 50 채팅 등 매우 제한적      | 기본 모델               |
| Copilot Pro        | 일반인                     | 월 $10   | 300 premium requests + 추가 과금 가능           | 최신 모델 풀 액세스     |
| Copilot Pro (학생) | GitHub Education 검증 학생 | **무료** | 월 300 premium requests (초과 시 다음달 초기화) | Pro 풀 기능 + 최신 모델 |

→ **우리가 원하는 건 Copilot Pro 무료**이며, 이를 위해서는 **GitHub Student Developer Pack** 승인이 필수입니다.

### 2026년 최신 정확한 등록 절차 (단계별)

1. **GitHub 계정 준비**
   - 이미 계정이 있다면 로그인
   - 없다면 [https://github.com](https://github.com/) 에서 새로 생성 (학교 이메일)
   - 기존 계정이 있으면 설정(https://github.com/settings/emails)에서 학교 이메일(.ac.kr)을 추가
   - **학교 이메일을 primary email(기본 이메일)로 설정** (드롭다운에서 선택 후 Save → 인증 인식을 도움. 나중에 개인 이메일로 되돌릴 수 있음)
   - 이메일 추가 후 verification link(인증 링크)를 클릭해 verified 상태로 만들기
2. **GitHub Student Developer Pack 신청 페이지 이동**

   https://education.github.com/pack



3. **학생 신분 증명** (가장 중요한 단계)

   대부분의 한국 대학생이 성공하는 순서 (우선순위 높은 순) :

   | 순위 | 증빙 방법                       | 성공률    | 소요시간    | 비고                                        |
   | ---- | ------------------------------- | --------- | ----------- | ------------------------------------------- |
   | 1    | 학교 공식 이메일 (.ac.kr)       | 매우 높음 | 즉시~수시간 | 대부분 자동 승인                            |
   | 2    | 학생증 사진 (재학증명서) 업로드 | 높음      | 1~5일       | 선명하게 촬영, 이름·학번·유효기간 보여야 함 |
   | 3    | 재학증명서 PNG 파일 업로드           | 높음      | 1~7일       | 최근 3개월 이내 발급본                      |
   | 4    | 등록금 영수증 + 신분증          | 중간      | 3~10일      | 최후의 수단                                 |

   → **한국 4년제 대학 재학생이라면 대부분 학교 이메일만으로 1~24시간 내 자동 승인**됩니다.
   -> 재학증명서는 영문으로 받고 파일이 pdf 형태이니 아래의 사이트에서 이미지 파일로 변환한다. 
   [text](https://smallpdf.com/kr/pdf-to-jpg?mu=b5Vg&mau=b5Vg&utm_campaign=21930591768_179389838308_pdf%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%B3%80%ED%99%98&utm_source=google&utm_medium=cpc&gad_source=1&gad_campaignid=21930591768&gbraid=0AAAAAoxWdI5FDXktGvqJ9ZNyQLXTc8MDQ&gclid=CjwKCAiAtq_NBhA_EiwA78nNWFiUmnB1IOiTjRV7UCOpP2bQMjfGXFEvuXCIDTDwhh8wizmKkR-nyxoC0hQQAvD_BwE)

4. **승인 확인**
   - https://education.github.com/pack 에서 "Your pack" 상태 확인
   - 승인 메일 도착 (보통 "You're all set!" 제목)
5. **Copilot Pro 무료 활성화** (승인 후 바로 가능)

   두 가지 방법 중 편한 것 선택:

   방법 A (가장 확실)
   - https://github.com/settings/copilot 이동
   - "Code, planning, and automation" → Copilot 클릭
   - 학생 혜택으로 무료 가입 버튼 나타남 → 클릭

   방법 B
   - https://github.com/features/copilot 로 이동
   - 학생으로 인식되면 "무료로 시작" 또는 "Claim free access" 버튼 등장

   방법 C (학생/교사 전용 무료 signup 페이지)
   - https://github.com/github-copilot/free_signup 으로 직접 이동

   > **주의**: 신용카드 입력이 요구되면 진행하지 마십시오. 학생 혜택은 완전 무료이며 결제 정보가 필요하지 않습니다.

6. **VS Code 등 에디터에서 사용 시작**
   - GitHub 계정으로 Copilot 확장 로그인
   - 학생 혜택이 정상 적용되어 풀 Pro 기능 사용 가능

### 주의사항 (2026년 기준 자주 발생하는 문제)

- 승인 후에도 바로 안 보일 때 → 72시간까지 기다린 뒤 재로그인 시도 (Incognito/시크릿 모드 사용 추천). 혜택 동기화에 72시간~최대 2주가 소요될 수 있음
- "무료 버튼이 안 보임" → 캐시 지우기 / 다른 브라우저 시도 / primary email을 학교 이메일로 재설정 후 대기 / https://github.com/settings/copilot 직접 들어가기
- 인증 실패 시 → GitHub Support(https://support.github.com/contact/education)에 티켓 제출 (카테고리: "Student having trouble redeeming offers")
- 월 300 premium requests 제한은 학생도 동일 (과거에는 무제한이었으나 2025년 중반부터 변경됨)
- 졸업하면 자동으로 Pro 유료 전환됨 → 재학생 기간에 최대한 활용 권장
- 공식 문서 참조: https://docs.github.com/en/education

위 방법은 2026년 2월 6일 기준 GitHub 공식 문서 및 실제 학생 사례들을 종합한 **현재 가장 정확한 절차**입니다.

학교 이메일이 있다면 거의 100% 성공한다고 봐도 무방합니다.
---


## 🚀 시작하기

### 1단계: VSCode 설치

1. https://code.visualstudio.com/ 에서 다운로드 후 설치
2. 설치 시 **"Add to PATH" 옵션 체크** 권장
3. 설치 후 실행하여 다음 확장(Extensions)을 설치:
   - **Python** (Microsoft) — Python 개발 지원
   - **Jupyter** (Microsoft) — 노트북(.ipynb) 실행 지원

> 좌측 사이드바 확장 아이콘(□) 클릭 → 검색창에 "Python", "Jupyter" 입력 → Install 
> 파일 메뉴 - 자동 저장 클릭

### 2단계: Python 설치

1. https://www.python.org/downloads/ 에서 **Python 3.12** 이상 다운로드
2. 설치 프로그램 실행
3. **⚠️ 첫 화면에서 반드시 "Add python.exe to PATH" 체크** ← 가장 중요!
4. **"Install Now"** 클릭

설치 확인 (Windows: `Win+R` → `cmd` 입력 → 확인):

```bash
python --version
```

`Python 3.x.x`가 출력되면 성공입니다. 만약 `'python' is not recognized...` 오류가 나면 PATH 등록이 안 된 것이므로 Python을 제거 후 3번을 확인하며 재설치하세요. 

### 3단계: Copilot 확장 설치

1. VS Code를 실행한다.
2. 왼쪽 사이드바에서 **Extensions**(확장) 아이콘을 클릭한다.
3. 검색창에 `GitHub Copilot`을 입력하고 **GitHub Copilot** 확장을 설치한다.
4. 같은 방법으로 **GitHub Copilot Chat** 확장도 설치한다.
5. Command Palette(Ctrl+Shift+P 또는 Cmd+Shift+P)를 열고 "Copilot: Sign In"을 선택하여 GitHub 계정으로 로그인한다.
6. 우측 하단 상태바에서 Copilot 아이콘이 활성화되었는지 확인한다.


### 4단계: 저장소 클론

명령 프롬프트 열기 (Windows: `Win+R` → `cmd` 입력 → 확인):

```bash
cd C:\
git clone https://github.com/LeeSeogMin/socialogy.git
```

`C:\socialogy` 폴더가 생성되면 성공입니다.

---

만일 github copilot 실패햇을때 아래를 사용합니다. 

## Gemini CLI 설치 및 실행

### 1단계: Node.js 설치 확인
- Gemini CLI는 npm 방식 설치를 권장하므로 Node.js 필수
- https://nodejs.org 에서 LTS 버전 다운로드 후 설치
- npm은 Node.js와 함께 자동 설치됨

### 2단계: vscode 에서 새터미널 열기
- PowerShell 실행

### 3단계: Gemini CLI 설치
```bash
npm install -g @google/gemini-cli 

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned 
```

### 4단계: 실행
```bash
gemini   

중간에 브라우저에서 구글로 로그인하는 과정을 거치니 브라우저를 잘 살핀다. 

구글로그인 후에 성공했다는 메시지와 함께 r 을 입력하라는 메시지가 나오니 따라서 하면 잠시 후에 로그인된다. 

터미널에서 마우스 우클릭 후 패널위치를 오른쪽으로 한다. 
```

### 5단계: 인증 설정
처음 실행 시 다음 중 선택:
- **Google 계정 로그인** (권장)
- **Gemini API Key**
- **Vertex AI**
