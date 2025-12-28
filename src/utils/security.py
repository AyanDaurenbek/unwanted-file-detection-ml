import hashlib
from typing import Tuple

from fastapi import HTTPException, Header

API_KEY_HEADER = "X-API-Key"


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_api_key(api_key: str, provided: str | None) -> None:
    if not provided or provided != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


def sanitize_filename(filename: str) -> str:
    return filename.replace("..", "").replace("/", "_")
