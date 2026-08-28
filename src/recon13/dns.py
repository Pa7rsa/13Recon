from __future__ import annotations

import dns.exception
import dns.resolver

RECORD_TYPES = ("A", "AAAA", "CNAME")


def lookup(name: str, timeout: float = 4.0) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {record_type: [] for record_type in RECORD_TYPES}
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout

    for record_type in RECORD_TYPES:
        try:
            answers = resolver.resolve(name, record_type)
            result[record_type] = [answer.to_text().rstrip(".") for answer in answers]
        except (dns.exception.DNSException, OSError):
            result[record_type] = []
    return result
