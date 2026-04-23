#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap
from collections.abc import Iterable
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


BASE_URL = "http://www.alexonlinux.com/wp-json/wp/v2"


def fetch_json(path: str, params: dict[str, Any] | None = None) -> tuple[Any, dict[str, str]]:
    query = f"?{urlencode(params or {}, doseq=True)}" if params else ""
    with urlopen(f"{BASE_URL}{path}{query}") as response:
        body = response.read().decode("utf-8")
        headers = {k: v for k, v in response.headers.items()}
    return json.loads(body), headers


def fetch_collection(collection: str) -> list[dict[str, Any]]:
    params = {
        "per_page": 100,
        "_fields": "id,date,slug,link,title,content,categories,tags,comment_status",
    }
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        page_items, _ = fetch_json(f"/{collection}", params={**params, "page": page})
        if not isinstance(page_items, list) or not page_items:
            break
        items.extend(page_items)
        if len(page_items) < params["per_page"]:
            break
        page += 1
    return items


def fetch_term_map(taxonomy: str) -> dict[int, str]:
    params = {"per_page": 100, "_fields": "id,name"}
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        page_items, _ = fetch_json(f"/{taxonomy}", params={**params, "page": page})
        if not isinstance(page_items, list) or not page_items:
            break
        items.extend(page_items)
        if len(page_items) < params["per_page"]:
            break
        page += 1
    return {item["id"]: item["name"] for item in items}


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize_filename(title: str) -> str:
    safe = unescape(title)
    safe = re.sub(r'[<>:"/\\|?*]', "", safe)
    safe = re.sub(r"\s+", " ", safe).strip()
    safe = safe.rstrip(". ")
    return safe or "untitled"


