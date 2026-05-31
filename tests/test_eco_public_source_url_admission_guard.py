import pytest

from scripts.eco_public_source_guard import (
    PublicSourceUrlError,
    validate_public_source_url,
)
from scripts.run_eco_clinvar_sample_report import DEFAULT_SOURCE_URL as CLINVAR_SOURCE_URL
from scripts.run_eco_clinvar_sample_report import build_parser as build_clinvar_parser
from scripts.run_eco_clinvar_sample_report import download_file as download_clinvar_file
from scripts.run_eco_public_chrM_report import DEFAULT_SOURCE_URL as CHRM_SOURCE_URL
from scripts.run_eco_public_chrM_report import build_arg_parser as build_chrm_parser
from scripts.run_eco_public_chrM_report import download_file as download_chrm_file


@pytest.mark.parametrize(
    "url",
    [
        CHRM_SOURCE_URL,
        CLINVAR_SOURCE_URL,
    ],
)
def test_allowlisted_public_https_sources_pass(url):
    assert validate_public_source_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "http://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chrM.fa.gz",
        "file:///etc/passwd",
        "https://localhost:8000/secreto",
        "https://127.0.0.1/secreto",
        "https://10.0.0.4/dataset",
        "https://172.16.1.10/dataset",
        "https://192.168.1.20/dataset",
        "https://[::1]/dataset",
        "https://dominio-no-verificado.com/dataset",
    ],
)
def test_public_source_url_guard_rejects_unsafe_or_unexpected_sources(url):
    with pytest.raises(PublicSourceUrlError):
        validate_public_source_url(url)


def test_custom_public_https_domain_requires_explicit_admission():
    url = "https://example.org/public-demo.fa.gz"

    with pytest.raises(PublicSourceUrlError):
        validate_public_source_url(url)

    assert validate_public_source_url(url, allow_custom_url=True) == url


@pytest.mark.parametrize(
    "parser_factory",
    [
        build_chrm_parser,
        build_clinvar_parser,
    ],
)
def test_public_source_scripts_expose_explicit_custom_url_flag(parser_factory):
    args = parser_factory().parse_args(["--allow-custom-url"])
    assert args.allow_custom_url is True


@pytest.mark.parametrize(
    "download_function",
    [
        download_chrm_file,
        download_clinvar_file,
    ],
)
def test_download_helpers_validate_url_even_when_cache_exists(download_function, tmp_path):
    cached_file = tmp_path / "cached.gz"
    cached_file.write_bytes(b"cached")

    with pytest.raises(PublicSourceUrlError):
        download_function("file:///etc/passwd", cached_file)
