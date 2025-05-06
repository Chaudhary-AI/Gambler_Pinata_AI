import time
from pathlib import Path
import sys
import logging
from threading import Lock

# Add the correct path to the chroma_brain module dynamically
sys.path.append(str(Path(__file__).resolve().parent / "scripts"))

try:
    from chroma_brain import feed_code_file
except ImportError:
    feed_code_file = None
    print("[Warning] 'chroma_brain' module not found. Using mock function. Please ensure it is installed.")

if feed_code_file is None:
    def feed_code_file(file, label=None):
        print(f"[Mock] Processing file: {file} with label: {label}")

# Configurable watch directory
WATCH_DIR = Path.home() / "1man.army" / "intel_drop"
PROCESSED_LOG = WATCH_DIR / ".ingested.log"
WATCH_EXT = [".py", ".html", ".bat", ".txt"]

WATCH_DIR.mkdir(parents=True, exist_ok=True)
log_lock = Lock()

logging.basicConfig(
    filename=WATCH_DIR / "auto_ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_ingested():
    return set(open(PROCESSED_LOG).read().splitlines()) if PROCESSED_LOG.exists() else set()

def mark_ingested(path):
    with log_lock:
        with open(PROCESSED_LOG, "a") as f:
            f.write(f"{str(path)}\n")

def process_file(file, retries=3):
    for attempt in range(retries):
        try:
            feed_code_file(file, label=file.stem)
            mark_ingested(file)
            print(f"[+] Ingested: {file.name}")
            return
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed for {file}: {e}")
    logging.error(f"Failed to process {file} after {retries} attempts.")

def watch_and_ingest():
    print(f"[🧠] Watching {WATCH_DIR} for new files...")
    seen = get_ingested()
    try:
        while True:
            for file in WATCH_DIR.glob("*"):
                if file.suffix in WATCH_EXT and str(file) not in seen:
                    process_file(file)
                    seen.add(str(file))
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[🛑] Stopping watcher...")

if __name__ == "__main__":
    watch_and_ingest()