import subprocess
import os

def git_pull(repo_path):
    try:
        subprocess.check_call(['git', '-C', repo_path, 'pull'])
        print(f"✅ Git pull thành công tại: {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi git pull: {e}")
    except Exception as e:
        print(f"❌ Lỗi khác: {e}")

if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.abspath(__file__))
    git_pull(repo_path)
