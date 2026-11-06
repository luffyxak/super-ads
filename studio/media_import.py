"""Allowlisted, size-bounded local media ingestion."""

import base64
import binascii
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from .contracts import ASSET_ROLES, ContractError, fields, require, safe_name, string

MAX_MEDIA = 16 * 1024 * 1024
IMAGE = {".png": {"png"}, ".jpg": {"mjpeg"}, ".jpeg": {"mjpeg"}, ".webp": {"webp"}}
VIDEO = {".mp4": {"h264"}}
AUDIO = {".wav": {"pcm_s16le", "pcm_s24le", "pcm_f32le"}, ".mp3": {"mp3"}, ".m4a": {"aac"}}


def safe_path(root, *parts):
    root = Path(root)
    candidate = root.joinpath(*parts)
    if not candidate.resolve().is_relative_to(root.resolve()) or root.is_symlink():
        raise ContractError("Unsafe storage path.")
    current = root
    for part in candidate.relative_to(root).parts:
        current /= part
        require(not current.is_symlink(), "Symlinks are not allowed in studio storage.")
    return candidate


def sha_file(path):
    require(path.is_file() and not path.is_symlink(), "Expected a regular file.")
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def probe(path, ext, kind):
    try:
        info = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-protocol_whitelist",
                "file",
                "-max_alloc",
                "134217728",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ],
            timeout=12,
            check=True,
            capture_output=True,
        )
        data = json.loads(info.stdout)
        streams = data["streams"]
        require(1 <= len(streams) <= (2 if kind == "clip" else 1), "Unsupported media stream count.")
        table = AUDIO if kind in {"voice", "music", "foley"} else VIDEO if kind == "clip" else IMAGE
        stream = streams[0]
        require(stream["codec_name"] in table[ext], "Media bytes do not match the allowed codec.")
        if table is not AUDIO:
            require(
                1 <= stream["width"] <= 4096 and 1 <= stream["height"] <= 4096, "Unsupported picture size."
            )
        if table is VIDEO:
            require(
                all(s.get("codec_type") == "audio" and s.get("codec_name") == "aac" for s in streams[1:]),
                "Only AAC audio is supported in imported clips.",
            )
            require("mp4" in data["format"]["format_name"].split(","), "Import a real MP4 container.")
        duration = 0 if table is IMAGE else round(float(data["format"]["duration"]) * 1000)
        require(table is IMAGE or 100 <= duration <= 60000, "Media must be 0.1–60 seconds.")
        subprocess.run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-xerror",
                "-protocol_whitelist",
                "file",
                "-max_alloc",
                "134217728",
                "-threads",
                "2",
                "-i",
                str(path),
                "-f",
                "null",
                "-",
            ],
            timeout=30,
            check=True,
            capture_output=True,
        )
        return duration
    except (OSError, ValueError, KeyError, OverflowError, subprocess.SubprocessError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError("The media could not be safely decoded.") from None


def ingest(value, asset_dir):
    fields(value, ("name", "role", "rights", "source", "disclosure", "consent", "data"), "Asset")
    name = safe_name(value.get("name"))
    role = value.get("role")
    require(isinstance(role, str) and role in ASSET_ROLES, "Choose an allowed asset role.")
    ext = Path(name).suffix.lower()
    allowed = AUDIO if role in {"voice", "music", "foley"} else VIDEO if role == "clip" else IMAGE
    require(ext in allowed, "Unsupported extension for the selected asset role.")
    payload = value.get("data")
    require(isinstance(payload, str) and len(payload) <= (MAX_MEDIA + 2) // 3 * 4, "Media exceeds 16 MiB.")
    try:
        data = base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError):
        raise ContractError("Invalid base64 asset.") from None
    require(0 < len(data) <= MAX_MEDIA, "Media must be between 1 byte and 16 MiB.")
    # Reject playlist/manifest bytes before FFmpeg can interpret them as references.
    magic = {
        ".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
        ".jpg": data.startswith(b"\xff\xd8"),
        ".jpeg": data.startswith(b"\xff\xd8"),
        ".webp": data[:4] == b"RIFF" and data[8:12] == b"WEBP",
        ".mp4": data[4:8] == b"ftyp",
        ".m4a": data[4:8] == b"ftyp",
        ".wav": data[:4] == b"RIFF" and data[8:12] == b"WAVE",
        ".mp3": data.startswith(b"ID3") or len(data) > 1 and data[0] == 255 and data[1] & 224 == 224,
    }
    require(magic[ext], "Media signature does not match the extension.")
    sha = hashlib.sha256(data).hexdigest()
    metadata = {
        key: string(value.get(key, ""), key, 1000) for key in ("rights", "source", "disclosure", "consent")
    }
    identifier = hashlib.sha256((role + ext + sha + str(metadata)).encode()).hexdigest()[:24]
    asset_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    target = safe_path(asset_dir, identifier + ext)
    if target.exists():
        require(sha_file(target) == sha, "Stored asset bytes changed.")
        duration = probe(target, ext, role)
    else:
        with tempfile.NamedTemporaryFile(dir=asset_dir, suffix=ext, delete=False) as temp:
            temp.write(data)
            path = Path(temp.name)
        try:
            duration = probe(path, ext, role)
            os.replace(path, target)
        finally:
            path.unlink(missing_ok=True)
    return {
        "id": identifier,
        "name": name,
        "role": role,
        "ext": ext,
        "sha256": sha,
        "durationMs": duration,
        **metadata,
    }
