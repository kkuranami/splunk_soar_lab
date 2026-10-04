#!/usr/bin/env python3

import json
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def route(path):
    if path == "/health":
        return {"status": "ok"}
    if path.startswith("/intel/ip/"):
        return {"verdict": "malicious" if path.endswith("/192.0.2.10") else "unknown"}
    if path == "/containment/block-ip":
        return {"result": "simulated"}
    return None

class Handler(BaseHTTPRequestHandler):
    def respond(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        payload = route(self.path)
        body = json.dumps(payload or {"error": "not found"}).encode()
        self.send_response(200 if payload else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = do_POST = respond

host = socket.gethostbyname(socket.gethostname())
print("mock-api listening on http://%s:8080" % host, flush=True)
ThreadingHTTPServer((host, 8080), Handler).serve_forever()
