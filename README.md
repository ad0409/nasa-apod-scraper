# NASA APOD Scraper 🚀

This project automates the download of NASA's Astronomy Picture of the Day (APOD) and overlays its scientific explanation as text on the image. Designed for Windows, it supports automation via the Windows Task Scheduler.

## Example Output

![Example Output](assets/example-output-image.jpg)

[Check original APOD post here](https://apod.nasa.gov/apod/ap250607.html)

## Features ✨

- Fetches daily images from NASA's APOD API
- Adds scientific explanation as text overlay
- Automatically scales text based on image size
- Comprehensive error handling and logging
- Full type hints for code reliability

## Prerequisites 📋

Ensure the following tools are installed on your system:

- **Python 3.12 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **uv**: Open Microsoft PowerShell (press `Win + X`, then `i`) or your preferred IDE terminal, and run:
  ```powershell
  winget install --id=astral-sh.uv -e
  ```

### Need Help Setting Up?

Follow these tutorials to set up the prerequisites:
- [Installing Python on Windows](https://docs.python.org/3/using/windows.html)
- [Installing Git on Windows](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Getting Started with uv](https://docs.astral.sh/uv/getting-started/)

## Setting Up the Project 🔧

1. **Clone the Repository**:
   Open Microsoft PowerShell (press `Win + X`, then `i`) or your preferred IDE terminal, and run:
   ```powershell
   git clone https://github.com/ad0409/nasa-apod-scraper.git
   cd nasa-apod-scraper
   ```

2. **Pin Python Version**:
   Ensure the project uses the correct Python version:
   ```powershell
   uv python pin 3.12
   ```

3. **Install Dependencies**:
   Sync the project dependencies:
   ```powershell
   uv sync
   ```

4. **Configure Environment**:
   - Copy the example environment file:
     ```powershell
     copy .env.example .env
     ```
   - Open the `.env` file in a text editor:
     ```powershell
     notepad .env
     ```
   - Edit the file with your settings (e.g., NASA API key). Example configuration:
     ```env
     # Required settings
     NASA_APOD_API_KEY=your_api_key_here
     WINDOWS_SAVE_DIR=C:\Users\YourUsername\Pictures\APOD

     # Optional settings
     LOG_FILE_PATH=C:\Users\YourUsername\Documents\dev\nasa-apod-scraper\logs.txt  # defaults to ./logs.txt
     ```
   - Hit **Save** and exit the editor.

5. **Prepare the Batch File**:
   - Copy the example batch file:
     ```powershell
     copy run_main.bat.example run_main.bat
     ```
   - Open the `run_main.bat` file in a text editor and change the directory to the project root path you set previously.
   - Save and close the file.

6. **Run the Script**:
   Execute the script using:
   ```powershell
   uv run main.py
   ```

## Setting Up Windows Background 🎨

To use the downloaded images as your desktop wallpaper, follow these steps:

1. **Open Windows Personalization Settings**:
   - Right-click on the desktop and select **Personalize**.

2. **Set Background to Slideshow**:
   - Under the **Background** section, select **Slideshow** from the dropdown menu.

3. **Choose the Folder**:
   - Click **Browse** and navigate to the folder where the images are saved (e.g., `C:\Users\YourUsername\Pictures\APOD`).

4. **Adjust Slideshow Settings**:
   - Set the time interval for changing wallpapers (e.g., every 1 minute).
   - Enable **Shuffle** to randomize the wallpapers.

5. **Save Settings**:
   - Close the settings window, and your desktop will now display the downloaded images as a slideshow.

## Automating with Windows Task Scheduler 🕒

To automate the script execution daily, follow these steps:

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and press Enter.

2. **Create a New Task**:
   - Click **Create Task**.
   - Under the **General** tab, provide a name (e.g., `NASA APOD Scraper`) and select **Run with highest privileges**.

3. **Set the Trigger**:
   - Go to the **Triggers** tab and click **New**.
   - Set the task to run daily at your preferred time.

4. **Set the Action**:
   - Go to the **Actions** tab and click **New**.
   - Select **Start a program** and browse to the `run_main.bat` file.

5. **Save and Test**:
   - Save the task and test it by right-clicking the task and selecting **Run**.

## Project Structure 📁

```
nasa-apod-scraper/
├── .env.example          # Template for environment variables
├── pyproject.toml        # Project metadata and dependencies
├── main.py               # Main script
├── run_main.bat.example  # Example batch file for automation
└── logs.txt              # Log file (created on first run)
```

## Development 🛠️

This project uses:
- Modern Python packaging with `pyproject.toml`
- `uv` package manager for deterministic builds
- Type hints and docstrings throughout
- Comprehensive error handling and logging

### Error Handling
The script handles:
- Missing/invalid environment variables
- API request failures
- Non-image media types
- Image processing errors
- File system operations

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [NASA APOD API](https://api.nasa.gov/) for the amazing space images
- [Pillow](https://python-pillow.org/) for image processing
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment management
- [uv](https://github.com/astral-sh/uv) for modern Python packaging