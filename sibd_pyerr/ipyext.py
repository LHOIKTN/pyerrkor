"""
sibd_pyerr IPython 확장 모듈
주피터 노트북에서 자동으로 문법 검사와 에러 한글화를 활성화합니다.
"""

import ast
import sys
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import argument, magic_arguments
from IPython.utils.io import capture_output
from .core import install


@magics_class
class SibdPyerrMagics(Magics):
    """sibd_pyerr 매직 명령어 클래스"""
    
    def __init__(self, shell):
        super().__init__(shell)
        # 기본 에러 핸들러 설치
        install()
    
    @line_magic
    @magic_arguments()
    @argument('code', nargs='*', help='실행할 파이썬 코드')
    def sibd_py(self, line):
        """
        문법 검사 후 코드를 실행하는 매직 명령어
        
        사용법:
            %sibd_py print("Hello World")
            %%sibd_py
            x = 1
            print(x)
        """
        if not line.strip():
            return "사용법: %sibd_py <코드>"
        
        # 문법 검사
        try:
            ast.parse(line)
        except SyntaxError as e:
            from .registry import get_kor_error_info
            name, msg = get_kor_error_info(SyntaxError, e)
            from .display.jupyter import display_jupyter_error
            display_jupyter_error(name, msg)
            return
        
        # 문법이 올바르면 실행
        return self.shell.run_code(line)
    
    @line_magic
    def sibd_py_install(self, line):
        """sibd_pyerr 에러 핸들러를 설치합니다."""
        install()
        return "sibd_pyerr 에러 핸들러가 설치되었습니다."


def load_ipython_extension(ipython):
    """IPython 확장 로드 함수"""
    # 매직 명령어 등록
    ipython.register_magics(SibdPyerrMagics)
    
    # 기본 에러 핸들러 설치
    install()
    
    # 셀 실행 전 문법 검사 훅 등록
    def pre_run_cell(info):
        """셀 실행 전 문법 검사"""
        cell_source = info.raw_cell
        
        # 빈 셀이나 매직 명령어는 건너뛰기
        if not cell_source.strip() or cell_source.strip().startswith('%'):
            return
        
        try:
            ast.parse(cell_source)
        except SyntaxError as e:
            from .registry import get_kor_error_info
            name, msg = get_kor_error_info(SyntaxError, e)
            from .display.jupyter import display_jupyter_error
            display_jupyter_error(name, msg)
            # 셀 실행 중단
            raise e
    
    # 셀 실행 전 훅 등록
    ipython.events.register('pre_run_cell', pre_run_cell)
    
    print("✅ sibd_pyerr 확장이 로드되었습니다!")
    print("📝 사용 가능한 명령어:")
    print("   - %sibd_py <코드>: 문법 검사 후 코드 실행")
    print("   - %sibd_py_install: 에러 핸들러 재설치")


def unload_ipython_extension(ipython):
    """IPython 확장 언로드 함수"""
    # 매직 명령어 제거
    if hasattr(ipython, 'magics_manager'):
        ipython.magics_manager.registry.pop('sibd_py', None)
        ipython.magics_manager.registry.pop('sibd_py_install', None)
    
    print("sibd_pyerr 확장이 언로드되었습니다.") 