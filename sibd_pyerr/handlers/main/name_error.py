import re
import traceback
from sibd_pyerr.registry import register, format_error_location


@register("NameError")
def handle_name_error(exc_type, exc_value):
    kor_err_name = "이름 오류"
    m = re.search(r"name '(.+?)' is not defined", str(exc_value))
    var = m.group(1) if m else ""
    
    # 기본 메시지
    message = f"정의되지 않은 변수 '{var}'를 사용했습니다."
    
    # 위치 정보 추가
    location = format_error_location(exc_value)
    if location:
        message += f"\n\n{location}"
    
    return kor_err_name, message
