
import streamlit as st
from utils.styles import style
import os
import numpy as np
import cv2
from  PIL import Image 
from utils.utils import generateDownloadableImage



#  css part
st.write(style, unsafe_allow_html=True)
st.sidebar.markdown('<h3>TutuPhoto</h3>', unsafe_allow_html=True)
with st.sidebar.expander("About TutuPhoto"):
     st.write("""
        Use TutuPhoto to add intersting filters to your photos for free.\n\n Hope you enjoy!
     """) 








# check model exists
path = './model/colorization_release_v2.caffemodel'
isExist = os.path.exists(path)

if isExist:
   
   prototxt = r'../model/colorization_deploy_v2.prototxt'
   model = r'../model/colorization_release_v2.caffemodel'
   points = r'../model/pts_in_hull.npy'



   points = os.path.join(os.path.dirname(__file__), points)
   prototxt = os.path.join(os.path.dirname(__file__), prototxt)
   model = os.path.join(os.path.dirname(__file__), model)

   net = cv2.dnn.readNetFromCaffe(prototxt, model)     # load model from disk
   pts = np.load(points)

   # add the cluster centers as 1x1 convolutions to the model
   class8 = net.getLayerId("class8_ab")
   conv8 = net.getLayerId("conv8_313_rh")
   pts = pts.transpose().reshape(2, 313, 1, 1)
   net.getLayer(class8).blobs = [pts.astype("float32")]
   net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]


   uploaded_file = st.file_uploader("Upload Your Black & White Image", type=['jpg','png','jpeg']) 





   if uploaded_file is not None:
      try:
         col1, col2 = st.columns( [0.5, 0.5])

         image = Image.open(uploaded_file)  
         # convert Image PIL to OpenCv format
         img = np.array(image) 
         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
         scaled = img.astype("float32") / 255.0
         lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
         resized = cv2.resize(lab, (224, 224))
         L = cv2.split(resized)[0]
         L -= 50
         net.setInput(cv2.dnn.blobFromImage(L))
         ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
         ab = cv2.resize(ab, (img.shape[1], img.shape[0]))
      
         L = cv2.split(lab)[0]
         colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
         colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
         colorized = np.clip(colorized, 0, 1)
         colorized = (255 * colorized).astype("uint8")

         with col2:
            st.image(colorized, use_column_width='always', caption='Colorized') 
         with col1:
            st.image(image, use_column_width='always', caption="before") 
            byte_im = generateDownloadableImage(colorized)
            st.sidebar.markdown(f'<p style="text-align: center;">Colorized</p>', unsafe_allow_html=True)
            st.sidebar.download_button(
                        label="Download Colorized Image",
                        data=byte_im,
                        file_name=f"Colorized.{image.format}",
                        mime=f"image/{image.format}"
                     )
      except:
         st.markdown("sth went wrong, please try again or try another image")
else:
   import gdown
   # a file
   url = "https://drive.google.com/file/d/1qdFjzHQzL9Qw2u3EenTqJWlZbGWT9w-p/view?usp=share_link"

   output_path = './model/colorization_release_v2.caffemodel'
   gdown.download(url, output_path, quiet=False, fuzzy=True)
   
