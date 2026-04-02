# 🎬 VideoConverter

> Converta vídeos para MP4 em segundos, direto do terminal.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-007808?style=flat-square&logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

---

## ✨ O que faz

Script Python simples e rápido que converte vídeos de qualquer formato popular para **MP4 (H.264 + AAC)** — o formato mais compatível com celulares, TVs, redes sociais e players de vídeo.

```
Exploration.mov  ──►  Exploration.mp4  ✓ 45.2 MB
```

---

## 📦 Formatos suportados

| Categoria | Extensões |
|-----------|-----------|
| Apple / iOS | `.mov`, `.m4v` |
| Windows | `.avi`, `.wmv`, `.asf` |
| Web | `.webm`, `.flv`, `.f4v` |
| Universal | `.mkv` |
| Mobile | `.3gp` |
| Broadcast | `.ts`, `.mts`, `.m2ts`, `.vob` |
| Outros | `.ogv`, `.rm`, `.rmvb`, `.divx` |

---

## ⚙️ Pré-requisitos

### 1. FFmpeg

| Sistema | Comando |
|---------|---------|
| **Windows** | `winget install Gyan.FFmpeg` |
| **macOS** | `brew install ffmpeg` |
| **Linux** | `sudo apt install ffmpeg` |

> Após instalar no Windows, **reinicie o VSCode** para o PATH atualizar.

### 2. Python 3.8+

```bash
pip install colorama
```

---

## 🚀 Como usar

```bash
# Converter um arquivo
python main.py video.mov

# Converter vários arquivos de uma vez
python main.py clip1.avi clip2.webm clip3.mkv

# Converter todos os vídeos de uma pasta
python main.py --pasta ./meus_videos

# Definir pasta de saída
python main.py video.mov --saida ./convertidos

# Pasta inteira com saída personalizada
python main.py --pasta ./originais --saida ./mp4s

# Ajustar qualidade
python main.py video.avi --qualidade 18
```

---

## 🎛️ Opções

| Flag | Atalho | Descrição | Padrão |
|------|--------|-----------|--------|
| `--pasta` | `-p` | Pasta com vídeos para converter | — |
| `--saida` | `-o` | Pasta onde salvar os MP4s | Mesma do vídeo |
| `--qualidade` | `-q` | Qualidade CRF (18=alta · 22=padrão · 28=compacto) | `22` |

---

## 📊 Qualidade vs Tamanho

| CRF | Qualidade | Uso indicado |
|-----|-----------|--------------|
| `18` | Alta | Arquivamento, edição |
| `22` | Padrão ✓ | Uso geral |
| `28` | Compacta | Compartilhamento rápido |

---

## 💡 Detalhes técnicos

- **Codec de vídeo:** H.264 (`libx264`) com preset `fast`
- **Codec de áudio:** AAC a 192kbps
- **Otimização:** `faststart` para streaming
- O arquivo original **nunca é apagado**
- Barra de progresso em tempo real no terminal

---

## 📁 Estrutura do projeto

```
VideoConverter/
├── main.py        # Script principal
├── README.md      # Este arquivo
└── .venv/         # Ambiente virtual Python
```

---

## 📄 Licença

MIT — fique à vontade para usar, modificar e distribuir.
