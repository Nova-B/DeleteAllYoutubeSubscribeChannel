# YouTube 구독 채널 자동 해제 프로그램

YouTube에서 구독 중인 모든 채널을 자동으로 해제하는 프로그램입니다.

## 주요 기능

- 모든 구독 채널 자동 로드
- 한 번에 모든 구독 해제
- 진행 상황 실시간 표시
- 안전한 확인 절차

## 설치 방법

### 1. Python 설치
Python 3.7 이상이 필요합니다. [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드하세요.

### 2. 필요한 패키지 설치

#### 방법 1: uv 사용 (권장)

```bash
# uv 설치 (아직 설치하지 않은 경우)
pip install uv

# 가상환경 생성 및 패키지 설치
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

uv pip install -r requirements.txt
```

#### 방법 2: pip 사용

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install selenium webdriver-manager
```

## 사용 방법

### 1. 프로그램 실행

#### uv 가상환경을 사용하는 경우

```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 프로그램 실행
python unsubscribe_all.py
```

#### 일반 실행

```bash
python unsubscribe_all.py
```

### 2. 로그인

- 프로그램이 Chrome 브라우저를 자동으로 엽니다
- YouTube에 로그인하세요
- 로그인이 완료되면 터미널로 돌아와서 Enter를 누르세요

### 3. 구독 해제

- 프로그램이 자동으로 모든 구독 채널을 로드합니다
- 확인 메시지가 나타나면 'yes'를 입력하세요
- 구독 해제가 자동으로 진행됩니다

## 주의 사항

⚠️ **경고**: 이 프로그램은 모든 구독 채널을 해제합니다. 실행 전 신중히 고려하세요.

- 프로그램 실행 중에는 브라우저를 조작하지 마세요
- 인터넷 연결이 안정적인지 확인하세요
- 구독 채널이 많을 경우 시간이 오래 걸릴 수 있습니다
- YouTube의 정책에 따라 너무 빠른 작업은 제한될 수 있습니다

## 문제 해결

### Chrome 드라이버 오류
- 프로그램이 자동으로 Chrome 드라이버를 다운로드합니다
- Chrome 브라우저가 최신 버전인지 확인하세요

### 구독 버튼을 찾을 수 없음
- 페이지가 완전히 로드될 때까지 기다리세요
- YouTube 언어 설정을 확인하세요 (한국어 또는 영어)
- 수동으로 구독 관리 페이지로 이동해보세요

### 로그인 문제
- 2단계 인증을 완료하세요
- Chrome 프로필을 사용하려면 코드의 주석 처리된 부분을 활성화하세요

## 프로그램 중단

프로그램을 중단하려면 `Ctrl + C`를 누르세요.

## 기술 스택

- Python 3.7+
- Selenium WebDriver
- ChromeDriver (자동 설치)

## 면책 조항

이 프로그램은 교육 목적으로 제공됩니다. 사용으로 인한 모든 결과는 사용자의 책임입니다.

## 라이선스

MIT License
