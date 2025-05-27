"""
An application that downloads the current NASA astronomic picture of the day (APOD).
The picture can be i.e. processed afterwards to serve as a wallpaper.
"""

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
import subprocess
from pathlib import Path  # Import Path
from typing import Optional  # Import Optional

BASE_URL = "https://api.nasa.gov/planetary/apod?"


def load_config() -> str:
    """Load environment variables and return API key."""
    load_dotenv()
    api_key: Optional[str] = os.getenv("NASA_APOD_API_KEY")
    if not api_key:
        raise ValueError("NASA_APOD_API_KEY is not set. Please check your .env file.")
    return api_key


def get_APOD_data(api_key: str) -> requests.Response:
    url = f"{BASE_URL}api_key={api_key}"
    """Request APOD response from API."""
    response = requests.get(url)
    response.raise_for_status()
    return response


def process_data(response: requests.Response) -> None:
    """Strip dedicated datasets from API response and save to Windows path."""
    data = response.json()
    hd_image_url: Optional[str] = data.get("hdurl")

    if hd_image_url:
        # Extract filename from the URL
        filename: str = urlparse(hd_image_url).path.split("/")[-1]
        image_response = requests.get(hd_image_url)

        # Define temporary save directory in WSL using pathlib
        temp_save_dir_wsl = Path("/tmp/apod-nasa")
        temp_save_dir_wsl.mkdir(parents=True, exist_ok=True)
        temp_save_path_wsl = temp_save_dir_wsl / filename

        # Save the image temporarily in WSL
        with open(temp_save_path_wsl, "wb") as image_file:
            image_file.write(image_response.content)
        print(f"Image downloaded temporarily to WSL: {temp_save_path_wsl}")

        # Define the target Windows path using pathlib
        windows_save_dir = Path(r"C:\Users\AD\Pictures\Screensaver\apod-nasa")
        windows_save_path = windows_save_dir / filename

        # Use a shell command to create the directory and copy the file
        # Ensure the target directory exists on the Windows side via WSL
        # Convert Windows path to WSL path format for shell command
        windows_save_dir_wsl_format = subprocess.run(
            ["wslpath", "-u", str(windows_save_dir)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        windows_save_path_wsl_format = subprocess.run(
            ["wslpath", "-u", str(windows_save_path)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        create_dir_command = f"mkdir -p '{windows_save_dir_wsl_format}'"
        copy_command = f"cp '{temp_save_path_wsl}' '{windows_save_path_wsl_format}'"

        try:
            # Create the target directory on the Windows side via WSL
            subprocess.run(
                create_dir_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"Ensured Windows target directory exists: {windows_save_dir}")

            # Copy the file from WSL temp to Windows target
            subprocess.run(
                copy_command, shell=True, check=True, capture_output=True, text=True
            )
            print(f"Image copied to Windows: {windows_save_path}")

            # Optional: Clean up the temporary file in WSL
            # os.remove(temp_save_path_wsl)
            # print(f"Removed temporary WSL file: {temp_save_path_wsl}")

        except subprocess.CalledProcessError as e:
            print(f"Error executing shell command: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    else:
        print("HD Image URL not available for today.")


def main() -> None:
    api_key = load_config()
    response = get_APOD_data(api_key)
    process_data(response)


if __name__ == "__main__":
    main()
