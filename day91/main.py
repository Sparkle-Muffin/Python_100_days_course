# Example use
# Default (Polish voice):
# python day91/main.py day91/input/test_file.txt
# With voice specified:
# python day91/main.py day91/input/test_file.txt --voice en_US-ryan-high

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import textract
from PyPDF2 import PdfReader
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

SUPPORTED_EXTENSIONS = {".txt", ".doc", ".docx", ".odt", ".pdf"}


def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_docx(path: Path) -> str:
    """
    Read text from a .docx file without third-party packages.
    A .docx file is a ZIP archive containing XML documents.
    """
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as document_xml:
            xml_data = document_xml.read()

    root = ET.fromstring(xml_data)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    text_nodes = root.findall(".//w:t", namespace)
    return "\n".join(node.text for node in text_nodes if node.text)


def read_odt(path: Path) -> str:
    """
    Read text from a .odt file without third-party packages.
    An .odt file is a ZIP archive with text in content.xml.
    """
    with zipfile.ZipFile(path) as zf:
        with zf.open("content.xml") as content_xml:
            xml_data = content_xml.read()

    root = ET.fromstring(xml_data)
    namespace = {"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
    text_nodes = root.findall(".//text:p", namespace)
    return "\n".join("".join(node.itertext()).strip() for node in text_nodes if "".join(node.itertext()).strip())


def read_doc(path: Path) -> str:
    # For .doc support install: pip install textract

    return textract.process(str(path)).decode("utf-8", errors="replace")


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def read_file_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension: {suffix}. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    if suffix == ".txt":
        return read_txt(path)
    if suffix == ".doc":
        return read_doc(path)
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".odt":
        return read_odt(path)
    return read_pdf(path)


def send_text_to_tts_server(text: str, server_url: str, voice: str | None = None) -> bytes:
    request_data = {"text": text}
    if voice:
        request_data["voice"] = voice

    payload = json.dumps(request_data, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url=server_url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.read()
    except urllib.error.HTTPError as err:
        details = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Server returned HTTP {err.code}: {details}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Cannot connect to TTS server: {err.reason}") from err


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read text from .txt/.doc/.docx/.odt/.pdf, send it to TTS server, "
            "and save returned audio file."
        )
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to input file (.txt, .doc, .docx, .odt, .pdf).",
    )
    parser.add_argument(
        "--server-url",
        default="http://localhost:5000",
        help="TTS server URL (default: http://localhost:5000).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory for saved .wav file (default: output).",
    )
    parser.add_argument(
        "--voice",
        default=None,
        help="Optional voice name/id to send to TTS server.",
    )
    args = parser.parse_args()

    input_path = args.input_file
    if not input_path.exists() or not input_path.is_file():
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        return 1

    try:
        text = read_file_text(input_path)
    except Exception as err:
        print(f"Failed to read input file: {err}", file=sys.stderr)
        return 1

    if not text.strip():
        print("Input text is empty. Nothing to synthesize.", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / f"{input_path.stem}.wav"

    try:
        audio_bytes = send_text_to_tts_server(text, args.server_url, args.voice)
    except Exception as err:
        print(f"Failed to synthesize speech: {err}", file=sys.stderr)
        return 1

    output_path.write_bytes(audio_bytes)
    print(f"Saved audio to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
