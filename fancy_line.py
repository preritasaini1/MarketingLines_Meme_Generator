import streamlit as st  # UI Design
import os
import requests
import random
import base64
import tempfile  # To create a temporary file for the meme
from dotenv import load_dotenv  # For loading environment variables
from PIL import Image, ImageDraw, ImageFont  # For meme generation

# Load environment variables
load_dotenv()

# Import Google Generative AI
import google.generativeai as genai

# Configure genai API
genai.configure(api_key='AIzaSyDVEax7Sy6Wnpt_s7sIFho5wNgFUjN8l54')

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Function to generate the marketing campaign output
def get_marketing_output(product, audience):
    prompt = f"""
    You are an expert copywriter. Create a marketing campaign output for the following:
    Product: {product}
    Target Audience: {audience}
    
    The output should include:
    - creative headline in indian perspective with hinglish in rhyme in english written
     - You are a creative copywriter tasked with generating catchy and playful marketing lines. The style should be flirty, witty, and engaging, similar to how Zomato markets itself. Focus on clever wordplay, puns, and humor that would appeal to a young, loving audience. The lines should be short, snappy, and perfect for social media, creating a fun and friendly vibe that grabs attention. Make the audience smile and feel connected to the brand.
     - Generate 5 catchy and flirty marketing lines with a tone similar to Zomato's playful style in hinglish. 
    - A short and catchy tagline
    - A detailed product description
    - 5 relevant hashtags
    - 5 dynamic marketing lines (similar to the style of slogans or catchy phrases)
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate dynamic fancy lines for marketing
def get_dynamic_fancy_lines(product, audience):
    prompt = f"""
    You are an expert marketer. Generate 5 creative, catchy, and dynamic marketing lines for the following:
    Product: {product}
    Target Audience: {audience}
    
    The lines should be:
    - Short and catchy
    - Evoke curiosity or excitement
    - Be suitable for social media marketing
    """
    response = model.generate_content(prompt)
    return response.text.splitlines()

# Function to generate dynamic Hinglish fancy lines for marketing
def get_dynamic_hinglish_lines(product, audience):
    prompt = f"""
    You are an expert marketer and Hindi-English (Hinglish) copywriter. 
    Generate 5 creative, catchy, and dynamic marketing lines in Hinglish for the following:
    Product: {product}
    Target Audience: {audience}
    
    The lines should be:
    - Short and catchy
    - Evoke curiosity or excitement
    - Use Hinglish language (a mix of Hindi and English)
    - Be suitable for social media marketing
    """
    response = model.generate_content(prompt)
    return response.text.splitlines()

# Function to generate memes with centered text and user-selected font color
def generate_meme(image, top_text, bottom_text, font_size, text_color="white"):
    meme_image = Image.open(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(meme_image)

    # Function to split text into multiple lines if it exceeds the width
    def split_text(text, font, max_width, draw):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # Calculate width of the current line with the new word added
            width, _ = draw.textbbox((0, 0), current_line + " " + word, font=font)[2:4]
            
            # If the word fits, add it to the current line
            if width <= max_width:
                current_line += (" " + word) if current_line else word
            else:
                # Otherwise, start a new line
                if current_line:
                    lines.append(current_line)
                current_line = word

        # Add the last line
        if current_line:
            lines.append(current_line)

        return lines

    # Split the top and bottom text
    top_lines = split_text(top_text, font, meme_image.width - 20, draw)
    bottom_lines = split_text(bottom_text, font, meme_image.width - 20, draw)

    # Calculate the space needed for both top and bottom texts
    top_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in top_lines]) + len(top_lines) * 5
    bottom_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in bottom_lines]) + len(bottom_lines) * 5

    # Ensure there's enough space for both texts
    if top_text_height + bottom_text_height >= meme_image.height:
        raise ValueError("Text is too large for the image. Reduce the font size or text length.")

    # Position for top text (centered)
    top_y = 10
    for line in top_lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        text_position = ((meme_image.width - text_width) // 2, top_y)
        draw.text(text_position, line.upper(), fill=text_color, font=font, stroke_width=2, stroke_fill="black")
        top_y += text_height + 5

    # Position for bottom text (centered, from the bottom)
    bottom_y = meme_image.height - bottom_text_height - 10
    for line in bottom_lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        text_position = ((meme_image.width - text_width) // 2, bottom_y)
        draw.text(text_position, line.upper(), fill=text_color, font=font, stroke_width=2, stroke_fill="black")
        bottom_y += text_height + 5

    # Save the resulting meme to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        meme_image.save(tmpfile.name)
        return tmpfile.name



# Setting up the Streamlit app
st.set_page_config(
    page_title='Marketing Campaign & Meme Generator',
    layout="wide",
    page_icon=":sparkles:",
    initial_sidebar_state="expanded"
)

# Header for the app
st.header("FunFusion: Meme and Content Creator :gem:")

# Tabs for functionality
tab1, tab2 = st.tabs(["📢 Marketing Campaign Generator", "😂 Meme Generator"])

st.sidebar.header("💡 Boost Your Marketing with Fun & Memes!")
st.sidebar.subheader("Create, Customize, Engage!")
st.sidebar.markdown("___")
st.sidebar.subheader("📍 Marketing Tip of the Day")
st.sidebar.info(
    "Marketing is not about selling a product; it's about telling a story! "
    "Connect with your audience emotionally to leave a lasting impression."
)

# Example API: Random Facts
def get_random_fact():
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    data = response.json()
    return data['text']

random_fact = get_random_fact()
st.sidebar.markdown(f"🧠 {random_fact}")
st.sidebar.markdown("___")

st.sidebar.write(''' 
             <u>**Features:**</u>
            - **Instant Meme Creation:** Generate fun and personalized memes in seconds.
            - **Campaign Customization:** Design marketing campaigns tailored to your audience.
            - **Dynamic Text and Image Editing:** Customize fonts, sizes, and images for your perfect visual.
            - **Social Media Integration:** Share your memes and campaigns directly on social platforms.
            - **Easy-to-Use Interface:** No design skills required—just a few clicks to create amazing content.
            - **Fun & Interactive:** Use AI to add a creative flair to your posts with unlimited possibilities.
             
             With FunFusion, you can effortlessly boost your marketing and entertain your audience in a whole new way!
    ''', unsafe_allow_html=True)

st.sidebar.markdown("___")
st.sidebar.subheader("📞 Contact Us")
st.sidebar.text("Have any questions or feedback? Reach out to us:")
st.sidebar.text("📧 project@funfusion.com")


st.markdown(
    """
    <style>
    /* Change background color of the entire page */
    .stApp {
        background-color: #F5988C /* Light purple */
    }

    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: 	 #F0F0F0; /* Light blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Marketing Campaign Generator
