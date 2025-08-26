"""
An application that downloads the current NASA astronomic picture of the day (APOD)
and adds its explanation as text overlay for use as a wallpaper.
"""

from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
import os
import subprocess
import logging

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- Constants ---
TEMP_SAVE_DIR_WSL = Path("/tmp/apod-nasa")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LOG_FILE = os.getenv("LOG_FILE_PATH")
if not LOG_FILE:
    LOG_FILE = str(Path(__file__).parent / "logs.txt")
# --- Logging Setup ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
logging.info("Script started.")

BASE_URL: str = "https://api.nasa.gov/planetary/apod?"

def load_config() -> Tuple[str, Path]:
    """
    Load environment variables and return API key and Windows save directory.
    
    Returns:
        Tuple[str, Path]: The NASA APOD API key and Windows save directory path
        
    Raises:
        ValueError: If required environment variables are not set.
    """
    load_dotenv()
    api_key: Optional[str] = os.getenv('NASA_APOD_API_KEY')
    windows_save_dir: Optional[str] = os.getenv('WINDOWS_SAVE_DIR')

    if not api_key:
        logging.error("NASA_APOD_API_KEY is not set. Please check your .env file.")
        raise ValueError("NASA_APOD_API_KEY is not set. Please check your .env file.")
    if not windows_save_dir:
        logging.error("WINDOWS_SAVE_DIR is not set. Please check your .env file.")
        raise ValueError("WINDOWS_SAVE_DIR is not set. Please check your .env file.")

    return api_key, Path(windows_save_dir)

def get_api_response(api_key: str) -> requests.Response:
    """
    Request APOD data from NASA API.

    Args:
        api_key (str): NASA API key for authentication.

    Returns:
        requests.Response: Response from the NASA APOD API.

    Raises:
        requests.RequestException: If the API request fails.
    """
    url: str = f"{BASE_URL}api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise

def process_data(response: requests.Response) -> Tuple[str, Optional[requests.Response], Optional[str], Optional[str]]:
    """
    Extract image URL and explanation text from API response.

    Args:
        response (requests.Response): Response from NASA APOD API.

    Returns:
        Tuple containing:
            - str: Filename extracted from the URL
            - Optional[requests.Response]: Response from image download request
            - Optional[str]: Explanation text for the image
            - Optional[str]: Media type of the APOD (e.g., "image", "video")
    """
    data = response.json()
    media_type: Optional[str] = data.get("media_type")
    hd_image_url: Optional[str] = data.get("hdurl")
    image_explanation_text: Optional[str] = data.get("explanation")

    filename: str = ""
    image_response: Optional[requests.Response] = None

    if media_type != "image":
        logging.info(f"Media type is '{media_type}'. No image to process.")
        return "", None, image_explanation_text, media_type

    if hd_image_url:
        filename = urlparse(hd_image_url).path.split("/")[-1]
        try:
            image_response = requests.get(hd_image_url)
            image_response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Image download failed: {e}")
            image_response = None

    return filename, image_response, image_explanation_text, media_type

def temp_save_to_wsl(filename: str, image_response: Optional[requests.Response]) -> Path:
    """
    Parse fetched content into an image file and save it.
    
    Args:
        filename (str): Name of the file to save
        image_response (Optional[requests.Response]): Response containing the image data
        
    Returns:
        Path: Path to the saved temporary file
        
    Raises:
        IOError: If there's an error writing the file
    """
    if not image_response:
        logging.error("No image response provided")
        raise ValueError("No image response provided")

    TEMP_SAVE_DIR_WSL.mkdir(parents=True, exist_ok=True)
    temp_save_path_wsl = TEMP_SAVE_DIR_WSL / filename

    with open(temp_save_path_wsl, "wb") as image_file:
        image_file.write(image_response.content)
    logging.info(f"Image downloaded temporarily to WSL: {temp_save_path_wsl}")

    return temp_save_path_wsl

