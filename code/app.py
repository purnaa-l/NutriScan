import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set the page configuration
st.set_page_config(page_title="NutriScan: Smart Calorie Counter")

# Logo
logo = Image.open("Logo.jpeg")  # Update with the path to your logo
st.image(logo, use_column_width=True, width=150)  # Resize the logo

# Title and header
st.title("🍽️ NutriScan: Your Smart Calorie Counter 🍽️")
st.markdown("""
    **📸 Snap a Picture of Your Meal!** 
    Let NutriScan do the rest! With just one click, you'll receive a comprehensive nutritional analysis of your food.

    **What You’ll Discover:**
    - **🔥 Calorie Counts:** Find out exactly how many calories are on your plate!
    - **📊 Macronutrient Breakdown:** Get insights into the distribution of carbohydrates, proteins, and fats.
    - **🥗 Health Assessments:** Understand the overall healthiness of your meal with our simple rating system.

    **Why Choose NutriScan?**
    - **Fast & Accurate:** Receive instant feedback on your meal’s nutritional content.
    - **Easy to Use:** Just upload an image and let our smart technology do the work for you!
    - **Stay Informed:** Make healthier choices by understanding your food better!

    Ready to dive into the world of nutrition? Upload your meal image now! 🚀
""")


# File uploader for image input
uploaded_file = st.file_uploader("📸 Click an image of your meal!", type=["jpeg", "jpg", "png"])
image = ""

# Display uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Meal Image", use_column_width=True)

# Submit button to analyze the image
submit = st.button("🔍 Get Nutritional Information!")

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Convert the uploaded image into the format required by the model
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Image Not Uploaded!")

# Detailed input prompt for the model
input_prompt = """
You are a nutrition expert analyzing an image of food uploaded by the user. Your task is to identify the food items present in the image and provide a detailed nutritional breakdown for each item. Please include the following information in a clear and organized format:

1. **Food Items Identified**:
   - List each food item detected in the image.

2. **Caloric Information**:
   - Provide the calorie count for each food item.

3. **Nutritional Breakdown**:
   - For each food item, detail the approximate content of the following nutrients:
     - Carbohydrates (in grams)
     - Proteins (in grams)
     - Fats (in grams)
     - Saturated Fats (in grams)
     - Vitamins (specify types and amounts)
     - Minerals (specify types and amounts)
     - Roughages/Fiber (in grams)

4. **Health Assessment**:
   - Assess the overall healthiness of the meal based on the nutritional information provided. Use a simple rating system (e.g., "Healthy," "Moderate," "Unhealthy") and provide a brief explanation for your assessment.

5. **Summary Statistics**:
   - At the end of your response, calculate and summarize the percentage contribution of each macronutrient (Carbohydrates, Proteins, Fats) to the total caloric content of the meal.

   - Present the information in a neat, structured format, using bullet points, headings, and sections for clarity.
"""

# Get the response and display it when the submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("📊 Nutritional Information")
    st.write(response)

# Custom CSS for improved styling
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9; /* Light background for better contrast */
        color: #333; /* Darker text color for improved readability */
    }
    .stButton {
        display: flex; 
        justify-content: center; /* Center the button horizontally */
        margin: 20px 0; /* Add margin for spacing */
    }
    .stButton > button {
        background-color: #007BFF; /* A professional blue color */
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 18px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
        transition: background-color 0.3s, transform 0.3s; /* Smooth transitions */
    }
    .stButton > button:hover {
        background-color: #0056b3; /* Darker blue for hover state */
        transform: translateY(-2px); /* Slight lift effect on hover */
    }
    h1 {
        color: #2c3e50; /* Dark slate blue for main title */
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    h2 {
        color: #34495e; /* Slate gray for section headers */
        margin-top: 30px;
        margin-bottom: 10px;
    }
    h3 {
        color: #7f8c8d; /* Lighter gray for subheaders */
        margin-top: 20px;
    }
    .markdown-text-container {
        color: #34495e; /* Consistent text color for markdown content */
        font-size: 16px;
        line-height: 1.6;
        margin: 0 auto; /* Center content */
        max-width: 800px; /* Maximum width for better readability */
    }
    .stImage {
        margin: 20px 0;
        border: 2px solid #ecf0f1; /* Light border for images */
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        background-color: white; /* White background for image container */
    }
</style>
""", unsafe_allow_html=True)
