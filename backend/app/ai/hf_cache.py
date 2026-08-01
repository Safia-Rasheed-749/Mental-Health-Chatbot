"""
=========================================================
Hugging Face Cache Configuration
Project : AI Mental Health Chatbot (FYP)

Centralized, cross-platform Hugging Face cache setup.

All AI modules should import this module FIRST, before any
Hugging Face library (e.g. `datasets`, `transformers`,
`huggingface_hub`), so every model / dataset download is
stored in the same location.

Uses the current user's home directory so the project works
on any machine without hardcoded drive paths.
=========================================================
"""

import os
from pathlib import Path

# =====================================================
# Hugging Face Cache (Cross Platform)
# Uses the current user's home directory so the project
# works on any machine without hardcoded drive paths.
# =====================================================

CACHE_ROOT = Path.home() / ".cache" / "huggingface"

os.environ["HF_HOME"] = str(CACHE_ROOT)
os.environ["HF_DATASETS_CACHE"] = str(CACHE_ROOT / "datasets")
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_ROOT / "transformers")
os.environ["TORCH_HOME"] = str(CACHE_ROOT / "torch")

