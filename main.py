import os
import requests
from urllib.parse import urlparse


def download_nasa_image(api_key):
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        hd_image_url = data.get("hdurl")
        explanation_text = data.get("explanation")
        date = data.get("date")
        title = data.get("title")

        if hd_image_url:
            filename = urlparse(hd_image_url).path.split("/")[-1]
            image_response = requests.get(hd_image_url)
            save_dir = r"C:\Users\AD\Pictures\Screensaver\NASA APOD"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{filename}")

            with open(save_path, "wb") as image_file:
                image_file.write(image_response.content)

            print(f"Image downloaded and saved successfully. Saved as: {save_path}")
        else:
            print("HD Image URL not available for today.")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")


# Replace "DEMO_KEY" with your actual NASA API key
api_key = "DEMO_KEY"
download_nasa_image(api_key)
