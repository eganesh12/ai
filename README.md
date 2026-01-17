# PulsePoint AI

PulsePoint AI is a platform designed to process long-form video content, making it accessible and engaging for modern audiences. By leveraging Generative AI and multimodal models, PulsePoint AI automatically identifies key moments in videos, converts video formats, and generates dynamic captions, transforming lengthy sessions into shareable content.

## Features

- **Emotional Peaks Detection**: Automatically identifies high-energy or profound moments in videos using audio analysis and sentiment detection.
- **Smart-Crop to Vertical**: Tracks the speaker's face to ensure they remain centered when converting horizontal videos to vertical formats (9:16).
- **Dynamic Captions Generation**: Creates engaging, timed overlays and catchy headlines to enhance viewer engagement.

## Project Structure

```
pulsepoint-ai
├── src
│   ├── app.py                  # Main entry point for the FastAPI application
│   ├── audio_analysis.py        # Functions for analyzing audio tracks and detecting emotional peaks
│   ├── transcription.py         # Handles transcription of audio to text for karaoke-style captions
│   ├── sentiment_analysis.py     # Analyzes sentiment of transcribed text to identify impactful moments
│   ├── face_detection.py        # Implements face detection to keep the speaker centered in videos
│   └── hook_generation.py       # Generates catchy headlines to enhance shareability
├── requirements.txt             # Lists project dependencies
├── .gitignore                   # Specifies files to ignore in version control
└── README.md                    # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pulsepoint-ai
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```
   uvicorn src.app:app --reload
   ```

## Submission Requirements

- Submit a link to your public GitHub repository on the Unstop portal.
- Include a screen recording video of your live working project in this README.

## License

This project is licensed under the MIT License. See the LICENSE file for details.