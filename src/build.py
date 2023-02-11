import subprocess
import os
def run_build():
    os.chdir("Run")
    subprocess.run(["cargo","build"])  ##THIS PROCESS OF MOVING DIRECTORIES MAY BECOME OBSOLETE WITH __INIT__.PY, UNSURE
    os.chdir("..")
    print("Build Complete.")

if __name__ == "__main__":
    run_build()