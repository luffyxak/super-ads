"""Loopback request boundaries for the Studio server."""

import http.client
import tempfile
import threading
import unittest

from studio.server import StudioServer
from studio.store import Store


class HTTPContract(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        server = StudioServer(0, Store(folder.name))
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.port = server.server_port

    def request(self, method, path, **kwargs):
        client = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            client.request(method, path, **kwargs)
            response = client.getresponse()
            return response.status, response.read()
        finally:
            client.close()

    def test_origin_and_host_guards_apply_to_sensitive_routes(self):
        for headers in ({"Origin": "http://attacker.invalid"}, {"Host": "attacker.invalid"}):
            status, _ = self.request("GET", "/api/projects", headers=headers)
            self.assertEqual(status, 400)
        status, _ = self.request("GET", "/api/projects", headers={"Sec-Fetch-Site": "cross-site"})
        self.assertEqual(status, 400)
        status, _ = self.request(
            "GET",
            "/api/projects/quiet-hours/assets/" + "a" * 24 + "?preview=" + "a" * 64,
            headers={"Sec-Fetch-Site": "cross-site"},
        )
        self.assertEqual(status, 400)
        self.assertEqual(self.request("GET", "/api/health")[0], 200)

    def test_invalid_project_object_fails_without_writing(self):
        status, _ = self.request(
            "POST",
            "/api/projects",
            body='{"id":"bad","workflow":"15s-reel","brief":"invalid"}',
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 400)
        self.assertEqual(self.request("GET", "/api/projects"), (200, b"[]"))
