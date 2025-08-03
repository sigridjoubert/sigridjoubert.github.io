from builder.builder import Builder
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os
import sys

SITE_NAME = "Sigrid Joubert"
PORT = 8000
OUTPUT_DIR = "build"  # Change if your build output is elsewhere

if __name__ == "__main__":
    # Build the site
    builder = Builder(SITE_NAME)
    builder.build_site()

    # Check for "local" argument
    if "local" in sys.argv:
        os.chdir(OUTPUT_DIR)  # Change working dir to site output

        handler = SimpleHTTPRequestHandler
        httpd = TCPServer(("", PORT), handler)

        print(f"Serving '{SITE_NAME}' at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")
            httpd.server_close()

