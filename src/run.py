import url
import build
import install
import sys

if __name__ == "__main__":
    if(sys.argv[1] == "build"):
        sys.exit(build.run_build()) # Should exit 0 on success
    elif(sys.argv[1] == "install"):
        sys.exit(install.run_install()) # Should exit 0 on success
    else:
        sys.exit(url.parser_driver()) # Should exit 0 on success // Subject to Change