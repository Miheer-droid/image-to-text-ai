---
title: Image to Text AI
emoji: 🖼️
colorFrom: blue
colorTo: green
sdk: gradio
app_file: main.py
pinned: false
---
# 🖼️ Image to Text AI 📝

This is a simple web application that uses Google's Gemini AI model to analyze images. It provides a detailed description, identifies potential real-world locations, and estimates the likelihood of the image being AI-generated.

## ✨ Features

-   **Detailed Descriptions:** Get a rich, paragraph-long description of any uploaded image.
-   **Location Identification:** Recognizes famous landmarks and natural wonders.
-   **AI-Generated Detection:** Provides a percentage estimate of the likelihood an image is AI-generated.
-   **Safety First:** Automatically blocks and refuses to analyze inappropriate (NSFW) content.
-   **Responsive UI:** Works on both desktop and mobile browsers.

## 🚀 How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Miheer-droid/image-to-text-ai.git
    cd image-to-text-ai
    ```

2.  **Install Dependencies**
    Make sure you have Python 3.8+ installed. Then, install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Your API Key**
    -   Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    -   Create a file named `.env` in the project folder.
    -   Add your key to the `.env` file like this:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Run the Application**
    ```bash
    python main.py
    ```
    This will automatically launch the application in your web browser.

## 🛠️ Tech Stack

-   **AI Model:** Google Gemini 1.5 Flash
-   **Backend:** Python
-   **UI:** Gradio
-   **Libraries:** `google-generativeai`, `python-dotenv`, `Pillow`