#!/usr/bin/env python3
"""Shared OpenAI API-key handling for the image production pipeline.

The key must come from the OPENAI_API_KEY environment variable, set by the
runtime/session's own secret mechanism -- never hard-coded, never written to
a file in this repo, never logged or printed. Every function here that could
touch the key is written so no exception message can ever contain it.
"""
from __future__ import annotations

import os


class MissingAPIKeyError(RuntimeError):
    pass


def get_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY is not set. Export it in your shell, or set it as "
            "an environment variable in your session/runtime's secret "
            "configuration, before running this tool -- e.g. "
            "`export OPENAI_API_KEY=...` locally, or as an environment "
            "variable on your Claude Code Remote environment. Never put the "
            "key in a script, config file, or commit."
        )
    return key


def build_client():
    """Return an authenticated openai.OpenAI client, or raise a clear error."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The 'openai' package is not installed. Run: "
            "pip install -r requirements.txt"
        ) from exc
    return OpenAI(api_key=get_api_key())
