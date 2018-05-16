import subprocess

def get():
    try:
        return (subprocess.check_output(['git', 'rev-parse', 'HEAD'])).decode("utf-8").rstrip()
    except:
        return "Error: git probably not installed"
