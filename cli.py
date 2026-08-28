from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from . import __version__
from .dns import lookup
from .http import SECURITY_HEADERS, probe_many

_DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="13recon",
        description="13Recon — lightweight reconnaissance for authorized security research.",
    )
    parser.add_argument("target", help="Domain name to inspect (for systems you own or are authorized to test)")
    parser.add_argument("--timeout", type=float, default=8.0, help="Per-request timeout in seconds (default: 8)")
    parser.add_argument("--workers", type=int, default=10, help="Concurrent HTTP workers (default: 10)")
    parser.add_argument("--dns-timeout", type=float, default=4.0, help="DNS timeout in seconds (default: 4)")
    parser.add_argument("--json", dest="json_path", metavar="PATH", help="Write a JSON report to PATH")
    return parser


def _validate_args(args: argparse.Namespace) -> str:
    target = args.target.strip().lower().rstrip(".")
    if not target or not _DOMAIN_RE.fullmatch(target):
        raise ValueError("invalid domain name")
    if args.timeout <= 0 or args.dns_timeout <= 0:
        raise ValueError("timeouts must be greater than zero")
    if args.workers < 1 or args.workers > 100:
        raise ValueError("workers must be between 1 and 100")
    return target


def _print_report(target: str, dns_data: dict[str, list[str]], http_data: list) -> None:
    print(f"13Recon v{__version__} :: authorized recon helper")
    print(f"Target: {target}\n")
    print("DNS")
    for kind, values in dns_data.items():
        print(f"  {kind:<6} {', '.join(values) if values else '-'}")

    print("\nHTTP")
    for item in http_data:
        if item.ok:
            title = item.title or "-"
            elapsed = f"{item.elapsed:.2f}s" if item.elapsed is not None else "-"
            redirect = f" redirects={item.redirect_count}" if item.redirect_count else ""
            print(f"  {item.requested_url:<32} {item.status:<3} {title[:36]:<36} {elapsed}{redirect}")
        else:
            print(f"  {item.requested_url:<32} ERROR  {item.error}")

    print("\nSecurity headers")
    for item in http_data:
        if not item.ok or not item.headers:
            continue
        print(f"  {item.final_url}")
        for header in SECURITY_HEADERS:
            state = "PRESENT" if item.headers.get(header) else "MISSING"
            print(f"    {header:<28} {state}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        target = _validate_args(args)
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    dns_data = lookup(target, timeout=args.dns_timeout)
    urls = [f"https://{target}", f"http://{target}"]
    http_data = probe_many(urls, workers=args.workers, timeout=args.timeout)

    report = {
        "tool": "13Recon",
        "version": __version__,
        "target": target,
        "dns": dns_data,
        "http": [item.to_dict() for item in http_data],
    }

    _print_report(target, dns_data, http_data)

    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nJSON report written to {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
