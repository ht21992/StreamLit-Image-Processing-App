# Import libraries
import streamlit as st
import numpy as np
from PIL import Image
import base64
from st_click_detector import click_detector
from utils.styles import style
from utils.filters import filters_pointer
from utils.utils import generateDownloadableImage
import os

# Inital Slider Values
initialValues = {'Bright': 30, 'Dark': -30, 'Black&White': 127, 'HDR': {'sigma_s': 12, 'sigma_r': 0.15}, 'PencilSketch-Color': {
    'sigma_s': 60, 'sigma_r': 0.07, 'shade_factor': 0.1}, 'PencilSketch-Grey': {'sigma_s': 60, 'sigma_r': 0.07, 'shade_factor': 0.1}}


if "n_clicks" not in st.session_state:
    st.session_state["n_clicks"] = "0"


# Change page names on Side bar
st.set_page_config(
    page_title="TutoPhoto - Filter Photos",

)


pages = st.source_util.get_pages('main.py')
new_page_names = {
    'main': 'Filter Photo',
    'colorizePhoto': 'Colorize Photo',
}


for key, page in pages.items():
    if page['page_name'] in new_page_names:
        page['page_name'] = new_page_names[page['page_name']]

# Change page names on Side bar

#  css part
st.write(style, unsafe_allow_html=True)


logo = Image.open('logo.ico')
st.sidebar.markdown('<h3>TutuPhoto</h3>', unsafe_allow_html=True)
with st.sidebar.expander("About TutuPhoto"):
    st.write("""
        add coll filters to your photos, enhance the quality of your photos and colorize your old black and white images for free.\n\n Hope you enjoy!
     """)
    st.image(logo, width=30)
    st.markdown('<a href="https://www.buymeacoffee.com/hosseintaj">Buy Me A Coffee</a>',
                unsafe_allow_html=True)


# Add file uploader to allow users to upload photos
uploaded_file = st.file_uploader(
    "Upload Your Image", type=['jpg', 'png', 'jpeg'])

thumbnails = next(os.walk(r'./thumbnails'))[2]
id = str(int(st.session_state["n_clicks"]) + 1)


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    converted_img = np.array(image.convert('RGB'))
    col1, col2 = st.columns([0.5, 0.5])

    encoded_thumbnails = []
    for thumb in thumbnails:
        with open(f'./thumbnails/{thumb}', "rb") as exampleImage:
            encoded = base64.b64encode(exampleImage.read()).decode()
            encoded_thumbnails.append(f"data:image/jpeg;base64,{encoded}")

    content = ""
    for thumb, title in zip(encoded_thumbnails, ['Bright', 'PencilSketch-Color', 'Summer', 'Winter', 'HDR', 'PencilSketch-Grey', 'Sepia', 'Grey', 'Black&White', 'Dark', 'Sharp', 'Invert']):
        content += f"<a  href='#' id={title}><img style='width:100px !important;margin:5px !important' src='{thumb}'></a>"
    clicked = click_detector(content, key="click_detector")

    if clicked != "" and clicked != st.session_state["n_clicks"]:
        intensity = 0
        sigma_s = 60
        sigma_r = 0.07
        shade_factor = 0.1
        if clicked in ['Black&White', 'Bright', 'Dark']:
            st.sidebar.markdown(
                f'<p style="text-align: center;">{clicked} Adjustments</p>', unsafe_allow_html=True)
            intensity = st.sidebar.slider(
                'Adjust the intensity', -255, 255, initialValues[clicked], step=1)
        elif clicked in ['HDR', 'PencilSketch-Color', 'PencilSketch-Grey']:
            st.sidebar.markdown(
                f'<p style="text-align: center;">{clicked} Adjustments</p>', unsafe_allow_html=True)
            sigma_s = st.sidebar.slider(
                'Adjust the smoothness', 0, 200, initialValues[clicked]['sigma_s'], step=1)
            sigma_r = st.sidebar.slider(
                'Adjust the edge', 0.1, 1.0, initialValues[clicked]['sigma_r'], step=0.1)
            if clicked in ['PencilSketch-Color', 'PencilSketch-Grey']:
                shade_factor = st.sidebar.slider(
                    'Adjust the shade', 0.0, 0.1, initialValues[clicked]['shade_factor'], step=0.01)
        after_filter_img = filters_pointer.get(clicked, '')(
            converted_img, intensity=intensity, sigma_r=sigma_r, sigma_s=sigma_s, shade_factor=shade_factor)
        with col2:
            st.image(after_filter_img,
                     use_column_width='always', caption=clicked)
            byte_im = generateDownloadableImage(after_filter_img)
            st.sidebar.download_button(
                label=f"Download {clicked} Filter",
                data=byte_im,
                file_name=f"Filtered.{image.format}",
                mime=f"image/{image.format}"
            )

    with col1:
        st.image(image, use_column_width='always', caption="before")
