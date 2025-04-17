import time
from pathlib import Path
import sys
import logging

# Add the correct path to the chroma_brain module
sys.path.append(r"C:\PROFESSOR JOHNNY'S FAMILY HOME SWEET\Gambler Pinata AI\scripts")

try:
    from chroma_brain import feed_code_file
except ImportError:
    feed_code_file = None
    print("[Warning] 'chroma_brain' module not found. Using mock function. Please ensure it is installed.")

if feed_code_file is None:
    def feed_code_file(file, label=None):
        print(f"[Mock] Processing file: {file} with label: {label}")

WATCH_DIR = Path.home() / "1man.army" / "intel_drop"
PROCESSED_LOG = WATCH_DIR / ".ingested.log"
WATCH_EXT = [".py", ".html", ".bat", ".txt"]

WATCH_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=WATCH_DIR / "auto_ingest.log", level=logging.INFO)

def get_ingested():
    return set(open(PROCESSED_LOG).read().splitlines()) if PROCESSED_LOG.exists() else set()

def mark_ingested(path):
    with open(PROCESSED_LOG, "a") as f: f.write(f"{str(path)}\n")

def watch_and_ingest():
    print(f"[🧠] Watching {WATCH_DIR} for new files...")
    seen = get_ingested()
    while True:
        for file in WATCH_DIR.glob("*"):
            if file.suffix in WATCH_EXT and str(file) not in seen:
                try:
                    feed_code_file(file, label=file.stem)
                    mark_ingested(file)
                    seen.add(str(file))
                    print(f"[+] Ingested: {file.name}")
                except Exception as e:
                    logging.warning(f"Failed: {file} | {e}")
        time.sleep(5)

if __name__ == "__main__":
    watch_and_ingest()