from __future__ import annotations

import re
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from .models import HttpResult

SECURITY_HEADERS = (
    "strict-transport-security",
    "content-security-policy",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "permissions-policy",
)

_USER_AGENT = "13Recon/0.2 (+authorized-security-testing)"


def _title(text: str) -> str | None:
    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()[:200] or None


def probe(url: str, timeout: float = 8.0) -> HttpResult:
    started = time.perf_counter()
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": _USER_AGENT},
        )
        elapsed = round(time.perf_counter() - started, 3)
        selected = {key.lower(): value for key, value in response.headers.items()}
        return HttpResult(
            requested_url=url,
            final_url=response.url,
            ok=True,
            status=response.status_code,
            elapsed=elapsed,
            title=_title(response.text),
            server=response.headers.get("Server"),
            content_type=response.headers.get("Content-Type"),
            headers={key: selected.get(key, "") for key in SECURITY_HEADERS},
            redirect_count=len(response.history),
        )
    except requests.RequestException as exc:
        return HttpResult(
            requested_url=url,
            final_url=url,
            ok=False,
            elapsed=round(time.perf_counter() - started, 3),
            error=str(exc),
        )


def probe_many(
    urls: Iterable[str],
    workers: int = 10,
    timeout: float = 8.0,
) -> list[HttpResult]:
    urls = list(urls)
    results: list[HttpResult] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(probe, url, timeout): url for url in urls}
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda item: item.requested_url)
