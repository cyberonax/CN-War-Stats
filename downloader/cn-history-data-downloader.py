import requests
import os
from datetime import datetime
from pathlib import Path

# -----------------------
# CONFIGURATION
# -----------------------
BASE_URL = "https://www.cybernations.net/assets/CyberNations_SE_War_Stats_"
ZIP_IDS = ["525001", "525002"]

# Directory that is tracked by your repository (e.g., "downloaded_zips" inside your repo)
LOCAL_DIR = Path("./downloaded_zips")
LOCAL_DIR.mkdir(exist_ok=True)

# -----------------------
# HELPER FUNCTIONS
# -----------------------
def construct_url(date_obj, zip_id):
    """Construct the URL with the date and zip id."""
    date_str = f"{date_obj.month}{date_obj.day}{date_obj.year}"
    return f"{BASE_URL}{date_str}{zip_id}.zip"

def file_already_in_repo(file_name):
    """Check if the file already exists in the designated directory."""
    file_path = LOCAL_DIR / file_name
    return file_path.exists()

def download_zip(url, save_path):
    """Download the zip file and save it to the specified path."""
    try:
        print(f"Attempting to download from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if the download fails
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded successfully: {save_path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False

# -----------------------
# MAIN EXECUTION (Single Run)
# -----------------------
def main():
    now = datetime.now()
    for zip_id in ZIP_IDS:
        url = construct_url(now, zip_id)
        file_name = url.split("/")[-1]  # Extract filename from the URL
        local_path = LOCAL_DIR / file_name

        if file_already_in_repo(file_name):
            print(f"File already exists in the repository: {file_name}")
            continue

        if download_zip(url, local_path):
            print(f"Saved file: {local_path}")
        else:
            print(f"No file downloaded for: {file_name}")

if __name__ == '__main__':
    main()
