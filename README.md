# sibd_pyerr - 선일빅데이터고등학교 파이썬 에러 한글화

파이썬 예외 메시지를 한글로 출력해주는 라이브러리입니다.

## 🚀 주요 기능

- **문법 오류 검출**: SyntaxError를 포함한 모든 파이썬 에러를 한글로 표시
- **CLI 래퍼**: `sibd-py` 명령어로 파이썬 파일 실행 시 자동 문법 검사
- **주피터 노트북 통합**: IPython 확장으로 자동 에러 한글화
- **자동 프로필 설정**: 한 번 설정하면 모든 주피터 세션에 자동 적용

## 📦 설치

```bash
pip install sibd_pyerr
```

## 🔧 사용법

### 1. 기본 사용법

```python
import sibd_pyerr
sibd_pyerr.install()
```

### 2. CLI 래퍼 사용법

```bash
# 문법 검사 후 파이썬 파일 실행
sibd-py your_script.py

# 또는 모듈로 실행
python -m sibd_pyerr.cli your_script.py
```

### 3. 주피터 노트북에서 사용

#### 자동 설정 (권장)
```python
# 한 번만 실행하면 모든 주피터 세션에 자동 적용
import sibd_pyerr
sibd_pyerr.setup_profile()
```

#### 수동 설정
```python
# 주피터 노트북에서 직접 로드
%load_ext sibd_pyerr.ipyext
```

#### 매직 명령어 사용
```python
# 문법 검사 후 코드 실행
%sibd_py print("Hello World")

# 에러 핸들러 재설치
%sibd_py_install
```

## 🎯 지원하는 에러 타입

### 문법 오류 (SyntaxError)
- 괄호 미완성
- 문자열 미완성
- 들여쓰기 오류
- 잘못된 대입문
- f-string 오류

### 런타임 오류
- NameError (정의되지 않은 변수)
- TypeError (타입 오류)
- IndexError (인덱스 오류)
- KeyError (키 오류)
- ZeroDivisionError (0으로 나누기)
- AttributeError (속성 오류)
- ImportError (임포트 오류)
- ValueError (값 오류)

### 라이브러리 오류
- NumPy 오류
- Pandas 오류

## 📁 프로젝트 구조

```
sibd_pyerr/
├── core.py              # 핵심 에러 처리 로직
├── cli.py               # CLI 래퍼 스크립트
├── ipyext.py            # IPython 확장 모듈
├── install_profile.py   # 프로필 자동 설정
├── registry.py          # 에러 핸들러 등록
├── display/             # 출력 형식
│   ├── cli.py          # CLI 출력
│   └── jupyter.py      # 주피터 출력
└── handlers/            # 에러 핸들러
    ├── main/           # 기본 파이썬 에러
    ├── numpy/          # NumPy 에러
    └── pandas/         # Pandas 에러
```

## 🔄 버전 히스토리

### 0.1.3
- CLI 래퍼 (`sibd-py` 명령어) 추가
- IPython 확장 모듈 추가
- 자동 프로필 설정 기능 추가
- 문법 오류 검출 기능 추가

### 0.1.2
- type_error 관련 수정
- print 함수를 덮어썼습니다.

### 0.1.1
- 초기 버전

### 0.1.0
- 기본 에러 한글화 기능

## 📚 참고 자료

- [friendly-traceback](https://github.com/friendly-traceback/friendly-traceback)
- [소스코드 저장소](https://github.com/ehdcjf/pyerrkor.git)

## 🎓 개발 목적

이 패키지는 **선일빅데이터고등학교**의 교육용으로 개발되었습니다.
프로그래밍을 즐겨보세요! ^_^
