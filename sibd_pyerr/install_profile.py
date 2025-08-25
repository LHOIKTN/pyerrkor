"""
IPython 프로필 자동 설정 스크립트
sibd_pyerr 확장을 IPython 디폴트 프로필에 자동으로 등록합니다.
"""

import os
import sys
from pathlib import Path


def get_ipython_profile_dir():
    """IPython 프로필 디렉토리를 반환합니다."""
    home = Path.home()
    
    # IPython 프로필 디렉토리 찾기
    profile_dirs = [
        home / ".ipython" / "profile_default",
        home / ".jupyter" / "profile_default",
        home / ".config" / "ipython" / "profile_default"
    ]
    
    for profile_dir in profile_dirs:
        if profile_dir.exists():
            return profile_dir
    
    # 기본 디렉토리 생성
    default_profile = home / ".ipython" / "profile_default"
    default_profile.mkdir(parents=True, exist_ok=True)
    return default_profile


def create_startup_script(profile_dir):
    """시작 스크립트를 생성합니다."""
    startup_dir = profile_dir / "startup"
    startup_dir.mkdir(exist_ok=True)
    
    script_path = startup_dir / "00-sibd-pyerr.py"
    
    script_content = '''"""
sibd_pyerr 자동 로드 스크립트
IPython/Jupyter 시작 시 자동으로 sibd_pyerr 확장을 로드합니다.
"""

try:
    # IPython이 실행 중인지 확인
    ip = get_ipython()
    if ip is not None:
        # sibd_pyerr 확장 로드
        ip.run_line_magic("load_ext", "sibd_pyerr.ipyext")
        print("✅ sibd_pyerr 확장이 자동으로 로드되었습니다!")
    else:
        print("⚠️  IPython 환경이 아닙니다. sibd_pyerr 확장을 수동으로 로드하세요.")
except ImportError as e:
    print(f"❌ sibd_pyerr 패키지를 찾을 수 없습니다: {e}")
    print("   pip install sibd_pyerr로 설치하세요.")
except Exception as e:
    print(f"❌ sibd_pyerr 확장 로드 실패: {e}")
'''
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_path


def install_cli_script():
    """CLI 스크립트를 PATH에 설치합니다."""
    try:
        import sibd_pyerr
        package_dir = Path(sibd_pyerr.__file__).parent
        cli_script = package_dir / "cli.py"
        
        if not cli_script.exists():
            print("❌ CLI 스크립트를 찾을 수 없습니다.")
            return False
        
        # 실행 권한 부여
        cli_script.chmod(0o755)
        
        # symlink 생성 (선택사항)
        try:
            import site
            bin_dir = Path(site.USER_BASE) / "bin"
            bin_dir.mkdir(exist_ok=True)
            
            symlink_path = bin_dir / "sibd-py"
            if symlink_path.exists():
                symlink_path.unlink()
            
            symlink_path.symlink_to(cli_script)
            print(f"✅ CLI 스크립트가 {symlink_path}에 설치되었습니다.")
            print(f"   사용법: sibd-py <파이썬_파일>")
            return True
        except Exception as e:
            print(f"⚠️  CLI 스크립트 symlink 생성 실패: {e}")
            print(f"   수동으로 실행: python -m sibd_pyerr.cli <파이썬_파일>")
            return False
            
    except ImportError:
        print("❌ sibd_pyerr 패키지를 찾을 수 없습니다.")
        return False


def main():
    """메인 설치 함수"""
    print("🚀 sibd_pyerr IPython 프로필 설정을 시작합니다...")
    
    # IPython 프로필 디렉토리 찾기/생성
    profile_dir = get_ipython_profile_dir()
    print(f"📁 IPython 프로필 디렉토리: {profile_dir}")
    
    # 시작 스크립트 생성
    script_path = create_startup_script(profile_dir)
    print(f"✅ 시작 스크립트 생성: {script_path}")
    
    # CLI 스크립트 설치
    cli_success = install_cli_script()
    
    print("\n🎉 설치가 완료되었습니다!")
    print("\n📋 다음에 Jupyter/IPython을 시작하면:")
    print("   - 자동으로 sibd_pyerr 확장이 로드됩니다")
    print("   - 문법 오류가 한글로 표시됩니다")
    print("   - 런타임 오류도 한글로 표시됩니다")
    
    if cli_success:
        print("\n💻 CLI 사용법:")
        print("   sibd-py <파이썬_파일>")
    
    print("\n🔧 수동 설정이 필요한 경우:")
    print("   %load_ext sibd_pyerr.ipyext")
    
    print("\n📚 사용 가능한 명령어:")
    print("   - %sibd_py <코드>: 문법 검사 후 코드 실행")
    print("   - %sibd_py_install: 에러 핸들러 재설치")


if __name__ == "__main__":
    main() 