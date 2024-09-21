import streamlit as st 
import google.generativeai as genai
import os 
from dotenv import load_dotenv
from PIL import Image 
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def process_image(uploaded_image):
    if uploaded_image is not None:
        image_data = uploaded_image.getvalue()
    
        img_parts = [
            {
            "mime_type": uploaded_image.type,
            "data": image_data
            }
        ]
        return img_parts
    else:
        raise FileNotFoundError("No file is uploaded!")

st.set_page_config(page_title="Meal Advisor App!")
st.header("Meal Advisor App!")
file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if file is not None:
    image = Image.open(file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the dish!")

input_prompt="""
You are an expert nutritionist and chef. Your task is to analyze the ingredients or dish from the uploaded image and suggest potential recipes that can be made using these items. Additionally, provide detailed nutritional information, including the calories for each food item and the total calorie content for the suggested recipes.
Please respond in the following format:
1. Suggested Recipe 1
   - Ingredients: [List of ingredients]
   - Instructions: [Step-by-step instructions]
   - Nutritional Information:
     - Total Calories: [Total calories for the recipe]
     - [Item 1] - [Number of calories]
     - [Item 2] - [Number of calories]
     - [Item 3] - [Number of calories]
   ----
2. Suggested Recipe 2
   - Ingredients: [List of ingredients]
   - Instructions: [Step-by-step instructions]
   - Nutritional Information:
     - Total Calories: [Total calories for the recipe]
     - [Item 1] - [Number of calories]
     - [Item 2] - [Number of calories]
   ----
"""

## If submit button is clicked

if submit:
    image_data=process_image(file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)