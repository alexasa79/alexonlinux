#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import mimetypes
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import urlopen


POSTS_DIR = Path("content/essays")
ASSETS_DIR = Path("static/assets")
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\((https?://[^)]+)\)")


def slugify(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._ -]", "", name)
    safe = re.sub(r"\s+", " ", safe).strip()
    return safe or "post"


def choose_extension(url: str, content_type: str | None) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
        return suffix
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed:
            return guessed
    return ".img"


def build_asset_path(destination: Path, extension: str) -> Path:
    return destination.parent / f"{destination.name}{extension}"


def download_image(url: str, destination: Path) -> Path:
    with urlopen(url) as response:
        content = response.read()
        content_type = response.headers.get("Content-Type")
    extension = choose_extension(url, content_type)
    final_path = build_asset_path(destination, extension)
    final_path.write_bytes(content)
    return final_path


def iter_post_files() -> Iterable[Path]:
    return sorted(POSTS_DIR.glob("*.md"))


def main() -> int:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    total_downloads = 0
    touched_files = 0

    for post_path in iter_post_files():
        text = post_path.read_text(encoding="utf-8")
        matches = list(IMAGE_PATTERN.finditer(text))
        if not matches:
            continue

        post_asset_dir = ASSETS_DIR / slugify(post_path.stem)
        post_asset_dir.mkdir(parents=True, exist_ok=True)
        replacements: dict[str, str] = {}

        for match in matches:
            url = match.group(2)
            if url in replacements:
                continue

            parsed = urlparse(url)
            parsed_path = Path(parsed.path)
            raw_name = parsed_path.name or "image"
            if parsed_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
                base_name = parsed_path.stem or "image"
            else:
                base_name = raw_name
            digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
            temp_destination = post_asset_dir / f"{slugify(base_name)}-{digest}"
            downloaded = download_image(url, temp_destination)
            relative_path = Path("..") / "assets" / post_asset_dir.name / downloaded.name
            replacements[url] = relative_path.as_posix()
            total_downloads += 1

        updated = text
        for url, local_path in replacements.items():
            updated = updated.replace(f"]({url})", f"]({local_path})")

        if updated != text:
            post_path.write_text(updated, encoding="utf-8")
            touched_files += 1

    print(f"Downloaded {total_downloads} images")
    print(f"Updated {touched_files} markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
