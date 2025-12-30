# microsoftAuth.py
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import minecraft_launcher_lib


client = "9af2fafb-bfbe-4fbe-9abf-fb3fe9affc7c"
backend = "https://argon-auth.onrender.com"
PORT = 6942
REDIRECT_URI = f"http://localhost:{PORT}/"


def open_browser_and_listen(client_id, backend_url, timeout=180):
    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.server.full_path = self.path
            html = (
                "<html><body style='font-family: sans-serif; text-align:center; padding:30px;'>"
                "<h2>Sign-in complete</h2>"
                "<p>You can now close this tab. This window will attempt to close automatically.</p>"
                "<script>setTimeout(()=>{try{window.close();}catch(e){/*ignore*/}},1200);</script>"
                "</body></html>"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            # shutdown safely
            def _shutdown():
                try:
                    self.server.shutdown()
                except Exception:
                    pass
            threading.Thread(target=_shutdown, daemon=True).start()

        def log_message(self, format, *args):
            return

    try:
        httpd = HTTPServer(("localhost", PORT), OAuthHandler)
    except OSError as e:
        raise RuntimeError(f"Failed to bind to localhost:{PORT} — maybe the port is in use. ({e})")

    # ask the launcher lib for the login url
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(client_id, REDIRECT_URI)

    # run server in background
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    webbrowser.open(login_url, new=2)

    start = time.time()
    while getattr(httpd, "full_path", None) is None:
        if time.time() - start > timeout:
            try:
                httpd.shutdown()
            except Exception:
                pass
            raise TimeoutError("Timed out waiting for browser redirect. Did you complete sign-in in the browser?")
        time.sleep(0.2)

    full_received_url = f"{REDIRECT_URI.rstrip('/')}{httpd.full_path}"
    try:
        httpd.server_close()
    except Exception:
        pass
    server_thread.join(timeout=1)

    # validate auth code and state
    auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(full_received_url, state)

    # hand off to your backend to finish exchange
    resp = requests.post(f"{backend_url}/complete_login", json={
        "auth_code": auth_code,
        "code_verifier": code_verifier
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()

def Authenticate(tk_root, on_done, timeout=180):
    def worker():
        try:
            info = open_browser_and_listen(client, backend, timeout=timeout)
            # schedule callback on main thread
            tk_root.after(0, lambda: on_done(info, None))
        except Exception as e:
            tk_root.after(0, lambda: on_done(None, e))
    threading.Thread(target=worker, daemon=True).start()
