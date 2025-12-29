import subprocess

def read_until(stream, text):
    window = stream.read(len(text))
    while window != text:
        print(window)
        window = window[1:] + stream.read(1)

sclang = subprocess.Popen(["/usr/bin/sclang"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
ghci = subprocess.Popen(["/usr/bin/ghci"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

read_until(ghci.stdout, b"ghci>")
print(":script BootTidal.hs")
ghci.stdin.write(b":script BootTidal.hs\n")
ghci.stdin.flush()

read_until(ghci.stdout, b"tidal>")
print(":script main.hs")
ghci.stdin.write(b":script main.hs\n")
ghci.stdin.flush()

while True:
    pass

