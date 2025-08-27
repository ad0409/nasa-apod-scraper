"""
NASA APOD Scraper: A script to fetch and process NASA's Astronomy Picture of the Day.
"""

import logging
import os
import textwrap
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = os.getenv("FONT_PATH", "C:\\Windows\\Fonts\\Arial.ttf")
LOG_FILE = os.getenv(
    "LOG_FILE_PATH", str(Path(__file__).parent / "logs.txt")
)
INITIAL_FONT_SIZE = 20  # Initial font size for explanation text
MIN_FONT_SIZE = 10  # Minimum font size for explanation text

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
    api_key: Optional[str] = os.getenv("NASA_APOD_API_KEY")
    windows_save_dir: Optional[str] = os.getenv("WINDOWS_SAVE_DIR")

    if not api_key:
        raise ValueError(
            "NASA_APOD_API_KEY is not set. Please check your .env file or environment variables."
        )
    if not windows_save_dir:
        raise ValueError(
            "WINDOWS_SAVE_DIR is not set. Please check your .env file or environment variables."
        )

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
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error("API request failed: %s", e)
        raise

def process_data(
    response: requests.Response
) -> Tuple[Optional[str], Optional[requests.Response], Optional[str], Optional[str]]:
    """
    Extract image URL and explanation text from API response.

    Args:
        response (requests.Response): Response from NASA APOD API.

    Returns:
        Tuple containing:
            - Optional[str]: Filename extracted from the URL
            - Optional[requests.Response]: Response from image download request
            - Optional[str]: Explanation text for the image
            - Optional[str]: Media type of the APOD (e.g., "image", "video")
    """
    data = response.json()
    media_type: Optional[str] = data.get("media_type")
    hd_image_url: Optional[str] = data.get("hdurl")
    image_explanation_text: Optional[str] = data.get("explanation")

    if media_type != "image":
        logging.info("Media type is '%s'. No image to process.", media_type)
        return None, None, image_explanation_text, media_type

    filename = (
        urlparse(hd_image_url).path.split("/")[-1] if hd_image_url else None
    )
    image_response = None

    if hd_image_url:
        try:
            image_response = requests.get(hd_image_url, timeout=10)
            image_response.raise_for_status()
        except requests.RequestException as e:
            logging.error("Image download failed: %s", e)

    return filename, image_response, image_explanation_text, media_type

def save_image_to_windows(
    filename: str, image_response: requests.Response, windows_save_dir: Path
) -> Path:
    """
    Save fetched image content directly to Windows directory.

    Args:
        filename (str): Name of the file to save
        image_response (requests.Response): Response containing the image data
        windows_save_dir (Path): Windows directory path to save the file

    Returns:
        Path: Path to the saved file

    Raises:
        ValueError: If image_response is None
        IOError: If there's an error writing the file
    """
    if not image_response:
        raise ValueError("No image response provided")

    windows_save_dir.mkdir(parents=True, exist_ok=True)
    save_path = windows_save_dir / filename

    with open(save_path, "wb") as image_file:
        image_file.write(image_response.content)

    logging.info("Image downloaded to Windows: %s", save_path)
    return save_path

def add_image_explanation_text(
    image_path: Path, image_explanation_text: Optional[str]
) -> Path:
    """
    Open an image, add wrapped explanation text to the bottom left quadrant, and save it.

    Args:
        image_path (Path): Path to the image file
        image_explanation_text (Optional[str]): Text to add to the image, if any

    Returns:
        Path: Path to the modified image

    Raises:
        FileNotFoundError: If the image file is not found
        IOError: If there's an error processing the image
    """
    try:
        image = Image.open(image_path)
        if not image_explanation_text:
            return image_path

        draw = ImageDraw.Draw(image)
        img_width, img_height = image.size

        # Define the bottom-left quadrant dimensions
        quadrant_width = img_width // 2
        quadrant_height = img_height // 2

        # Dynamically calculate font size to fit the text within the quadrant
        font_size = INITIAL_FONT_SIZE  # Use named constant for initial font size
        font = ImageFont.truetype(FONT_PATH, font_size)

        # Estimate average character width for the current font
        avg_char_width = font.getlength("A") if hasattr(font, "getlength") else 10
        wrapping_width = max(10, int(quadrant_width // avg_char_width))

        wrapped_text = textwrap.fill(image_explanation_text, width=wrapping_width)

        while font_size > MIN_FONT_SIZE:
            text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            if text_width <= quadrant_width and text_height <= quadrant_height:
                break

            font_size -= 1
            font = ImageFont.truetype(FONT_PATH, font_size)

        # Position the text within the bottom-left quadrant
        x_position = 20  # Padding from the left edge
        y_position = img_height - quadrant_height + 20  # Padding from the top of the quadrant

        draw.multiline_text(
            (x_position, y_position), wrapped_text, fill=(255, 255, 255), font=font
        )
        image.save(image_path)

        logging.info("Explanation text added and saved to: %s", image_path)
        return image_path
    except FileNotFoundError:
        logging.error("Image file not found at %s", image_path)
        raise
    except OSError as e:
        logging.error("Error adding text to image: %s", e)
        raise

def main() -> None:
    """
    Main execution function that orchestrates the APOD image processing workflow.
    """
    try:
        api_key, windows_save_dir = load_config()
        api_response = get_api_response(api_key)

        if api_response.status_code != 200:
            logging.error(
                "NASA APOD API request failed with status code %d", api_response.status_code
            )
            return

        filename, image_response, image_explanation_text, media_type = process_data(
            api_response
        )

        if media_type != "image" or not filename or not image_response:
            logging.info("No valid image data to process.")
            return

        image_path = save_image_to_windows(
            filename, image_response, windows_save_dir
        )
        add_image_explanation_text(image_path, image_explanation_text)
    except ValueError as ve:
        logging.error("Configuration error: %s", ve)
    except requests.RequestException as re:
        logging.error("API or image request error: %s", re)
    except OSError as oe:
        logging.error("File or image processing error: %s", oe)

if __name__ == "__main__":
    main()
