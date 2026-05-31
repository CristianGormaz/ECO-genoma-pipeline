from __future__ import annotations

import ipaddress
from typing import Iterable
from urllib.parse import urljoin, urlparse
import urllib.request


ALLOWED_PUBLIC_SOURCE_HOSTS = frozenset(
    {
        "ftp.ncbi.nlm.nih.gov",
        "hgdownload.soe.ucsc.edu",
    }
)


class PublicSourceUrlError(ValueError):
    """Raised when a configurable public source URL is not admissible."""


def _normalized_host(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise PublicSourceUrlError("solo se permiten URLs https para fuentes públicas configurables")
    if not parsed.netloc or not parsed.hostname:
        raise PublicSourceUrlError("la URL debe incluir un dominio público")
    if parsed.username or parsed.password:
        raise PublicSourceUrlError("la URL no debe incluir credenciales")
    return parsed.hostname.rstrip(".").lower()


def _is_private_or_local_host(host: str) -> bool:
    if host in {"localhost"} or host.endswith(".localhost"):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def validate_public_source_url(
    url: str,
    *,
    allowed_hosts: Iterable[str] = ALLOWED_PUBLIC_SOURCE_HOSTS,
    allow_custom_url: bool = False,
) -> str:
    """Validate a configurable public URL before E.C.O. downloads it."""
    host = _normalized_host(url)
    if _is_private_or_local_host(host):
        raise PublicSourceUrlError("la URL apunta a una fuente local, privada o no pública")

    allowed = {item.rstrip(".").lower() for item in allowed_hosts}
    if host not in allowed and not allow_custom_url:
        raise PublicSourceUrlError(
            "dominio no permitido por defecto; usa --allow-custom-url solo para fuentes públicas revisadas"
        )
    return url


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, *, allowed_hosts: Iterable[str], allow_custom_url: bool) -> None:
        self.allowed_hosts = tuple(allowed_hosts)
        self.allow_custom_url = allow_custom_url

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        redirected_url = urljoin(req.full_url, newurl)
        validate_public_source_url(
            redirected_url,
            allowed_hosts=self.allowed_hosts,
            allow_custom_url=self.allow_custom_url,
        )
        return super().redirect_request(req, fp, code, msg, headers, redirected_url)


def open_public_source_url(
    url: str,
    *,
    timeout: int,
    headers: dict[str, str],
    allowed_hosts: Iterable[str] = ALLOWED_PUBLIC_SOURCE_HOSTS,
    allow_custom_url: bool = False,
):
    validate_public_source_url(
        url,
        allowed_hosts=allowed_hosts,
        allow_custom_url=allow_custom_url,
    )
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(
        _GuardedRedirectHandler(
            allowed_hosts=allowed_hosts,
            allow_custom_url=allow_custom_url,
        )
    )
    return opener.open(request, timeout=timeout)
