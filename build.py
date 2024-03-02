#!/usr/bin/env python3

import subprocess
import sys


def build():
    print("Building files using pyinstaller")
    dist_path = "./project/bin"
    subprocess.run(f"pyinstaller --distpath {dist_path} src/main.py")


def main(argv: list[str]):
    build()


if __name__ == "__main__":
    main(sys.argv)
