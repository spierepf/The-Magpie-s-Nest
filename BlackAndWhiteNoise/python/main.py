import os
import pathlib
import subprocess
import time
from icecream import ic


def read_until(stream, text):
    print("")
    window = stream.read(len(text))
    print(window.decode("utf-8"), end="")
    while window != text:
        window = window[1:] + stream.read(1)
        print(window.decode("utf-8")[-1], end="")


def write(text, stream):
    print(text)
    stream.write(text)
    stream.flush()

BOOT_TIDAL_HS = pathlib.Path(__file__).with_name("BootTidal.hs")
TIDAL_SOURCE = pathlib.Path(__file__).with_name("main.tidal")

def main():
    print("Hello from black-and-white-noise!")
    with subprocess.Popen(["/usr/bin/jackd", "-d", "alsa", "-d", "hw:Headset"]) as jackd:
        try:
            sclang_env = os.environ
            sclang_env["QT_QPA_PLATFORM"] = "offscreen"
            sclang = subprocess.Popen(["/usr/bin/sclang"], env=sclang_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            read_until(sclang.stdout, b"SuperDirt: listening on port 57120")

            ghci = subprocess.Popen(["/usr/bin/ghci"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            read_until(ghci.stdout, b"ghci>")
            write(f":script {BOOT_TIDAL_HS}\n".encode("utf-8"), ghci.stdin)
            # read_until(ghci.stdout, b"tidal>")

            last_modified_timestamp = None
            while jackd.poll() is None and sclang.poll() is None and ghci.poll() is None:
                current_modified_timestamp = os.path.getmtime(TIDAL_SOURCE)
                if current_modified_timestamp != last_modified_timestamp:
                    last_modified_timestamp = current_modified_timestamp
                    write(f":script {TIDAL_SOURCE}\n".encode("utf-8"), ghci.stdin)
                time.sleep(0.1)
        finally:
            if sclang.poll() is not None:
                ic(sclang.stdout.read().decode("utf-8"))
            if ghci.poll() is not None:
                ic(ghci.stdout.read().decode("utf-8"))
            jackd.terminate()


if __name__ == "__main__":
    main()
