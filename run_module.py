

import argparse
import threading
import subprocess
import sys
import time
import webview
from pathlib import Path
import os

# Sicherstellen dass das Projektverzeichnis im Pfad ist
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"[Launcher] Added project path to sys.path: {project_root}")


os.chdir(project_root)


def close_server(port=8501):
    """Beendet Streamlit-Server auf Port"""
    # lsof -ti:8501
    p1 = subprocess.Popen(["lsof", "-ti", f":{port}"], stdout=subprocess.PIPE)
    # xargs kill -9
    p2 = subprocess.Popen(["xargs", "kill", "-9"], stdin=p1.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.stdout.close()

    out, err = p2.communicate()
    if p2.returncode != 0:
        print(f"Error stopping server: {err.decode().strip()}")
    else:
        print(f"Server on port {port} stopped successfully.")


def start_streamlit(streamlit_file: str, streamlit_port: int = 8501) -> None:
    """Starts Streamlit in the background"""
    print("🚀 Starting Streamlit Server...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", streamlit_file,
        "--server.headless", "true",
        "--server.port", str(streamlit_port),
        "--browser.gatherUsageStats", "false"])


def on_closed(port=8501):
    """Callback function when the GUI window is closed"""
    print("❌ GUI window closed. Stopping Streamlit...")
    # Beende Streamlit Prozess
    close_server(port)


def create_gui_window(window_title: str,
                      url: str,
                      width: int = 400,
                      height: int = 800,
                      on_top: bool = True,
                      resizable: bool = True,
                      on_closed_func: callable = None,
                      port: int = 8501):
    """Creates a GUI window with an integrated browser"""
    print("⏳ Waiting for Streamlit Server...")
    time.sleep(3)
    print("🖥️ Opening GUI window...")

    main_window = webview.create_window(
        window_title,
        url,
        width=width,
        height=height,
        on_top=on_top,
        resizable=resizable,
        fullscreen=False,
    )

    if on_closed_func:
        main_window.events.closed += lambda: on_closed_func(port)

    webview.start()


def main(streamlit_file: str, streamlit_port: int, window_title: str, url: str, width: int, height: int, on_top: bool, resizable: bool):
    """Main function to start Streamlit and the GUI window. Streamlit will be started in a separate thread, while the GUI runs in the main thread."""
    on_closed_func = None
    if streamlit_file and streamlit_port:
        # streamlit will be started in a separate thread
        # pywebview demands to run in the main thread
        streamlit_thread = threading.Thread(target=start_streamlit, args=(
            streamlit_file, streamlit_port), daemon=True)
        streamlit_thread.start()
        on_closed_func = on_closed
        url = f"http://localhost:{streamlit_port}"

    # pywebview in main thread
    create_gui_window(window_title, url, width, height, on_top,
                      resizable, on_closed_func=on_closed_func, port=streamlit_port)


def cli():
    """Parses command line arguments and starts the application. Useful for development and debugging."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--streamlit_file", default=None)
    parser.add_argument("--streamlit_port", type=int, default=8501)
    parser.add_argument("--window_title", default="StaabTools")
    parser.add_argument("--url", default="")
    parser.add_argument("--width", type=int, default=400)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--on_top", default="true")
    parser.add_argument("--resizable", default="true")
    args, _ = parser.parse_known_args()
    if args:
        main(
            streamlit_file=args.streamlit_file,
            streamlit_port=args.streamlit_port,
            window_title=args.window_title,
            url=args.url,
            width=args.width,
            height=args.height,
            on_top=args.on_top.lower() == "true",
            resizable=args.resizable.lower() == "true",
        )


if __name__ == "__main__":
    cli()
