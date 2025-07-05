import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import gradio as gr

# --- 1. Configuration and Setup (No Changes) ---
load_dotenv()
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    if not api_key:
        raise ValueError("API key is empty. Please check your .env file.")
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")
except (KeyError, ValueError) as e:
    print(f"ERROR: Could not configure Gemini API. {e}")
    with gr.Blocks() as demo:
        gr.Markdown("# 🔴 ERROR: Missing Google API Key\nPlease create a `.env` file and add your `GOOGLE_API_KEY` to it.")
    demo.launch()
    exit()

# --- 2. Core AI and Image Processing Logic (No Changes) ---
vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_vision_response(image, prompt):
    try:
        response = vision_model.generate_content([prompt, image])
        if not response.parts:
            block_reason = "unknown"
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason.name.lower().replace('_', ' ')
            error_message = f"❌ **Analysis Blocked** ❌\n\n"\
                            f"The image could not be processed. This is likely because it was flagged for a safety reason (e.g., it may contain inappropriate content).\n\n"\
                            f"Reason provided by the API: **{block_reason}**"
            return error_message
        return response.text
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An error occurred while communicating with the AI. Please try again."

# --- 3. The Main Function for Gradio (No Changes) ---
def image_analyzer(image_input):
    if image_input is None:
        return "Please provide an image first by uploading or using the webcam."
    pil_image = Image.fromarray(image_input)
    prompt = """
    You are an expert image analyst. Your task is to analyze the provided image and give a structured response with three distinct parts.
    Your response must use Markdown for formatting (e.g., **bold** headings).

    1.  **Detailed Description:**
        Provide a detailed, multi-sentence paragraph describing the image. Mention the main subject, the setting, colors, mood, and any important details.

    2.  **Origin & Location Identification:**
        Analyze if the image contains a recognizable real-world landmark, or if it is a famous piece of art, photograph, or internet meme. If you identify a specific place or work, state its name and origin (e.g., "Eiffel Tower, Paris, France" or "The Mona Lisa by Leonardo da Vinci"). If it's a generic scene, state "This appears to be a generic location or object."

    3.  **AI Generation Analysis:**
        Carefully examine the image for signs of being AI-generated (e.g., unnatural textures, errors in details like hands or text, overly perfect composition). Provide your estimation as a percentage of the likelihood that this image was created by an AI. Format your answer exactly as: "**AI Generation Likelihood:** [a number between 0 and 100]%".
    """
    analysis_result = get_gemini_vision_response(pil_image, prompt)
    return analysis_result

# --- 4. The Gradio User Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {background-color: #f0f4f9;}") as demo:
    gr.Markdown(
        """
        # 🖼️ Image to Text AI (V2.2) 📝
        Upload an image, paste from your clipboard, or use your webcam. The AI will provide a detailed analysis.
        """
    )

    with gr.Row(variant='panel'):
        # Input Column
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.TabItem("⬆️ Upload & Paste"):
                    # --- MODIFIED: Added 'clipboard' back to the sources ---
                    image_upload_input = gr.Image(type="numpy", label="Upload an Image or Paste from Clipboard", sources=['upload', 'clipboard'])
                
                with gr.TabItem("📸 Use Webcam"):
                    # --- MODIFIED: Polished instructions and component label for maximum clarity ---
                    gr.Markdown("**Instructions:**\n1. Allow browser access to your camera.\n2. Look for the **\"Snap\"** button below the video and click it to capture a photo.\n3. The snapped photo will appear in the box, replacing the live video.\n4. Click the \"Analyze Image\" button below.")
                    image_webcam_input = gr.Image(type="numpy", label="Step 1: Click \"Snap\" Below to Take Photo", sources=["webcam"])
            
            analyze_button = gr.Button("Step 2: Analyze Image", variant="primary")

        # Output Column
        with gr.Column(scale=1):
            text_output = gr.Markdown(
                label="AI Analysis",
                value="The AI's analysis will appear here...",
            )

    # Logic to handle inputs (No Changes)
    def get_image_from_any_input(img_from_upload, img_from_webcam):
        image_to_analyze = img_from_upload if img_from_upload is not None else img_from_webcam
        return image_analyzer(image_to_analyze)

    analyze_button.click(
        fn=get_image_from_any_input,
        inputs=[image_upload_input, image_webcam_input],
        outputs=text_output
    )

# --- 5. Launch the Application (No Changes) ---
if __name__ == "__main__":
    demo.launch(inbrowser=True)