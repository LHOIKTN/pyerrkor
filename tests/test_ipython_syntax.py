# IPython 환경에서 syntax error 테스트
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 한글 에러 핸들러 설치
from sibd_pyerr.core import install, check_syntax_error

install()

# 문법 검사 테스트
code_with_error = """
for i in range(10)  # 콜론(:) 누락
    print(i)
"""

print("문법 검사 테스트:")
syntax_error = check_syntax_error(code_with_error)
if syntax_error:
    print(f"발견된 문법 오류: {syntax_error}")
    print(f"에러 메시지: {syntax_error.msg}")
    print(f"에러 라인: {syntax_error.lineno}")
    print(f"에러 위치: {syntax_error.offset}")

    # 한글화된 에러 메시지 출력
    from sibd_pyerr.registry import get_kor_error_info

    name, msg = get_kor_error_info(SyntaxError, syntax_error)
    print(f"\n한글화된 에러:")
    print(f"에러 이름: {name}")
    print(f"에러 설명: {msg}")
else:
    print("문법 오류가 없습니다.")
