from recon13.http import _title


def test_title_extracts_and_normalizes() -> None:
    html = "<html><head><title>  Hello   World </title></head></html>"
    assert _title(html) == "Hello World"


def test_title_missing() -> None:
    assert _title("<html></html>") is None


def test_title_is_capped() -> None:
    assert len(_title("<title>" + ("x" * 500) + "</title>")) == 200
