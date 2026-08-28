import pytest

from recon13.cli import _validate_args, build_parser


def test_validate_args_accepts_domain() -> None:
    args = build_parser().parse_args(["Example.COM", "--workers", "5"])
    assert _validate_args(args) == "example.com"


@pytest.mark.parametrize("target", ["", "https://example.com", "not a domain"])
def test_validate_args_rejects_invalid_target(target: str) -> None:
    args = build_parser().parse_args([target])
    with pytest.raises(ValueError):
        _validate_args(args)
