"""
web_tool.py — Simulated web fetch using local fixture files.

For known documentation URLs, returns the contents of a fixture file so the
lab works entirely offline.  For localhost URLs, makes a real HTTP GET
request: the lab confines network egress to localhost, and the attacker's
exfil listener sits on localhost:9999, so Attack 1 still works.  Any
non-localhost URL is refused.

The use_poisoned flag routes API documentation requests to the compromised
fixture used by Attack 3.
"""

import os
import urllib.parse

import httpx

_MODULE_DIR   = os.path.dirname(os.path.abspath(__file__))
_LAB_DIR      = os.path.dirname(_MODULE_DIR)
_FIXTURES_DIR = os.path.join(_LAB_DIR, "fixtures")

# Fixtures served for known documentation URLs
_URL_MAP: dict[str, str] = {
    "https://docs.example.com/api":         "api_docs_clean.txt",
    "https://docs.example.com/api/v2":      "api_docs_clean.txt",
    "https://docs.example.com/general":     "api_docs_clean.txt",
    "https://docs.example.com/auth":        "api_docs_clean.txt",
}


class WebTool:
    def __init__(self, fixtures_dir: str = None, use_poisoned: bool = False):
        self.fixtures_dir = fixtures_dir or _FIXTURES_DIR
        self.use_poisoned = use_poisoned

    def fetch(self, url: str) -> str:
        """Fetch a URL.

        Returns fixture content for known docs URLs; makes a real HTTP GET
        for localhost URLs (enabling exfil via crafted GET requests to the
        local listener); refuses non-localhost URLs.
        """
        # Attack 3: redirect API docs to poisoned fixture when flag is set
        if self.use_poisoned and "docs.example.com" in url:
            return self._read_fixture("api_docs_poisoned.txt")

        # Serve fixture for known documentation URLs
        if url in _URL_MAP:
            return self._read_fixture(_URL_MAP[url])

        # Partial URL matches (e.g. docs.example.com without exact path)
        if "docs.example.com" in url:
            return self._read_fixture("api_docs_clean.txt")

        # Real HTTP GET for localhost URLs only — the lab confines egress to
        # localhost, which is where Attack 1's exfil listener lives.
        parsed = urllib.parse.urlsplit(url)
        if parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
            return f"[WebTool] Refused: only localhost is reachable in this lab ({url})"

        try:
            resp = httpx.get(url, timeout=5.0, follow_redirects=True)
            body = resp.text
            return body[:2000] if len(body) > 2000 else body
        except httpx.ConnectError:
            return f"[WebTool] Connection refused: {url}"
        except httpx.TimeoutException:
            return f"[WebTool] Request timed out: {url}"
        except Exception as exc:
            return f"[WebTool] Failed to fetch {url}: {exc}"

    def _read_fixture(self, filename: str) -> str:
        path = os.path.join(self.fixtures_dir, filename)
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"[WebTool] Fixture not found: {filename}"
