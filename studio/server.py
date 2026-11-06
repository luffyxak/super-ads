"""Loopback-only HTTP interface for the shared project engine."""

import hmac
import json
import mimetypes
import re
import secrets
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from .contracts import ROOT, RATIOS, ContractError, canonical, require
from .demo import fixture_handoffs, load_demo
from .jobs import render_job
from .media_import import MAX_MEDIA
from .store import public

WEB = ROOT / "studio" / "web"
MIME = {".js": "text/javascript", ".html": "text/html; charset=utf-8", ".srt": "text/plain; charset=utf-8"}
CSP = "default-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self'"
PREVIEW_CSP = (
    "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
    "img-src 'self' data:; media-src 'self' data:; font-src 'self' data:; frame-ancestors 'self'"
)


class StudioServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, port, store):
        super().__init__(("127.0.0.1", port), Handler)
        self.store = store
        self.host = f"127.0.0.1:{self.server_port}"
        self.preview_key = secrets.token_bytes(32)


class Handler(BaseHTTPRequestHandler):
    server_version = "SuperAdsStudio"
    sys_version = ""

    def setup(self):
        super().setup()
        self.connection.settimeout(25)

    @property
    def store(self):
        return self.server.store

    def log_message(self, *_):
        # Project and file names can be client data.
        pass

    def _headers(self, status, mime, size, *, csp=CSP, extra=None):
        self.send_response(status)
        for name, value in {
            "Content-Type": mime,
            "Content-Length": str(size),
            "Content-Security-Policy": csp,
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
            "Cross-Origin-Resource-Policy": "same-origin",
            **(extra or {}),
        }.items():
            self.send_header(name, value)
        self.end_headers()

    def _bytes(self, data, mime, status=200, **kwargs):
        self._headers(status, mime, len(data), **kwargs)
        if self.command != "HEAD":
            self.wfile.write(data)

    def _json(self, data, status=200):
        self._bytes(canonical(data).encode(), "application/json; charset=utf-8", status)

    def _send_file(self, file, attachment=False, preview_media=False):
        size = file.stat().st_size
        start, end = 0, size - 1
        status, headers = 200, {"Accept-Ranges": "bytes"}
        if preview_media:
            headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        if range_ := self.headers.get("Range"):
            match = re.fullmatch(r"bytes=(\d{0,18})-(\d{0,18})", range_)
            if not match or not any(match.groups()):
                self._bytes(b"", "text/plain", 416, extra={"Content-Range": f"bytes */{size}"})
                return
            first, last = match.groups()
            start = int(first) if first else max(0, size - int(last))
            end = min(size - 1, int(last)) if first and last else size - 1
            if not 0 <= start <= end < size:
                self._bytes(b"", "text/plain", 416, extra={"Content-Range": f"bytes */{size}"})
                return
            status = 206
            headers["Content-Range"] = f"bytes {start}-{end}/{size}"
        if attachment:
            headers["Content-Disposition"] = f'attachment; filename="{file.name}"'
        mime = MIME.get(file.suffix) or mimetypes.guess_type(file)[0] or "application/octet-stream"
        self._headers(status, mime, end - start + 1, extra=headers)
        if self.command != "HEAD":
            with file.open("rb") as source:
                source.seek(start)
                remaining = end - start + 1
                while remaining:
                    data = source.read(min(remaining, 128 * 1024))
                    if not data:
                        break
                    self.wfile.write(data)
                    remaining -= len(data)

    def _asset_token(self, path):
        return hmac.digest(self.server.preview_key, path.encode(), "sha256").hex()

    def _preview_asset(self, url):
        if self.command not in {"GET", "HEAD"} or not re.fullmatch(
            r"/api/projects/[a-z0-9-]+/assets/[0-9a-f]{24}", url.path
        ):
            return False
        token = parse_qs(url.query).get("preview", [""])[0]
        return token.isascii() and hmac.compare_digest(token, self._asset_token(url.path))

    def _preview_url(self, project, asset):
        path = f"/api/projects/{project}/assets/{asset}"
        return f"{path}?preview={self._asset_token(path)}"

    def _guard(self, url):
        allowed = {self.server.host, f"localhost:{self.server.server_port}"}
        host = self.headers.get("Host")
        require(host in allowed, "Use the studio’s loopback origin.")
        if self._preview_asset(url) and self.headers.get("Origin") in (None, "null", f"http://{host}"):
            return
        origin = self.headers.get("Origin")
        require(not origin or origin == f"http://{host}", "Cross-origin requests are blocked.")
        require(self.headers.get("Sec-Fetch-Site", "") != "cross-site", "Cross-site requests are blocked.")

    def _body(self):
        require(self.headers.get_content_type() == "application/json", "Send application/json.")
        length = self.headers.get("Content-Length", "")
        require(length.isascii() and length.isdigit() and len(length) <= 9, "Invalid request length.")
        limit = (MAX_MEDIA + 2) // 3 * 4 + 65536 if self.path.endswith("/import") else 262144
        require(0 < int(length) <= limit, "Request exceeds its size limit.")
        try:
            data = json.loads(self.rfile.read(int(length)))
        except (UnicodeError, ValueError, RecursionError):
            raise ContractError("Invalid JSON body.") from None
        require(isinstance(data, dict), "Expected a JSON object.")
        return data

    def _get(self, url):
        path = url.path
        if path in {"/", "/app.js", "/style.css"}:
            return self._send_file(WEB / ("index.html" if path == "/" else path[1:]))
        if path == "/api/health":
            return self._json({"ok": True})
        if path == "/api/projects":
            return self._json(self.store.list())
        parts = path.strip("/").split("/")
        require(len(parts) >= 3 and parts[:2] == ["api", "projects"], "Unknown route.")
        state = self.store.get(parts[2], raw=True)
        if len(parts) == 3:
            return self._json(public(state))
        query = parse_qs(url.query)
        if parts[3:] in (["preview"], ["reference"]) and "cut" in query:
            cut = query["cut"][0]
            require(cut in state["cuts"], "Save the secondary cut before previewing it.")
            state = {**state, "shots": state["cuts"][cut], "hooks": [], "selectedHook": "", "tracks": []}
        if parts[3:] == ["history"]:
            return self._json(self.store.history(state["id"]))
        if parts[3:] == ["preview"]:
            from .render import preview_html

            ratio = query.get("format", ["9x16"])[0]
            hook = query.get("hook", [None])[0]
            seconds = query.get("time", ["0"])[0]
            require(
                re.fullmatch(r"\d{1,2}(\.\d{1,6})?", seconds) and ratio in RATIOS,
                "Invalid preview time or format.",
            )
            require(state["shots"], "Add a storyboard shot to preview.")
            require(hook is None or any(item["id"] == hook for item in state["hooks"]), "Unknown hook.")
            html = preview_html(
                state,
                round(float(seconds) * 1000),
                ratio,
                hook,
                media_url=lambda asset: self._preview_url(state["id"], asset),
                captions=query.get("captions", ["1"])[0] != "0",
            )
            return self._bytes(html.encode(), MIME[".html"], csp=PREVIEW_CSP)
        if parts[3:] == ["reference"]:
            from .render import reference_html

            shot = query.get("shot", [""])[0]
            require(any(item["id"] == shot for item in state["shots"]), "Unknown shot.")
            self.store._validate_assets(state)
            html = reference_html(state, shot, self.store.path(state["id"], "assets"))
            return self._bytes(
                html.encode(),
                MIME[".html"],
                csp=PREVIEW_CSP,
                extra={"Content-Disposition": f'attachment; filename="{shot}-reference.html"'},
            )
        if len(parts) == 5 and parts[3] == "assets":
            return self._send_file(
                self.store.asset_path(state, parts[4]), preview_media=self._preview_asset(url)
            )
        if len(parts) == 5 and parts[3] == "files":
            return self._send_file(
                self.store.file_path(state, parts[4]), attachment=query.get("download") == ["1"]
            )
        raise ContractError("Unknown route.")

    def _post(self, url):
        payload = self._body()
        if url.path == "/api/projects":
            return self._json(
                self.store.create(payload.get("id"), payload.get("workflow"), payload.get("brief", {})), 201
            )
        if url.path == "/api/demo":
            return self._json(load_demo(self.store, payload.get("id", "quiet-hours")), 201)
        parts = url.path.strip("/").split("/")
        require(len(parts) == 4 and parts[:2] == ["api", "projects"], "Unknown route.")
        project, action = parts[2:]
        revision = payload.pop("revision", None)
        if action in {"render", "hook"}:
            hook = payload.get("hook") if action == "hook" else None
            if action == "hook":
                require(
                    isinstance(hook, str) and any(h["id"] == hook for h in self.store.get(project)["hooks"]),
                    "Select a valid hook variant.",
                )
            reserved = self.store.reserve(project, revision, action)
            threading.Thread(target=render_job, args=(self.store, reserved, hook), daemon=True).start()
            return self._json(public(reserved), 202)
        if action == "fixture":
            return self._json(fixture_handoffs(self.store, project, revision))
        if action in {"report", "delivery"}:
            return self._json(self.store.build_files(project, revision, release=action == "delivery"))
        return self._json(self.store.change(project, revision, action, payload))

    def _dispatch(self, method):
        try:
            url = urlsplit(self.path)
            require(
                not url.scheme and not url.netloc and "%" not in url.path and ".." not in url.path,
                "Invalid request path.",
            )
            self._guard(url)
            method(url)
        except ContractError as error:
            self._json({"error": str(error)}, 409 if "Revision changed" in str(error) else 400)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            return
        except ValueError:
            self._json({"error": "The preview or input is outside the current project contract."}, 400)
        except (OSError, RuntimeError, ImportError):
            self._json({"error": "A local operation failed. Check storage and render prerequisites."}, 500)

    def do_GET(self):
        self._dispatch(self._get)

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        self._dispatch(self._post)


def serve(store, port):
    with StudioServer(port, store) as server:
        print(f"Super Ads Studio · http://{server.host}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
