from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class HttpResult:
    requested_url: str
    final_url: str
    ok: bool
    status: int | None = None
    elapsed: float | None = None
    title: str | None = None
    server: str | None = None
    content_type: str | None = None
    headers: dict[str, str] | None = None
    redirect_count: int = 0
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
