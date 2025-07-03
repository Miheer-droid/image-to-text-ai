import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import gradio as gr

# --- 1. Configuration and Setup ---

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API with the key from the environment
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    if not api_key:
        raise ValueError("API key is empty. Please check your .env file.")
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")
except (KeyError, ValueError) as e:
    print(f"ERROR: Could not configure Gemini API. {e}")
    # Display an error in the Gradio interface if the key is missing
    with gr.Blocks() as demo:
        gr.Markdown("# 🔴 ERROR: Missing Google API Key\nPlease create a `.env` file and add your `GOOGLE_API_KEY` to it.")
    demo.launch()
    exit()

# --- 2. Core AI and Image Processing Logic ---

# Create the GenerativeModel instance for the vision model
vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_vision_response(image, prompt):
    """
    Analyzes the image with a given prompt using the Gemini Vision model.
    Handles potential errors, including safety blocks.
    
    Args:
        image (PIL.Image.Image): The image to analyze.
        prompt (str): The text prompt to guide the AI.
        
    Returns:
        str: The generated text response or an error message.
    """
    try:
        # Generate content using the image and prompt
        response = vision_model.generate_content([prompt, image])
        
        # Check if the response was blocked due to safety settings
        if not response.parts:
            # Construct a user-friendly message about why it might have been blocked
            block_reason = "unknown"
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason.name.lower().replace('_', ' ')
            
            error_message = f"❌ **Analysis Blocked** ❌\n\n"\
                            f"The image could not be processed. This is likely because it was flagged for a safety reason (e.g., it may contain inappropriate content).\n\n"\
                            f"Reason provided by the API: **{block_reason}**"
            return error_message
            
        return response.text
        
    except Exception as e:
        # Catch any other potential errors during the API call
        print(f"An unexpected error occurred: {e}")
        return "An error occurred while communicating with the AI. Please try again."

# --- 3. The Main Function for Gradio ---

def image_analyzer(image):
    """
    This is the main function that Gradio will call when a user uploads an image.
    
    Args:
        image (numpy.ndarray): The image uploaded by the user (Gradio provides it in this format).
        
    Returns:
        str: The AI's formatted analysis of the image.
    """
    if image is None:
        return "Please upload an image first."
    
    # Convert the NumPy array from Gradio into a PIL Image object
    pil_image = Image.fromarray(image)
    
    # This is our detailed, "hidden" prompt that the user doesn't see
    prompt = """
    You are an expert image analyst. Your task is to analyze the provided image and give a structured response with three distinct parts.
    
    1.  **Detailed Description:**
        Provide a detailed, multi-sentence paragraph describing the image. Mention the main subject, the setting, colors, mood, and any important details.
    
    2.  **Location Identification:**
        Analyze if the image contains a recognizable real-world landmark, city, or natural wonder. If you identify a specific place, state its name clearly. If it's a generic location or unidentifiable, state "Location is not a recognizable landmark."
    
    3.  **AI Generation Analysis:**
        Carefully examine the image for signs of being AI-generated (e.g., unnatural textures, errors in details like hands or text, overly perfect composition). Provide your estimation as a percentage of the likelihood that this image was created by an AI. Format your answer exactly as: "AI Generation Likelihood: [a number between 0 and 100]%".
    """
    
    # Get the response from our Gemini function
    analysis_result = get_gemini_vision_response(pil_image, prompt)
    
    return analysis_result

# --- 4. The Gradio User Interface Definition ---

# Define the user interface using Gradio Blocks for more control
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {background-color: #f0f4f9;}") as demo:
    gr.Markdown(
        """
        # 🖼️ Image to Text AI 📝
        Upload an image and the AI will provide a detailed analysis, including a description, 
        location identification, and an estimate of whether the image is AI-generated.
        """
    )
    
    with gr.Row():
        image_input = gr.Image(type="numpy", label="Upload Your Image", sources=["upload", "webcam", "clipboard"])
        text_output = gr.Textbox(label="AI Analysis", lines=15, placeholder="The AI's analysis will appear here...", interactive=False)
    
    analyze_button = gr.Button("Analyze Image", variant="primary")
    
    # Connect the button click to the image_analyzer function
    analyze_button.click(
        fn=image_analyzer,
        inputs=image_input,
        outputs=text_output
    )

    gr.Markdown(
        """
        ---
        *Powered by Google Gemini Pro Vision. Built with Python and Gradio.*
        """
    )

# --- 5. Launch the Application ---

if __name__ == "__main__":
    # Launch the Gradio app. It will open in your browser.
    demo.launch(inbrowser=True)