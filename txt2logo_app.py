import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from magic_admin import Magic

load_dotenv()

# Initialize Magic
try:
    magic = Magic(
        api_secret_key=os.getenv('MAGIC_API'),
        retries=5,
        timeout=5,
        backoff_factor=0.01,
    )
except Exception as e:
    st.error(f"Failed to initialize Magic: {e}")
    raise

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API")
client = OpenAI(api_key=api_key)

# Capture and validate the DID token
query_params = st.experimental_get_query_params()
did_token = query_params.get("token", [None])[0]

if did_token:
    try:
        magic.Token.validate(did_token)

        def generate_logo(industry, style, colors, keywords):
            prompt = (
                f"A sleek, memorable logo for a {industry} brand, "
                f"featuring a {style} design, with a focus on a clean and simple aesthetic. "
                f"Color scheme: {colors[0]}, {colors[1]}, {colors[2]}, {colors[3]}. "
                f"Incorporates elements of {keywords}. "
                f"Single image, scalable, with a transparent background."
            )
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url

        # Streamlit UI
        st.sidebar.title("Settings")
        st.sidebar.subheader("Additional Keywords")
        keywords = st.sidebar.text_input("Enter any additional keywords or prompts")

        st.title("Txt 2 Logo Generator")
        st.markdown("Welcome to the Txt 2 Logo Generator! Select your preferences to generate a custom logo.")

        selected_industry = st.select_slider("Industry", options=["Technology", "Fashion", "Food & Beverage", "Healthcare", "Education"])
        selected_style = st.select_slider("Style", options=["Modern", "Classic", "Minimalist", "Playful", "Wordmark"])

        palettes = {
            "Modern Tech Style": {
                "image_path": r"brand_colors\ModernTechStyle.png",
                "colors": ["Azure", "Charcoal", "Silver", "Neon Green"]
            },
            "Vintage Nostalgia Style": {
                "image_path": r"brand_colors\VintageNostalgiaStyle.png",
                "colors": ["Rust", "Olive", "Cream", "Burgundy"]
            },
            "Nature Inspired Style": {
                "image_path": r"brand_colors\NatureInspiredStyle.png",
                "colors": ["Forest Green", "Sky Blue", "Sand", "Sunflower Yellow"]
            }
        }
        palette_names = list(palettes.keys())
        selected_palette_name = st.select_slider("Palette", options=palette_names)

        selected_palette = palettes[selected_palette_name]
        st.image(selected_palette['image_path'], caption=f"{selected_palette_name} Colors", width=300)
        st.write("Colors:", ", ".join(selected_palette['colors']))

        if st.button("Create My Logo"):
            if selected_industry and selected_style and selected_palette:
                logo_url = generate_logo(selected_industry, selected_style, selected_palette['colors'], keywords)
                st.image(logo_url, caption="Your Generated Logo")
            else:
                st.error("Please select an industry, a style, and a color palette.")

        st.markdown("*Thank you for using Txt 2 Logo Generator!*")
    except Exception as e:
        st.error(f"Invalid token: {e}")
else:
    st.error("No token provided.")

        
        

