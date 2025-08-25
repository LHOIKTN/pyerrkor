#!/usr/bin/env python3
"""
sibd-py CLI 래퍼 스크립트
파이썬 파일을 실행하기 전에 문법 검사를 수행합니다.
"""

import sys
import ast
import os
import subprocess
from pathlib import Path


def check_syntax(file_path):
    """파일의 문법을 검사합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        # 파일 내용을 SyntaxError 객체에 추가
        e.text = source
        e.filename = file_path
        return False, e
    except Exception as e:
        return False, e


def run_with_sibd_pyerr(file_path):
    """sibd_pyerr와 함께 파이썬 파일을 실행합니다."""
    # 문법 검사
    is_valid, error = check_syntax(file_path)
    
    if not is_valid:
        if isinstance(error, SyntaxError):
            # sibd_pyerr를 사용하여 한글화된 에러 메시지 출력
            try:
                from sibd_pyerr.registry import get_kor_error_info
                from sibd_pyerr.display.cli import print_cli_error
                
                name, msg = get_kor_error_info(SyntaxError, error)
                print_cli_error(name, msg)
            except ImportError:
                # sibd_pyerr가 설치되지 않은 경우 기본 에러 출력
                print(f"SyntaxError: {error}")
        else:
            print(f"파일 읽기 오류: {error}")
        return 1
    
            # 문법이 올바르면 파이썬으로 실행 (sibd_pyerr 기능 통합)
        try:
            # 파일 내용을 읽어서 직접 실행
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # sibd_pyerr와 함께 파이썬 파일 실행
            import subprocess
            import os
            
            # sibd_pyerr를 import하는 코드를 추가한 임시 스크립트 생성
            temp_script = f"""
import sys
import sibd_pyerr
sibd_pyerr.install()

# 원본 파일 실행
exec(open('{file_path}', 'r', encoding='utf-8').read())
"""
            
            # 임시 스크립트를 파일로 저장
            temp_file = f"{file_path}.temp.py"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(temp_script)
            
            try:
                # 임시 스크립트 실행
                result = subprocess.run([sys.executable, temp_file], 
                                      capture_output=False, 
                                      text=True)
                return result.returncode
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return 1
        except Exception as e:
            # sibd_pyerr가 이미 설치되어 있으므로 에러가 한글로 표시됨
            return 1


def main():
    """메인 함수"""
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print("sibd-py - 파이썬 에러 한글화 CLI 래퍼")
        print("")
        print("사용법: sibd-py <파이썬_파일> [인수...]")
        print("예시: sibd-py hello.py")
        print("")
        print("기능:")
        print("  - 파이썬 파일 실행 전 문법 검사")
        print("  - 문법 오류를 한글로 표시")
        print("  - 런타임 오류를 한글로 표시")
        print("")
        print("옵션:")
        print("  -h, --help    이 도움말을 표시")
        if len(sys.argv) < 2:
            sys.exit(1)
        else:
            sys.exit(0)
    
    file_path = sys.argv[1]
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"오류: 파일 '{file_path}'을 찾을 수 없습니다.")
        sys.exit(1)
    
    # 파일 확장자 확인
    if not file_path.endswith('.py'):
        print(f"경고: '{file_path}'는 파이썬 파일이 아닙니다.")
    
    # 실행
    exit_code = run_with_sibd_pyerr(file_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 