"""Prepare uma instalação local sem sobrescrever configurações existentes."""
import argparse
import re
import secrets
import shutil
import subprocess
import sys
import venv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configure-only", action="store_true", help="Cria somente .env, útil para Docker")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    if not env_path.exists():
        config = (root / ".env.example").read_text(encoding="utf-8")
        config = re.sub(r"(?m)^API_KEY=.*$", "API_KEY=" + secrets.token_urlsafe(32), config)
        with env_path.open("x", encoding="utf-8", newline="\n") as env_file:
            env_file.write(config)
        if sys.platform != "win32":
            env_path.chmod(0o600)
        print(".env criado com chave aleatória. Consulte o arquivo para configurar seu cliente.")
    else:
        print(".env existente preservado.")
    if args.configure_only:
        return
    if not (3, 10) <= sys.version_info[:2] <= (3, 13):
        raise SystemExit("Use Python 3.10 a 3.13 (recomendado: 3.12).")
    target = root / ".venv"
    interpreter = target / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if not interpreter.exists():
        venv.EnvBuilder(with_pip=True).create(target)
    subprocess.run([str(interpreter), "-m", "pip", "install", "-r", str(root / "requirements.txt")], check=True)
    if not shutil.which("ffmpeg"):
        print("AVISO: FFmpeg ausente. MP3 funciona; instale FFmpeg para os demais formatos.")
    print("Instalação concluída. Execute na pasta do projeto:")
    print(f'"{interpreter}" main.py')
    print("PowerShell: use & antes do caminho entre aspas.")


if __name__ == "__main__":
    main()