def add_image_explanation_text(temp_save_path_wsl: Path, image_explanation_text: Optional[str]) -> Path:
    """
    Open an image, add wrapped explanation text to the bottom left, and save it.
    
    Args:
        temp_save_path_wsl (Path): Path to the image file
        image_explanation_text (Optional[str]): Text to add to the image, if any
        
    Returns:
        Path: Path to the modified image
        
    Raises:
        FileNotFoundError: If the image file is not found
        IOError: If there's an error processing the image
    """
    try:
        image = Image.open(temp_save_path_wsl)

        if not image_explanation_text:
            return temp_save_path_wsl

        draw = ImageDraw.Draw(image)
        img_width, img_height = image.size
        text_color = (255, 255, 255)
        font_size = int(img_height / 60)
        font = ImageFont.truetype(FONT_PATH, font_size)
        max_text_width = int(img_width * 0.5)
        chars_per_line = max_text_width // (font_size // 2) if font_size > 0 else 80
        wrapped_text = textwrap.fill(image_explanation_text, width=chars_per_line)
        padding = 20
        text_bbox = draw.textbbox((0,0), wrapped_text, font=font)
        text_height = text_bbox[3] - text_bbox[1]
        x_position = padding
        y_position = max(0, img_height - text_height - padding)
        draw.multiline_text((x_position, y_position), wrapped_text, fill=text_color, font=font)
        image.save(temp_save_path_wsl)
        logging.info(f"Explanation text added and saved to: {temp_save_path_wsl}")
        return temp_save_path_wsl
    except FileNotFoundError:
        logging.error(f"Image file not found at {temp_save_path_wsl}")
        raise
    except Exception as e:
        logging.error(f"Error adding text to image: {e}")
        raise

def move_image_from_wsl_to_windows(filename: str, temp_save_path_wsl: Path, windows_save_dir: Path) -> None:
    """
    Move the processed image from WSL to Windows filesystem.
    
    Args:
        filename (str): Name of the file to move
        temp_save_path_wsl (Path): Current path of the file in WSL
        windows_save_dir (Path): Windows directory path to save the file to
        
    Raises:
        subprocess.CalledProcessError: If a shell command fails
        IOError: If there's an error copying the file
    """
    windows_save_path = windows_save_dir / filename
    windows_save_dir_wsl_format = subprocess.run(
        ["wslpath", "-u", str(windows_save_dir)],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()
    windows_save_path_wsl_format = subprocess.run(
        ["wslpath", "-u", str(windows_save_path)],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()
    create_dir_command = f"mkdir -p '{windows_save_dir_wsl_format}'"
    copy_command = f"cp '{temp_save_path_wsl}' '{windows_save_path_wsl_format}'"
    try:
        subprocess.run(create_dir_command, shell=True, check=True, capture_output=True)
        logging.info(f"Created Windows directory: {windows_save_dir}")
        subprocess.run(copy_command, shell=True, check=True, capture_output=True)
        logging.info(f"Copied image to Windows: {windows_save_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Shell command failed: {e}\nOutput: {e.stdout}\nError: {e.stderr}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

def main() -> None:
    """
    Main execution function that orchestrates the APOD image processing workflow.
    
    Raises:
        ValueError: If required environment variables are missing
        requests.RequestException: If API requests fail
        IOError: If there are file operation errors
    """
    try:
        api_key, windows_save_dir = load_config()
        api_response = get_api_response(api_key)
        if api_response.status_code != 200:
            logging.error(f"NASA APOD API request failed with status code {api_response.status_code}: {api_response.text}")
            return
        filename, image_response, image_explanation_text, media_type = process_data(api_response)
        if media_type != "image":
            logging.info(f"Media type is '{media_type}'. No image to process. Exiting cleanly.")
            return
        if not filename or not image_response:
            logging.warning("Failed to get required image data from NASA APOD API. Skipping image processing.")
            return
        temp_wsl_image_path = temp_save_to_wsl(filename, image_response)
        processed_image_path = add_image_explanation_text(temp_wsl_image_path, image_explanation_text)
        move_image_from_wsl_to_windows(filename, processed_image_path, windows_save_dir)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
