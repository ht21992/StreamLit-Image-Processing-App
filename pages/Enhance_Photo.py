
import streamlit as st
from utils.styles import style
import numpy as np
import cv2
from PIL import Image
from utils.utils import generateDownloadableImage

#  css part
st.write(style, unsafe_allow_html=True)
st.sidebar.markdown('<h3>TutuPhoto</h3>', unsafe_allow_html=True)
with st.sidebar.expander("About TutuPhoto"):
    st.write("""
        Use TutuPhoto to add intersting filters to your photos for free.\n\n Hope you enjoy!
     """)


uploaded_file = st.file_uploader(
    "Upload Your Image", type=['jpg', 'png', 'jpeg'])

sr = cv2.dnn_superres.DnnSuperResImpl_create()


model_path = "model/FSRCNN_x3.pb"


sr.readModel(model_path)

sr.setModel("fsrcnn", 3)


col1, col2 = st.columns([0.5, 0.5])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        converted_img = np.array(image.convert('RGB'))
        result = sr.upsample(converted_img)
        with col1:
            st.image(image, use_column_width='always', caption="original")
        with col2:
            st.image(result, use_column_width='always', caption='Enhanced')
            byte_im = generateDownloadableImage(result)
            st.sidebar.markdown(
                f'<p style="text-align: center;">Enhanced</p>', unsafe_allow_html=True)
            st.sidebar.download_button(
                label="Download Enhanced Image",
                data=byte_im,
                file_name=f"Enhanced.{image.format}",
                mime=f"image/{image.format}"
            )
    except:
         st.markdown("sth went wrong, please try again or try another image")
