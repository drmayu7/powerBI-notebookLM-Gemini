"""Generate the Lab 4 meeting audio from the committee transcript.

Reads 02-mesyuarat-jk-rekod-transcript.md, speaks each turn with a distinct
macOS voice per speaker, and writes 02-mesyuarat-jk-rekod-audio.m4a.

Run:
    uv run python module-2-notebooklm-gemini/examples/generate_audio.py
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import wave

HERE = Path(__file__).parent
TRANSCRIPT = HERE / "02-mesyuarat-jk-rekod-transcript.md"
OUT = HERE / "02-mesyuarat-jk-rekod-audio.m4a"

# Distinct built-in macOS voices per speaker (intelligible for Malay text).
SPEAKER_VOICES = {
    "Dr. Aisyah binti Rahman": "Samantha",
    "Encik Faizal bin Osman": "Daniel",
    "Puan Lim Mei Ling": "Karen",
    "Cik Nurul Huda binti Ismail": "Moira",
}
DEFAULT_VOICE = "Fred"

TURN_RE = re.compile(r"^\*\*(?P<speaker>[^:*]+):\*\*\s*(?P<text>.+)$")


def clean(text: str) -> str:
    """Strip Markdown markers so they are not read aloud."""
    # Remove bold/italic markers, headings, blockquotes, code ticks
    text = re.sub(r"[*_>#`]", "", text)
    return text.strip()


def synthesize_turn(voice: str, text: str, out_aiff: Path) -> None:
    """Invoke macOS say to synthesize one dialogue turn to an AIFF file."""
    subprocess.run(
        ["say", "-v", voice, "-o", str(out_aiff), text],
        check=True,
    )


def aiff_to_wav(aiff: Path, wav: Path) -> None:
    """Convert an AIFF-C file to a 16-bit LE WAV via afconvert."""
    subprocess.run(
        ["afconvert", str(aiff), str(wav), "-f", "WAVE", "-d", "LEI16"],
        check=True,
    )


def concatenate_wavs(wav_paths: list[Path], out_wav: Path) -> None:
    """Concatenate a list of WAV files (same format) into one WAV."""
    with wave.open(str(wav_paths[0]), "rb") as ref:
        params = ref.getparams()

    with wave.open(str(out_wav), "wb") as out:
        out.setparams(params)
        for wav_path in wav_paths:
            with wave.open(str(wav_path), "rb") as w:
                out.writeframes(w.readframes(w.getnframes()))


def wav_to_m4a(wav: Path, m4a: Path) -> None:
    """Convert a WAV file to AAC/m4a via afconvert."""
    subprocess.run(
        ["afconvert", str(wav), str(m4a), "-f", "m4af", "-d", "aac"],
        check=True,
    )


def main() -> None:
    if not shutil.which("say"):
        sys.exit("ERROR: macOS 'say' command not found. Run this script on macOS.")

    # Parse dialogue turns from the transcript.
    # Only include lines whose speaker is one of the four named participants
    # (skips header metadata like **Tarikh:**, **Pengerusi:** etc.).
    turns: list[tuple[str, str]] = []
    for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
        m = TURN_RE.match(line.strip())
        if m:
            speaker = m.group("speaker").strip()
            if speaker not in SPEAKER_VOICES:
                continue
            text = clean(m.group("text"))
            turns.append((speaker, text))

    if not turns:
        sys.exit("ERROR: no '**Speaker:** text' turns found in transcript.")

    print(f"Found {len(turns)} dialogue turns. Synthesizing...")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        wav_parts: list[Path] = []

        for i, (speaker, text) in enumerate(turns):
            voice = SPEAKER_VOICES.get(speaker, DEFAULT_VOICE)
            aiff = tmp_path / f"{i:03d}.aiff"
            wav = tmp_path / f"{i:03d}.wav"

            print(f"  [{i+1}/{len(turns)}] {speaker} ({voice}): {text[:60]}...")
            synthesize_turn(voice, text, aiff)
            aiff_to_wav(aiff, wav)
            wav_parts.append(wav)

        # Concatenate all WAV parts using Python's wave module (no external deps).
        combined_wav = tmp_path / "combined.wav"
        concatenate_wavs(wav_parts, combined_wav)

        # Convert to AAC/m4a.
        wav_to_m4a(combined_wav, OUT)

    print(f"Wrote {OUT.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()
