# %% [markdown]
# # 사회통계 강의 - 실습 환경 자동 설정
#
# 이 파일은 사회통계 강의 실습에 필요한 Python 환경을 자동으로 설정합니다.
#
# **기능:**
# 1. `.venv` 가상환경 생성 (이미 있으면 건너뜀)
# 2. 필요한 패키지 일괄 설치
# 3. Jupyter 커널 등록 (VSCode에서 선택 가능)
#
# **지원 OS:** Windows, macOS, Linux
# **Python 요구 사항:** 3.10 이상

# %% [markdown]
# ---
# ## 1단계: Python 버전 확인

# %%
import sys
import platform
import os

py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

# 이 파일의 위치를 프로젝트 루트로 사용
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

print("=" * 56)
print("  사회통계 강의 - 실습 환경 자동 설정")
print("=" * 56)
print(f"  OS      : {platform.system()} ({platform.machine()})")
print(f"  Python  : {py_ver} ({sys.executable})")
print(f"  프로젝트: {PROJECT_ROOT}")
print("=" * 56)

if sys.version_info < (3, 10):
    print("\n❌ Python 3.10 이상이 필요합니다.")
    print(f"   현재 버전: {py_ver}")
else:
    print(f"\n✅ Python {py_ver} — 요구 사항 충족!")

# %% [markdown]
# ---
# ## 2단계: 가상환경 생성

# %%
import subprocess
from pathlib import Path

VENV_DIR = Path(PROJECT_ROOT) / ".venv"
IS_WIN = platform.system() == "Windows"


def get_venv_python():
    """가상환경 내 Python 경로 (OS별)"""
    if IS_WIN:
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run_cmd(cmd):
    """크로스플랫폼 subprocess 실행"""
    kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True}
    if IS_WIN:
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"  ⚠️ 오류: {result.stderr.strip()}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


venv_python = get_venv_python()

if VENV_DIR.exists() and venv_python.exists():
    print(f"✅ 가상환경이 이미 존재합니다: {VENV_DIR}")
else:
    if VENV_DIR.exists():
        print("⚠️ 가상환경이 불완전합니다. 재생성합니다...")
        import shutil
        shutil.rmtree(VENV_DIR)
    print(f"📦 가상환경 생성 중: {VENV_DIR}")
    run_cmd([sys.executable, "-m", "venv", str(VENV_DIR)])
    print("✅ 가상환경 생성 완료!")

# %% [markdown]
# ---
# ## 3단계: 패키지 설치

# %%
PACKAGES = [
    "ipykernel",
    "nbformat",
    "numpy",
    "pandas",
    "plotly",
    "scipy",
    "matplotlib",
    "networkx",
    "statsmodels",
]

python = str(get_venv_python())

print("📦 pip 업그레이드 중...")
run_cmd([python, "-m", "pip", "install", "--upgrade", "pip", "-q"])

print(f"📦 패키지 설치 중: {', '.join(PACKAGES)}")
run_cmd([python, "-m", "pip", "install"] + PACKAGES + ["-q"])
print("✅ 패키지 설치 완료!")

# %% [markdown]
# ---
# ## 4단계: Jupyter 커널 등록

# %%
KERNEL_NAME = "socialogy"
KERNEL_DISPLAY = "사회통계 강의 (Python 3)"

print(f"📦 Jupyter 커널 등록 중: {KERNEL_DISPLAY}")
run_cmd([
    python, "-m", "ipykernel", "install",
    "--user",
    "--name", KERNEL_NAME,
    "--display-name", KERNEL_DISPLAY,
])
print("✅ 커널 등록 완료!")

# %% [markdown]
# ---
# ## 5단계: 설치 확인

# %%
print("\n" + "=" * 56)
print("  🎉 설정 완료!")
print("=" * 56)
print()
print("  1. VSCode에서 파일 → 폴더 열기 → socialogy 폴더 선택")
print("  2. notebooks/ 폴더의 .ipynb 파일 열기")
print("  3. 우측 상단 [커널 선택] 클릭")
print(f'  4. "{KERNEL_DISPLAY}" 선택')
print("  5. 첫 번째 코드 셀 실행 (▶ 또는 Ctrl+Enter)")
print("=" * 56)

# 패키지 import 확인
print("\n📋 설치된 패키지 확인:")
for pkg in PACKAGES:
    try:
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if IS_WIN:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.run(
            [python, "-c", f"import {pkg}"],
            check=True, **kwargs
        )
        print(f"  ✅ {pkg}")
    except subprocess.CalledProcessError:
        print(f"  ❌ {pkg} — 설치 실패")
