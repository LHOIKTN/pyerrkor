import sys
import ast
from .registry import get_kor_error_info
from .display.cli import print_cli_error
from .display.jupyter import display_jupyter_error
from .handlers import *  # 모든 핸들러 등록


def custom_handler(exc_type, exc_value, exc_traceback):
    name, msg = get_kor_error_info(exc_type, exc_value)
    print_cli_error(name, msg)
    # 기본 에러 메시지는 출력하지 않음 (중복 방지)
    # import traceback
    # traceback.print_exception(exc_type, exc_value, exc_traceback)


def check_syntax_error(code):
    """코드의 문법 오류를 미리 검사합니다."""
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return e


def ipython_handler(shell, exc_type, exc_value, exc_traceback, tb_offset=None):
    name, msg = get_kor_error_info(exc_type, exc_value)
    display_jupyter_error(name, msg)
    # 기본 에러 메시지는 출력하지 않음 (중복 방지)
    # shell.showtraceback((exc_type, exc_value, exc_traceback), tb_offset=tb_offset)


def pre_run_cell_hook(info):
    """IPython에서 셀 실행 전에 문법 검사를 수행합니다."""
    code = info.raw_cell
    syntax_error = check_syntax_error(code)
    if syntax_error:
        name, msg = get_kor_error_info(SyntaxError, syntax_error)
        display_jupyter_error(name, msg)
        return False  # 셀 실행을 중단
    return True


def install():
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell:
            shell.set_custom_exc((Exception,), ipython_handler)
            # pre_run_cell_hook 등록
            shell.events.register("pre_run_cell", pre_run_cell_hook)
            return
    except ImportError:
        pass
    sys.excepthook = custom_handler
    print(
        "This package was developed for educational use at SUNIL BIGDATA HIGH SCHOOL.\n Enjoy Programming^_^"
    )