class MarkdownConverter(HTMLParser):
    block_tags = {
        "p",
        "div",
        "section",
        "article",
        "header",
        "footer",
        "aside",
        "blockquote",
        "pre",
        "ul",
        "ol",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.href_stack: list[str | None] = []
        self.link_text_stack: list[list[str]] = []
        self.link_has_image_stack: list[bool] = []
        self.list_stack: list[tuple[str, int]] = []
        self.blockquote_depth = 0
        self.in_pre = False
        self.pre_buffer: list[str] = []
        self.skip_stack: list[str] = []

    def append(self, text: str) -> None:
        if not text:
            return
        if self.in_pre:
            self.pre_buffer.append(text)
        else:
            if self.parts:
                prev = self.parts[-1]
                if prev and text:
                    if prev[-1].isalnum() and text[0] in "[!":
                        self.parts.append(" ")
                    elif prev[-1] == ")" and text[0].isalnum():
                        self.parts.append(" ")
            self.parts.append(text)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def ensure_blank_line(self) -> None:
        joined = "".join(self.parts)
        if not joined.endswith("\n\n"):
            if joined.endswith("\n"):
                self.parts.append("\n")
            else:
                self.parts.append("\n\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)

        if tag in {"script", "style"}:
            self.skip_stack.append(tag)
            return
        if self.skip_stack:
            return

        if tag == "span" and attrs_dict.get("id", "").startswith("more-"):
            return
        if tag == "br":
            self.append("  \n")
            return
        if tag in {"p", "div", "section", "article"}:
            self.ensure_blank_line()
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.ensure_blank_line()
            level = int(tag[1])
            self.append("#" * level + " ")
            return
        if tag in {"strong", "b"}:
            self.append("**")
            return
        if tag in {"em", "i"}:
            self.append("*")
            return
        if tag == "code" and not self.in_pre:
            self.append("`")
            return
        if tag == "pre":
            self.ensure_blank_line()
            self.in_pre = True
            self.pre_buffer = []
            return
        if tag == "blockquote":
            self.ensure_blank_line()
            self.blockquote_depth += 1
            return
        if tag == "a":
            self.href_stack.append(attrs_dict.get("href"))
            self.link_text_stack.append([])
            self.link_has_image_stack.append(False)
            return
        if tag == "img":
            class_names = attrs_dict.get("class", "")
            if "wp-smiley" in class_names:
                alt = collapse_ws(unescape(attrs_dict.get("alt") or ""))
                if alt:
                    if self.link_text_stack:
                        self.link_text_stack[-1].append(alt)
                    else:
                        self.append(alt)
                return
            alt = collapse_ws(unescape(attrs_dict.get("alt") or "image"))
            src = attrs_dict.get("src") or ""
            if src:
                if self.link_has_image_stack:
                    self.link_has_image_stack[-1] = True
                self.append(f"![{alt}]({src})")
            return
        if tag == "ul":
            self.ensure_blank_line()
            self.list_stack.append(("ul", 0))
            return
        if tag == "ol":
            self.ensure_blank_line()
            self.list_stack.append(("ol", 0))
            return
        if tag == "li":
            if self.list_stack:
                kind, index = self.list_stack[-1]
                if kind == "ol":
                    index += 1
                    self.list_stack[-1] = (kind, index)
                    marker = f"{index}. "
                else:
                    marker = "- "
                self.append(("  " * (len(self.list_stack) - 1)) + marker)
            return

    def handle_endtag(self, tag: str) -> None:
        if self.skip_stack:
            if tag == self.skip_stack[-1]:
                self.skip_stack.pop()
            return

        if tag in {"strong", "b"}:
            self.append("**")
            return
        if tag in {"em", "i"}:
            self.append("*")
            return
        if tag == "code" and not self.in_pre:
            self.append("`")
            return
        if tag == "pre":
            code = "".join(self.pre_buffer).strip("\n")
            self.parts.append(f"```text\n{code}\n```\n\n")
            self.in_pre = False
            self.pre_buffer = []
            return
        if tag == "blockquote":
            self.parts.append("\n")
            self.blockquote_depth = max(0, self.blockquote_depth - 1)
            self.ensure_blank_line()
            return
        if tag == "a":
            href = self.href_stack.pop() if self.href_stack else None
            text_parts = self.link_text_stack.pop() if self.link_text_stack else []
            link_has_image = self.link_has_image_stack.pop() if self.link_has_image_stack else False
            if link_has_image and not text_parts:
                return
            text = collapse_ws("".join(text_parts)) or (href or "")
            if href:
                self.append(f"[{text}]({href})")
            else:
                self.append(text)
            return
        if tag in {"p", "div", "section", "article", "li"}:
            self.append("\n")
            return
        if tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self.ensure_blank_line()
            return
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self.parts.append("\n\n")
            return

    def handle_data(self, data: str) -> None:
        if self.skip_stack:
            return
        if not data:
            return

        text = data if self.in_pre else collapse_ws(unescape(data))
        if not text:
            return

        if self.link_text_stack:
            self.link_text_stack[-1].append(text)
            return

        if self.blockquote_depth and not self.in_pre:
            lines = text.splitlines() or [text]
            prefix = "> " * self.blockquote_depth
            for i, line in enumerate(lines):
                if i > 0:
                    self.append("\n")
                self.append(prefix + line.strip())
            return

        self.append(text)

    def get_markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"(?<=[A-Za-z0-9])(\[[^]\n]+\]\([^)]+\))", r" \1", text)
        text = re.sub(r"(\[[^]\n]+\]\([^)]+\))(?=[A-Za-z0-9])", r"\1 ", text)
        return text.strip() + "\n"


def html_to_markdown(html: str) -> str:
    parser = MarkdownConverter()
    parser.feed(html)
    return parser.get_markdown()


def format_front_matter(
    *,
    title: str,
    item_type: str,
    created_at: str,
    url: str,
    categories: Iterable[str],
    tags: Iterable[str],
) -> str:
    def yaml_list(values: Iterable[str]) -> str:
        values = list(values)
        if not values:
            return "[]"
        return "[" + ", ".join(json.dumps(value, ensure_ascii=False) for value in values) + "]"

    return textwrap.dedent(
        f"""\
        ---
        title: {json.dumps(title, ensure_ascii=False)}
        type: {json.dumps(item_type)}
        created_at: {json.dumps(created_at)}
        original_url: {json.dumps(url)}
        categories: {yaml_list(categories)}
        tags: {yaml_list(tags)}
        ---

        """
    )


def export_items(
    *,
    items: list[dict[str, Any]],
    item_type: str,
    destination: Path,
    category_map: dict[int, str],
    tag_map: dict[int, str],
) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for item in items:
        title = unescape(item["title"]["rendered"]).strip()
        created_at = item["date"]
        timestamp = datetime.fromisoformat(created_at).strftime("%Y-%m-%dT%H%M%S")
        filename = f"{timestamp} {sanitize_filename(title)}.md"
        path = destination / filename
        categories = [category_map.get(category_id, str(category_id)) for category_id in item.get("categories", [])]
        tags = [tag_map.get(tag_id, str(tag_id)) for tag_id in item.get("tags", [])]
        markdown = html_to_markdown(item["content"]["rendered"])
        front_matter = format_front_matter(
            title=title,
            item_type=item_type,
            created_at=created_at,
            url=item["link"],
            categories=categories,
            tags=tags,
        )
        path.write_text(front_matter + markdown, encoding="utf-8")
        written.append(path)
    return written


def write_manifest(
    *,
    output: Path,
    posts: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    category_map: dict[int, str],
    tag_map: dict[int, str],
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["type", "created_at", "title", "url", "categories", "tags"])
        for item_type, items in (("post", posts), ("page", pages)):
            for item in items:
                writer.writerow(
                    [
                        item_type,
                        item["date"],
                        unescape(item["title"]["rendered"]).strip(),
                        item["link"],
                        "; ".join(category_map.get(category_id, str(category_id)) for category_id in item.get("categories", [])),
                        "; ".join(tag_map.get(tag_id, str(tag_id)) for tag_id in item.get("tags", [])),
                    ]
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export WordPress posts and pages into Markdown files.")
    parser.add_argument("--output", default="export", help="Output directory")
    args = parser.parse_args()

    output = Path(args.output)
    posts = fetch_collection("posts")
    pages = fetch_collection("pages")
    category_map = fetch_term_map("categories")
    tag_map = fetch_term_map("tags")

    post_files = export_items(
        items=posts,
        item_type="post",
        destination=output / "posts",
        category_map=category_map,
        tag_map=tag_map,
    )
    page_files = export_items(
        items=pages,
        item_type="page",
        destination=output / "pages",
        category_map=category_map,
        tag_map=tag_map,
    )
    write_manifest(
        output=output / "manifest.csv",
        posts=posts,
        pages=pages,
        category_map=category_map,
        tag_map=tag_map,
    )

    print(f"Exported {len(post_files)} posts to {output / 'posts'}")
    print(f"Exported {len(page_files)} pages to {output / 'pages'}")
    print(f"Wrote manifest to {output / 'manifest.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
