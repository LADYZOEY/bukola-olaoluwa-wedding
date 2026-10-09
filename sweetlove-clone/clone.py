#!/usr/bin/env python3
"""
Universal Multi-Threaded Website Cloner
Downloads all pages from a target website and sets up clean URL structure.
"""

import os
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# 1. Target live domain
BASE_URL = "https://sweetlove-theme.thedigitalinvite.com"

# 2. Local output folder
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))

# 3. List of paths to clone (homepage is empty string "")
PAGES = [
    "",
]

# Browser headers to avoid 403 blocks
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def download_page(slug):
    url = f"{BASE_URL}/{slug}" if slug else BASE_URL
    print(f"[FETCHING] {url}")
    
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read()
            
            if not slug:
                # Root homepage
                out_file = os.path.join(TARGET_DIR, "index.html")
                with open(out_file, "wb") as f:
                    f.write(content)
            else:
                # Direct slug file: /about.html
                direct_file = os.path.join(TARGET_DIR, f"{slug}.html")
                os.makedirs(os.path.dirname(direct_file), exist_ok=True)
                with open(direct_file, "wb") as f:
                    f.write(content)
                
                # Folder structure: /about/index.html (for clean URLs)
                folder_target = os.path.join(TARGET_DIR, slug, "index.html")
                os.makedirs(os.path.dirname(folder_target), exist_ok=True)
                with open(folder_target, "wb") as f:
                    f.write(content)
                    
            print(f"[SAVED] {slug or 'index'} ({len(content)} bytes)")
    except Exception as err:
        print(f"[ERROR] Failed {url}: {err}")

KNOWN_ASSETS = [
    "/assets/index-qUp0T8yC.js",
    "/assets/index-CMJN1tNq.css",
    "/assets/birds_element-BnyCdFr7.png",
    "/assets/event-details-bg-CdaGzDti.png",
    "/lovable-uploads/045cc358-eb6d-442f-8cae-b0e16c78d69c.png",
    "/music/love-letters.mp3",
    "/__l5e/assets-v1/ca6688e9-16bc-42a6-b3b8-9ad34e0de031/intro.mp4",
    "/hero-cake.mp4",
    "/~flock.js"
]

def download_asset(asset_path):
    url = f"{BASE_URL}{asset_path}"
    out_path = os.path.join(TARGET_DIR, asset_path.lstrip("/"))
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"[EXISTS] {asset_path}")
        return
    print(f"[FETCHING ASSET] {url}")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": BASE_URL,
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"[SAVED ASSET] {asset_path} ({len(data)} bytes)")
    except Exception as err:
        print(f"[ERROR ASSET] {asset_path}: {err}")

def main():
    print(f"Starting clone for {len(PAGES)} pages from {BASE_URL}...")
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(download_page, PAGES)
    
    print("Downloading known core assets...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_asset, KNOWN_ASSETS)
    print("All pages & core assets downloaded successfully.")

if __name__ == "__main__":
    main()
