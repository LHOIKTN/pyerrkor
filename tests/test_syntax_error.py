# 콜론 누락 에러 테스트
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 한글 에러 핸들러 설치
from sibd_pyerr.core import install
install()

# 콜론이 누락된 코드를 문자열로 실행
code_with_error = """
for i in range(10)  # 콜론(:) 누락
    print(i)
"""

try:
    exec(code_with_error)
except SyntaxError as e:
    print(f"에러 타입: {type(e).__name__}")
    print(f"에러 메시지: {e}")
    print(f"에러 라인: {e.lineno}")
    print(f"에러 위치: {e.offset}")
    if hasattr(e, 'text'):
        print(f"문제 코드: {e.text}")
