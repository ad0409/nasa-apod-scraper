# WSL2 Release v1.0.0

## About
NASA APOD Scraper downloads the Astronomy Picture of the Day, adds the explanation as text overlay, and saves it to your Windows directory - all from within WSL2.

## Features
- Automatic download of NASA's APOD
- Text overlay with image explanation
- WSL2 to Windows filesystem integration
- Robust error handling and logging
- Configurable via environment variables
- Skips non-image media types automatically

## Quick Start

1. Get your NASA API key from https://api.nasa.gov/

2. Setup:
   ```bash
   # Clone and enter directory
   git clone https://github.com/ad0409/NASA_APOD_Scraper.git
   cd NASA_APOD_Scraper

   # Setup environment
   cp .env.example .env
   nano .env  # Edit with your settings

   # Install dependencies using uv
   uv pip install .
   ```

3. Run:
   ```bash
   uv run main.py
   ```

## What's Included
- `.env.example` - Template for environment setup
- `pyproject.toml` - Project metadata and dependencies
- `README.md` - Detailed documentation
- Comprehensive logging system
- Error handling for all major cases

## Requirements
- WSL2 (Windows Subsystem for Linux 2)
- Python 3.12+
- NASA API key
- DejaVu Sans font (`sudo apt-get install fonts-dejavu`)
- uv package manager (`pip install uv`)
