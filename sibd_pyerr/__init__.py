from .core import install
from .registry import get_kor_error_info

__all__ = [
    "install", 
    "get_kor_error_info",
    "setup_profile"
]

def setup_profile():
    """IPython 프로필에 sibd_pyerr 확장을 자동으로 설정합니다."""
    from .install_profile import main
    main()
