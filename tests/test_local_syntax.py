# 로컬 개발 중인 코드로 syntax error 테스트
import sys
import os

# 현재 프로젝트 루트를 Python 경로에 추가 (로컬 개발 코드)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 로컬 개발 중인 모듈 직접 import
from sibd_pyerr.core import install, check_syntax_error
from sibd_pyerr.registry import get_kor_error_info

# 한글 에러 핸들러 설치
install()

print("=== 로컬 개발 코드로 Syntax Error 테스트 ===")

# 테스트할 코드들
test_codes = [
    {
        "name": "콜론 누락",
        "code": """
for i in range(10)  # 콜론(:) 누락
    print(i)
""",
    },
    {
        "name": "괄호 미완성",
        "code": """
if True  # 콜론 누락
    print("Hello"
""",
    },
    {
        "name": "정상 코드",
        "code": """
for i in range(10):
    print(i)
""",
    },
]

# 각 테스트 코드 실행
for test in test_codes:
    print(f"\n--- {test['name']} ---")
    print(f"코드:\n{test['code']}")

    syntax_error = check_syntax_error(test["code"])
    if syntax_error:
        print(f"발견된 문법 오류: {syntax_error}")
        name, msg = get_kor_error_info(SyntaxError, syntax_error)
        print(f"한글화된 에러:")
        print(f"에러 이름: {name}")
        print(f"에러 설명: {msg}")
    else:
        print("✅ 문법 오류가 없습니다.")
