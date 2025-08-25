# 런타임 에러 테스트 파일

# NameError 테스트
print(undefined_variable)

# TypeError 테스트
result = "Hello" + 123

# IndexError 테스트
numbers = [1, 2, 3]
print(numbers[10])

# KeyError 테스트
data = {"name": "John", "age": 30}
print(data["city"])

# ZeroDivisionError 테스트
result = 10 / 0

# AttributeError 테스트
text = "Hello"
text.append("World") 