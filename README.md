# MediScript: Advanced Prescription Analyzer

![MediScript Banner](https://img.shields.io/badge/MediScript-Prescription%20Analyzer-blue?style=for-the-badge)

An advanced application that uses image processing techniques and Google's Gemini AI to accurately extract information from medical prescriptions.

## 🌟 Features

- **Advanced Image Processing**: Multi-step image enhancement for improved text readability
- **AI-Powered Extraction**: Uses Gemini-1.5-flash for accurate text recognition and information extraction
- **Structured Output**: Extracts patient information, medications, dosages, and usage instructions
- **User-Friendly Interface**: Beautiful Streamlit UI with intuitive design
- **Visualized Processing**: See each step of the image enhancement pipeline
- **Tabular Data View**: View extracted information in clean, organized tables
- **Export Options**: Download results in JSON and CSV formats
- **Sample Prescriptions**: Try the app with included sample images

## 📋 Prerequisites

- Python 3.9+
- Google Gemini API key
- Optional: Ngrok authentication token (for public sharing)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mediscript-prescription-parser.git
   cd mediscript-prescription-parser
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   NGROK_AUTH_TOKEN=your_ngrok_auth_token_here  # Optional
   ```

## 🏃‍♂️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## 📦 Project Structure

```
prescription_parser/
│
├── app.py                      # Main Streamlit application
├── .env                        # Environment variables (API keys)
├── .env.example                # Example environment file (for GitHub)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Project dependencies
│
├── modules/
│   ├── __init__.py             # Makes the directory a package
│   ├── image_processor.py      # Image enhancement functions
│   ├── prescription_parser.py  # AI-based text extraction
│   └── utils.py                # Utility functions
│
├── assets/
│   ├── styles.css              # Custom CSS for UI
│   ├── logo.png                # App logo
│   └── sample_images/          # Sample prescription images
│       ├── sample1.jpg
│       ├── sample2.jpg
│       └── sample3.jpg
│
└── README.md                   # Project documentation
```

## 🖼️ Image Processing Pipeline

The application enhances prescription images using a multi-step processing pipeline:

1. **Resize**: Ensures the image has an optimal size for processing
2. **Grayscale Conversion**: Converts the image to grayscale
3. **Adaptive Thresholding**: Applies adaptive threshold to handle uneven lighting
4. **Noise Reduction**: Reduces noise while preserving text details
5. **Edge Enhancement**: Sharpens text boundaries for better readability
6. **Contrast Enhancement**: Improves text-to-background contrast

## 🧠 AI Analysis

The enhanced image is sent to Google's Gemini AI with specific prompts to extract:

- Patient name and details
- Prescription date
- Medication names
- Dosage information
- Usage instructions
- Refill information

## 📊 Data Output

The extracted information is presented in multiple formats:

- Structured tables within the application
- Downloadable JSON file with complete extraction results
- CSV exports for patient information and medications

## 🔒 Privacy & Security

- All processing happens on your local machine
- No prescription data is stored or shared with any external services except Google's Gemini API
- API keys are stored securely in your local `.env` file

## ⚠️ Disclaimer

This application is intended for educational and demonstration purposes only. It should not replace professional medical advice or services. Always consult healthcare professionals for medical guidance.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Google Gemini AI for text extraction capabilities
- Streamlit for the web application framework
- OpenCV for image processing functionalities
