"""
╔══════════════════════════════════════╗
║      Video to MP4 Converter          ║
║  Suporta: MOV, AVI, WEBM, MKV, etc  ║
╚══════════════════════════════════════╝

Dependências:
    pip install ffmpeg-python tqdm colorama

Uso:
    # Converter um arquivo:
    python video_converter.py video.mov

    # Converter vários arquivos:
    python video_converter.py video1.avi video2.webm

    # Converter todos os vídeos de uma pasta:
    python video_converter.py --pasta ./meus_videos

    # Escolher pasta de saída:
    python video_converter.py video.mov --saida ./convertidos
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

# ─── Formatos suportados ────────────────────────────────────────────────────
FORMATOS_SUPORTADOS = {
    ".mov", ".avi", ".webm", ".mkv", ".flv", ".wmv",
    ".m4v", ".3gp", ".ts", ".mts", ".m2ts", ".vob",
    ".ogv", ".rm", ".rmvb", ".divx", ".f4v", ".asf"
}

# ─── Cores no terminal ──────────────────────────────────────────────────────
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    VERDE   = Fore.GREEN
    AMARELO = Fore.YELLOW
    VERMELHO= Fore.RED
    CIANO   = Fore.CYAN
    RESET   = Style.RESET_ALL
    NEGRITO = Style.BRIGHT
except ImportError:
    VERDE = AMARELO = VERMELHO = CIANO = RESET = NEGRITO = ""


def verificar_ffmpeg():
    """Verifica se o ffmpeg está instalado no sistema."""
    if shutil.which("ffmpeg") is None:
        print(f"{VERMELHO}✗ ffmpeg não encontrado!{RESET}")
        print(f"{AMARELO}  Instale em: https://ffmpeg.org/download.html{RESET}")
        print(f"{AMARELO}  Windows: winget install ffmpeg{RESET}")
        print(f"{AMARELO}  macOS:   brew install ffmpeg{RESET}")
        print(f"{AMARELO}  Linux:   sudo apt install ffmpeg{RESET}")
        sys.exit(1)


def obter_duracao(arquivo: Path) -> float:
    """Retorna a duração do vídeo em segundos."""
    try:
        resultado = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(arquivo)
            ],
            capture_output=True, text=True
        )
        return float(resultado.stdout.strip())
    except Exception:
        return 0.0


def converter_video(entrada: Path, saida: Path) -> bool:
    """
    Converte um vídeo para MP4 usando ffmpeg.
    Retorna True se bem-sucedido, False se falhou.
    """
    saida.parent.mkdir(parents=True, exist_ok=True)

    duracao = obter_duracao(entrada)
    nome_arquivo = entrada.name

    print(f"\n{CIANO}┌─ Convertendo:{RESET} {nome_arquivo}")
    if duracao > 0:
        mins = int(duracao // 60)
        segs = int(duracao % 60)
        print(f"{CIANO}│  Duração:{RESET} {mins:02d}:{segs:02d}")
    print(f"{CIANO}│  Saída:{RESET}   {saida.name}")
    print(f"{CIANO}└─ Progresso:{RESET}", end=" ", flush=True)

    cmd = [
        "ffmpeg",
        "-i", str(entrada),
        "-c:v", "libx264",        # codec de vídeo H.264
        "-preset", "fast",         # velocidade de codificação
        "-crf", "22",              # qualidade (0=perfeita, 51=ruim; 18-28 é bom)
        "-c:a", "aac",             # codec de áudio AAC
        "-b:a", "192k",            # bitrate do áudio
        "-movflags", "+faststart", # otimizado para streaming
        "-y",                      # sobrescrever se existir
        str(saida)
    ]

    processo = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Mostrar progresso simples
    barras = 0
    for linha in processo.stderr:
        if "time=" in linha and duracao > 0:
            try:
                parte_tempo = linha.split("time=")[1].split(" ")[0]
                h, m, s = parte_tempo.split(":")
                atual = int(h)*3600 + int(m)*60 + float(s)
                porcentagem = min(int((atual / duracao) * 20), 20)
                while barras < porcentagem:
                    print("█", end="", flush=True)
                    barras += 1
            except Exception:
                pass

    processo.wait()

    # Completar a barra
    while barras < 20:
        print("█", end="", flush=True)
        barras += 1

    if processo.returncode == 0:
        tamanho_mb = saida.stat().st_size / (1024 * 1024)
        print(f" {VERDE}✓ {tamanho_mb:.1f} MB{RESET}")
        return True
    else:
        print(f" {VERMELHO}✗ Falhou{RESET}")
        if saida.exists():
            saida.unlink()
        return False


def coletar_arquivos(caminhos: list, pasta: str | None) -> list[Path]:
    """Coleta todos os arquivos de vídeo para converter."""
    arquivos = []

    # Arquivos passados diretamente
    for caminho in caminhos:
        p = Path(caminho)
        if p.is_file():
            if p.suffix.lower() in FORMATOS_SUPORTADOS:
                arquivos.append(p)
            else:
                print(f"{AMARELO}⚠ Ignorado (formato não suportado): {p.name}{RESET}")
        else:
            print(f"{VERMELHO}✗ Arquivo não encontrado: {caminho}{RESET}")

    # Varrer pasta
    if pasta:
        p = Path(pasta)
        if p.is_dir():
            encontrados = [
                f for f in p.iterdir()
                if f.is_file() and f.suffix.lower() in FORMATOS_SUPORTADOS
            ]
            if encontrados:
                arquivos.extend(sorted(encontrados))
            else:
                print(f"{AMARELO}⚠ Nenhum vídeo encontrado em: {pasta}{RESET}")
        else:
            print(f"{VERMELHO}✗ Pasta não encontrada: {pasta}{RESET}")

    return arquivos


def main():
    parser = argparse.ArgumentParser(
        description="Converte vídeos para MP4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python video_converter.py video.mov
  python video_converter.py clip1.avi clip2.webm
  python video_converter.py --pasta ./videos
  python video_converter.py video.mkv --saida ./saida
  python video_converter.py --pasta ./videos --saida ./mp4s
        """
    )
    parser.add_argument("arquivos", nargs="*", help="Arquivos de vídeo para converter")
    parser.add_argument("--pasta",  "-p", help="Pasta com vídeos para converter")
    parser.add_argument("--saida",  "-o", help="Pasta de saída (padrão: mesma do vídeo)")
    parser.add_argument("--qualidade", "-q", type=int, default=22,
                        help="Qualidade CRF: 18=alta, 22=padrão, 28=menor arquivo (padrão: 22)")

    args = parser.parse_args()

    if not args.arquivos and not args.pasta:
        parser.print_help()
        sys.exit(0)

    # ── Cabeçalho ────────────────────────────────────────────────────────────
    print(f"\n{NEGRITO}{CIANO}{'═'*45}")
    print("      🎬  Video to MP4 Converter")
    print(f"{'═'*45}{RESET}")

    # ── Verificar ffmpeg ──────────────────────────────────────────────────────
    verificar_ffmpeg()

    # ── Coletar arquivos ──────────────────────────────────────────────────────
    arquivos = coletar_arquivos(args.arquivos, args.pasta)

    if not arquivos:
        print(f"\n{VERMELHO}Nenhum arquivo para converter.{RESET}")
        sys.exit(1)

    formatos_lista = ", ".join(sorted(FORMATOS_SUPORTADOS))
    print(f"\n{NEGRITO}Formatos suportados:{RESET} {formatos_lista}")
    print(f"{NEGRITO}Arquivos encontrados:{RESET} {len(arquivos)}")
    print(f"{NEGRITO}Qualidade CRF:{RESET}      {args.qualidade} (18=alta · 22=padrão · 28=compacto)")

    # ── Converter ─────────────────────────────────────────────────────────────
    sucesso = 0
    falhou  = 0

    for i, arquivo in enumerate(arquivos, 1):
        print(f"\n{AMARELO}[{i}/{len(arquivos)}]{RESET}", end="")

        # Definir caminho de saída
        if args.saida:
            pasta_saida = Path(args.saida)
        else:
            pasta_saida = arquivo.parent

        saida = pasta_saida / (arquivo.stem + ".mp4")

        # Não converter se já for MP4 com mesmo nome
        if arquivo.suffix.lower() == ".mp4" and arquivo == saida:
            print(f" {AMARELO}⚠ Já é MP4, pulando: {arquivo.name}{RESET}")
            continue

        if converter_video(arquivo, saida):
            sucesso += 1
        else:
            falhou += 1

    # ── Resumo ────────────────────────────────────────────────────────────────
    print(f"\n{NEGRITO}{CIANO}{'─'*45}{RESET}")
    print(f"{NEGRITO}Concluído!{RESET}  "
          f"{VERDE}✓ {sucesso} convertido(s){RESET}"
          + (f"  {VERMELHO}✗ {falhou} falhou(ram){RESET}" if falhou else ""))
    print()


if __name__ == "__main__":
    main()