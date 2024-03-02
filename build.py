#!/usr/bin/env python3

import platform
import subprocess
import sys


def build_windows(release: bool):
    print(f"INFO: Building using MSVC in {'release' if release else 'debug'} mode.")

    subprocess.run(
        "cmake -B project/build -DCMAKE_INSTALL_PREFIX=project/bin", shell=True
    )

    if release:
        subprocess.run(
            "cmake --build project/build --parallel --config Release", shell=True
        )
        subprocess.run("cmake --install project/build", shell=True)
    else:
        subprocess.run(
            "cmake --build project/build --parallel --config Debug", shell=True
        )
        subprocess.run("cmake --install project/build --config Debug", shell=True)


def build(release: bool):
    print(f"INFO: Building in {'release' if release else 'debug'} mode.")

    if release:
        subprocess.run(
            "cmake -B project/build -DCMAKE_INSTALL_PREFIX=project/bin -DCMAKE_BUILD_TYPE=Release",
            shell=True,
        )
    else:
        subprocess.run(
            "cmake -B project/build -DCMAKE_INSTALL_PREFIX=project/bin -DCMAKE_BUILD_TYPE=Debug",
            shell=True,
        )

    subprocess.run("cmake --build project/build --parallel", shell=True)
    subprocess.run("cmake --install project/build", shell=True)


def main(argv: list[str]):
    argc = len(argv)
    release = False
    if argc == 2 and argv[1] == "release":
        release = True

    if platform.system() == "Windows":
        build_windows(release)
    else:
        build(release)


if __name__ == "__main__":
    main(sys.argv)
