from sibd_pyerr.registry import register, format_error_location


@register("IndexError")
def _handle_index_error(exc_type, exc_value):
    kor_err_name = "인덱스 오류"
    msg = str(exc_value)
    
    # 기본 메시지 결정
    if "list" in msg:
        message = "리스트의 인덱스 범위를 벗어났습니다."
    elif "string" in msg:
        message = "문자열의 인덱스 범위를 벗어났습니다."
    elif "tuple" in msg:
        message = "튜플의 인덱스 범위를 벗어났습니다."
    else:
        message = "자료형의 인덱스 범위를 벗어났습니다."
    
    # 위치 정보 추가
    location = format_error_location(exc_value)
    if location:
        message += f"\n\n{location}"
    
    return kor_err_name, message
