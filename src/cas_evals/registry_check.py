"""Registry-fetch smoke check for the live cas-contracts GitHub Pages registry.

Performs live HTTP GETs against known-published registry paths and asserts
each responds with HTTP 200. This is deliberately network-dependent and
distinct from cas_evals.contracts.verify_vendored_contract(), which only
checks bytes on disk and never touches the network. The two mechanisms are
additive: verify_vendored_contract() proves the pinned offline copy is intact;
this module proves the live registry actually resolves today.
"""

from __future__ import annotations

import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://coding-autopilot-system.github.io/cas-contracts/registry"
DEFAULT_PATHS = (
    "index.json",
    "v0.1/manifest.json",
    "v0.1/common.schema.json",
    "v0.1/evaluation-result.schema.json",
)
MAX_RESPONSE_BYTES = 2_000_000


class RegistryCheckError(RuntimeError):
    """Raised when a registry-fetch smoke check fails."""


def check_registry_urls(
    base_url: str,
    paths: list[str] | tuple[str, ...],
    timeout_seconds: float = 10,
) -> list[tuple[str, int]]:
    """Fetch each path joined onto base_url and assert HTTP 200.

    Returns a list of (path, status_code) tuples when every URL responds
    with 200. Raises RegistryCheckError naming the first failing path if any
    URL returns non-200, times out, or the network is unavailable.
    """
    results: list[tuple[str, int]] = []
    for path in paths:
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        request = Request(url, method="GET")
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                status = response.status
                response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as error:
            raise RegistryCheckError(f"{path} returned HTTP {error.code}") from error
        except (URLError, TimeoutError, OSError) as error:
            raise RegistryCheckError(f"{path} is unavailable (network error)") from error
        if status != 200:
            raise RegistryCheckError(f"{path} returned HTTP {status}")
        results.append((path, status))
    return results


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: python -m cas_evals.registry_check [--base-url URL]."""
    args = list(sys.argv[1:] if argv is None else argv)
    base_url = DEFAULT_BASE_URL
    if "--base-url" in args:
        index = args.index("--base-url")
        base_url = args[index + 1]

    try:
        results = check_registry_urls(base_url, DEFAULT_PATHS)
    except RegistryCheckError as error:
        print(f"FAIL: {error}")
        return 1

    for path, status in results:
        print(f"{path}: {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