with tab1:
    # Inputs for product details and target audience
    product_details = st.text_input("Enter Product Details", "A new platform for seamless online learning")
    target_audience = st.text_input("Enter Target Audience", "college students and young professionals")

    # Generate button
    if st.button("Generate Marketing Campaign"):
        st.info("⚠️ The lines and content generated by this tool may not always be perfect or accurate. Please review and customize them before using them in your campaigns. Use at your discretion.")
        if product_details and target_audience:
            # Add a notification before generating the output
            st.info("✨ Hang tight! Crafting the perfect campaign for your product...")

            # Call the function to generate marketing output
            response = get_marketing_output(product_details, target_audience)

            # Display the generated campaign output
            st.markdown("### Generated Marketing Campaign")
            st.write(response)

            # Generate dynamic marketing lines
            st.write("Fancy Marketing Lines:")
            dynamic_lines = get_dynamic_fancy_lines(product_details, target_audience)
            for line in dynamic_lines:
                st.write(f"✅ {line}")

            # Generate dynamic Hinglish fancy lines
            st.write("Fancy Marketing Lines (Hinglish):")
            dynamic_hinglish_lines = get_dynamic_hinglish_lines(product_details, target_audience)
            for notification in dynamic_hinglish_lines:
                st.write(f"🌟 {notification}")

            # Success message
            st.success("🎉 Success! Your marketing campaign is ready to shine!")

        else:
            st.warning("⚠ Please fill in both fields to generate a campaign.")

# Meme Generator
with tab2:
    st.header("Meme Generator with Topic-Specific Short Lines")

    # Dropdown for selecting a meme topic
    meme_topic = st.selectbox(
        "Select a Meme Topic",
        ["Social Welfare", "Study", "Laugh", "Knowledge"]
    )

    # Function to generate meme text using AI
    def generate_meme_line(topic):
        prompt = f"""
        You are a creative copywriter tasked with generating a short and catchy meme line. 
        The style should be flirty, catchy, and engaging, similar to how Zomato markets itself. 
        Focus on clever wordplay, puns, and humor. 

        For the selected topic: {topic}, create a single short and catchy line in Hinglish (a mix of Hindi and English) 
        that is fun, relatable, and perfect for a meme.
        """
        response = model.generate_content(prompt)
        return response.text.strip()  # Get a single line of text

    # Upload image and customize meme
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    top_text = st.text_input("Top Text", "TOP TEXT")
    bottom_text = st.text_input("Bottom Text", "BOTTOM TEXT")
    font_size = st.slider("Font Size", 10, 50, 25)
    text_color = st.color_picker("Choose Text Color by clicking on color picker:", "#F3E2E2")
    
    if uploaded_image:
        # Generate the meme
        meme_path = generate_meme(uploaded_image, top_text, bottom_text, font_size, text_color)

        # Display the meme
        st.image(meme_path, caption="Your Meme", use_container_width=True)
        st.success("Meme generated successfully!")

        # Add download option
        with open(meme_path, "rb") as file:
            st.download_button(
                label="Download Meme",
                data=file,
                file_name="generated_meme.png",
                mime="image/png"
            )
    else:
        st.info("Upload an image to get started.")

