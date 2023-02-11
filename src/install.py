import subprocess
def run_install():
    subprocess.run(["pip","-q", "install", "--user", "PyGithub"])
    subprocess.run(["pip","-q", "install", "--user", "regex"])
    subprocess.run(["pip","-q", "install", "--user", "base64"])
    subprocess.run(["pip","-q","install", "--user", "ctypes"])
    subprocess.run(["pip","-q", "install", "--user", "requests"])
    subprocess.run(["pip","-q", "install", "--user", "ndjson"])
    subprocess.run(["pip","-q", "install", "--user", "gitpython"])
    # print("Install Complete.")  #to log file eventually

if __name__ == "__main__":
    run_install()