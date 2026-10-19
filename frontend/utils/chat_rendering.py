# -*- coding: utf-8 -*-
"""Safe Markdown rendering and script-aware direction for chat bubbles."""

import bleach
from markdown_it import MarkdownIt


def contains_urdu_script(text: str) -> bool:
    return any(
        "\u0600" <= char <= "\u06ff"
        or "\u0750" <= char <= "\u077f"
        or "\ufb50" <= char <= "\ufdff"
        or "\ufe70" <= char <= "\ufeff"
        for char in text
    )


def assistant_markup(text: str, language: str) -> str:
    """Render common Markdown safely while retaining normal Unicode shaping."""
    rendered = MarkdownIt("commonmark").enable("table").render(text or "")
    allowed_tags = {
        "p", "br", "strong", "em", "del", "blockquote", "ul", "ol", "li",
        "h1", "h2", "h3", "h4", "pre", "code", "hr", "table", "thead",
        "tbody", "tr", "th", "td", "a",
    }
    safe_html = bleach.clean(
        rendered,
        tags=allowed_tags,
        attributes={"a": ["href", "title"]},
        protocols={"http", "https", "mailto"},
        strip=True,
    )
    rtl = language == "urdu" or contains_urdu_script(text or "")
    direction = "rtl" if rtl else "ltr"
    text_class = "urdu-text" if rtl else "ltr-text"
    return (
        '<div class="chat-row" style="justify-content:flex-start;">'
        '<div class="ai-bubble-wrap"><div class="ai-avatar">🧠</div>'
        f'<div class="assistant-bubble {text_class}" dir="{direction}">{safe_html}</div>'
        '</div></div>'
    )
