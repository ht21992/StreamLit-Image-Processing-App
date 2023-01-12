from io import BytesIO
from  PIL import Image 
def generateDownloadableImage(img):
   img = Image.fromarray(img)
   buf = BytesIO()
   img.save(buf, format="JPEG")
   byte_im = buf.getvalue()
   return byte_im
