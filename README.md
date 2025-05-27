# NASA APOD Scraper

This project is a Proof of Concept (POC) for downloading the NASA Astronomy Picture of the Day (APOD) and saving it to a specified directory.

## Setup

1.  Clone the repository.
2.  Install dependencies: `uv sync`
3.  Create a `.env` file in the project root with your NASA API key:
    ```
    NASA_APOD_API_KEY=YOUR_API_KEY
    ```
    You can obtain an API key from the [NASA API website](https://api.nasa.gov/).

## Usage

Run the script:
```bash
uv run main.py