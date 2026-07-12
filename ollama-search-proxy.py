#!/usr/bin/env python3
"""
Tiny local CORS proxy for Ollama's hosted web search API.

Browsers block direct calls from a web page to https://ollama.com/api/web_search
because that endpoint doesn't send CORS headers (this is true of almost every
API that requires an API key - it's a deliberate security choice, not a bug).
This script runs on your own machine, forwards your search requests to Ollama's
API server-to-server (where CORS doesn't apply), and adds the CORS headers back
in on its own response so your browser will accept it.

It does not read, log, or store your API key - it just relays the Authorization
header you send it straight through to Ollama on each request.

Usage:
    python3 ollama-search-proxy.py [port]      (macOS/Linux)
    python ollama-search-proxy.py [port]       (Windows, or if python3 isn't on PATH)

Default port is 8787. Then, in the app's Search panel, set "Proxy URL" to:
    http://127.0.0.1:8787

Requires only the Python standard library. If you hit a certificate error
(most common on macOS), the script will print exactly which Python it's
running as and what to install to fix it. If installing certifi doesn't
help, you can run with OLLAMA_SEARCH_PROXY_INSECURE=1 set in your environment
to temporarily skip certificate checks and confirm whether it's really a
certificate problem or something else (e.g. a corporate firewall) - this is
for diagnosis only, not something to leave on.
"""
import sys
import os
import json
import ssl
import platform
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

UPSTREAM = 'https://ollama.com/api/web_search'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
INSECURE = os.environ.get('OLLAMA_SEARCH_PROXY_INSECURE') == '1'


def build_ssl_context():
    """Prefer certifi's CA bundle when available - it's the most reliable
    option across macOS/Windows/Linux and side-steps the well-known macOS
    python.org issue where Python doesn't use the system trust store. Falls
    back to the OS default trust store (fine on most Linux/Windows setups)
    if certifi isn't installed."""
    if INSECURE:
        print('\n*** OLLAMA_SEARCH_PROXY_INSECURE=1: certificate verification is OFF. ***')
        print('*** This is for diagnosing SSL issues only - your API key is not protected against')
        print('*** interception while this is on. Unset it once you know the real problem. ***\n')
        return ssl._create_unverified_context()
    try:
        import certifi
        print(f'Using certifi CA bundle: {certifi.where()}')
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        print('certifi not installed - using the OS default certificate trust store.')
        print(f'If you hit SSL errors below, run: {sys.executable} -m pip install certifi')
        return ssl.create_default_context()


print(f'Python: {sys.executable} ({platform.python_version()}, {platform.system()})')
SSL_CONTEXT = build_ssl_context()

CERT_FIX_MSG = (
    'SSL certificate verification failed while contacting ollama.com. '
    'This is a local Python/OS setup issue, not a problem with Ollama or this app. '
    f'Fix: run "{sys.executable} -m pip install certifi" (this exact command matters - '
    'installing certifi for a different Python than the one running this script won\'t help) '
    'then restart this script.'
)
if platform.system() == 'Darwin':
    CERT_FIX_MSG += (
        ' On macOS with Python installed from python.org, you can alternatively run the '
        '"Install Certificates.command" script found in your Python installation folder '
        '(usually under /Applications/Python 3.x/).'
    )


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0) or 0)
        body = self.rfile.read(length) if length else b''

        req = urllib.request.Request(UPSTREAM, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        auth = self.headers.get('Authorization')
        if auth:
            req.add_header('Authorization', auth)

        try:
            with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
                data = resp.read()
                status = resp.status
        except urllib.error.HTTPError as e:
            data = e.read()
            status = e.code
        except Exception as e:
            msg = str(e)
            if 'CERTIFICATE_VERIFY_FAILED' in msg or 'certificate verify failed' in msg:
                print(f'\n[ollama-search-proxy] {CERT_FIX_MSG}\n', file=sys.stderr)
                msg = CERT_FIX_MSG
            data = json.dumps({'error': msg}).encode()
            status = 502

        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass  # keep stdout quiet; remove this to see request logs


if __name__ == '__main__':
    HOST = '127.0.0.1'
    print(f'Ollama search proxy listening on http://{HOST}:{PORT}')
    print('Leave this running, then set "Proxy URL" to the address above in the app\'s Search panel.')
    print('Press Ctrl+C to stop.')
    try:
        HTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
    except OSError as e:
        if 'Address already in use' in str(e) or getattr(e, 'errno', None) in (48, 98, 10048):
            print(f'\nPort {PORT} is already in use - is the proxy already running, or is something else using it?')
            print(f'Try a different port: python3 ollama-search-proxy.py {PORT + 1}')
        else:
            print(f'\nCould not start server: {e}')
        sys.exit(1)
