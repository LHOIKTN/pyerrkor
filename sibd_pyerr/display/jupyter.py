def display_jupyter_error(name, message):
    try:
        from IPython.display import display, HTML
        display(HTML(f'<span style="color:red;">{name}</span>: {message}'))
    except ImportError:
        # IPython이 없는 경우 일반 print 사용
        print(f"{name}: {message}")
