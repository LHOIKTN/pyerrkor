from sibd_pyerr.registry import register
import re


def format_syntax_location(exc_value):
    """SyntaxError의 위치 정보를 포맷팅합니다."""
    if not hasattr(exc_value, "text") or exc_value.text is None:
        return ""

    lines = exc_value.text.split('\n')
    lineno = exc_value.lineno
    offset = exc_value.offset

    # 파일명 정보 추가
    filename = getattr(exc_value, 'filename', '<unknown>')
    if filename == '<unknown>':
        filename = '현재 파일'
    elif '/' in filename:
        filename = filename.split('/')[-1]  # 파일명만 표시
    
    # 문제가 있는 줄만 표시
    if 1 <= lineno <= len(lines):
        problem_line = lines[lineno - 1]
        # 포인터 생성 (에러 위치 표시)
        pointer = " " * (offset - 1) + "^" if offset else ""
        
        return f"📍 파일: {filename}\n📍 줄 번호: {lineno}\n📍 문제의 줄:\n{problem_line}\n{pointer}"
    
    return f"📍 파일: {filename}\n📍 줄 번호: {lineno}"


@register("SyntaxError")
def syntax_error_handler(exc_type, exc_value):
    kor_err_name = "문법 오류"
    msg = str(exc_value)

    patterns = [
        (
            r"invalid syntax",
            "문법 오류",
            lambda m: "파이썬 문법에 맞지 않는 구문이 있습니다.\n괄호, 콜론, 들여쓰기 등을 다시 확인해보세요.",
        ),
        (
            r"unexpected EOF while parsing",
            "코드 미완성",
            lambda m: "코드가 끝났지만, 괄호나 따옴표가 닫히지 않았습니다.\n열린 괄호나 문자열이 닫혔는지 확인하세요.",
        ),
        (
            r"EOL while scanning string literal",
            "문자열 미완성",
            lambda m: "문자열이 닫히지 않았습니다.\n큰따옴표(\"\") 또는 작은따옴표('') 쌍이 맞는지 확인하세요.",
        ),
        (
            r"unexpected character after line continuation character",
            "줄바꿈 오류",
            lambda m: "역슬래시(\\) 다음에 올 수 없는 문자가 있습니다.\n줄을 나눌 때는 \\ 뒤에 공백 없이 이어 써야 합니다.",
        ),
        (
            r"cannot assign to expression",
            "잘못된 대입문",
            lambda m: "값을 저장할 수 없는 수식에 대입하려 했습니다.\n왼쪽에는 변수만 올 수 있습니다. (예: 3 + 2 = x ← ❌)",
        ),
        (
            r"f-string: unmatched",
            "f-string 괄호 오류",
            lambda m: "f-string 내부 표현식에서 괄호가 맞지 않습니다.",
        ),
        (
            r"f-string: expecting '}'",
            "f-string 중괄호 오류",
            lambda m: "f-string 내부 표현식이 중괄호로 닫히지 않았습니다.",
        ),
        (
            r"f-string: expressions nested too deeply",
            "f-string 중첩 오류",
            lambda m: "f-string 내부 표현식에 중첩된 괄호가 너무 많습니다.\n표현식을 간단히 하세요.",
        ),
    ]

    for pattern, summary, explain in patterns:
        if re.search(pattern, msg):
            location = format_syntax_location(exc_value)
            return kor_err_name, f"{explain(None)}\n\n{location}"

    # 패턴 매칭이 안 된 경우에도 위치 정보는 표시
    location = format_syntax_location(exc_value)
    if location:
        return kor_err_name, f"파이썬 문법에 맞지 않는 코드가 있습니다.\n구문을 다시 점검해보세요.\n\n{location}"
    
    return kor_err_name, "파이썬 문법에 맞지 않는 코드가 있습니다.\n구문을 다시 점검해보세요."

    return (
        kor_err_name,
        "파이썬 문법에 맞지 않는 코드가 있습니다.\n구문을 다시 점검해보세요.",
    )
