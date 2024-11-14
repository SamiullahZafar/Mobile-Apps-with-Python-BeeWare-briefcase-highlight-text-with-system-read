import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Function to run the HTTP server in a separate thread
def run_http_server():
    # Change to the directory where 'index.html' is located (same directory as app.py)
    folder_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
    os.chdir(folder_path)  # Change to the directory containing app.py and index.html

    # Print the current directory to verify it's correct
    print("Current working directory:", os.getcwd())  # Should print the directory where app.py is located

    # Set up and start the HTTP server
    server = HTTPServer(('0.0.0.0', 5000), SimpleHTTPRequestHandler)
    print("HTTP server running on http://127.0.0.1:5000/")
    server.serve_forever()

# Toga App Class
class TTSHighlighterApp(toga.App):
    def startup(self):
        # Create a box to hold the WebView
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Create the WebView to load the HTML file served by the HTTP server
        webview = toga.WebView(style=Pack(flex=1))

        # Specify the URL of the HTTP server
        file_url = 'http://127.0.0.1:5000/index.html'  # Correct URL for serving index.html

        # Set the WebView URL to point to the local HTTP server
        webview.url = file_url

        # Add the WebView to the main box
        main_box.add(webview)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

# Main function to start both Toga and the HTTP server
def main():
    # Start the HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True  # Ensure the HTTP server stops when the Toga app exits
    http_thread.start()

    # Wait a bit to ensure the HTTP server is up before starting the Toga app
    time.sleep(2)  # Allow the HTTP server to start up before launching the Toga app

    # Run the Toga app
    return TTSHighlighterApp("TTS Highlighter", "dev.ihh")

if __name__ == "__main__":
    main().main_loop()
