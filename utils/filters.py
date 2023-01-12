import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline
# Filter Functions

def grey(img,*args,**kwargs):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img

def blackAndwhite(img, intensity=127, *arg, **kwargs):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_img, intensity, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage

# brightness adjustment
def bright(img, intensity = 30,*arg, **kwargs):
    img_bright = cv2.convertScaleAbs(img, beta=intensity)
    return img_bright

# brightness adjustment
def dark(img, intensity = -30,*arg, **kwargs):
    img_bright = cv2.convertScaleAbs(img, beta=intensity)
    return img_bright

#sharp effect
def sharpen(img, *arg, **kwargs):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(img, -1, kernel)
    return img_sharpen

#sepia effect
def sepia(img, *arg, **kwargs):
    img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia

#grey pencil sketch effect
def pencil_sketch_grey(img, *arg, **kwargs):
    #inbuilt function to create sketch effect in colour and greyscale
    sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=kwargs['sigma_s'], sigma_r=kwargs['sigma_r'], shade_factor=kwargs['shade_factor']) 
    return  sk_gray

#colour pencil sketch effect
def pencil_sketch_col(img, *arg, **kwargs):
    #inbuilt function to create sketch effect in colour and greyscale
    sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=kwargs['sigma_s'], sigma_r=kwargs['sigma_r'], shade_factor=kwargs['shade_factor']) 
    return  sk_color

#HDR effect
def HDR(img, *arg, **kwargs):
    hdr = cv2.detailEnhance(img, sigma_s=kwargs['sigma_s'], sigma_r=kwargs['sigma_r'])
    return  hdr

# invert filter
def invert(img, *arg, **kwargs):
    inv = cv2.bitwise_not(img)
    return inv

def LookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))
  
#summer effect
def summer(img, *arg, **kwargs):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv2.split(img)
    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    sum= cv2.merge((blue_channel, green_channel, red_channel ))
    return sum


#winter effect
def winter(img, *arg, **kwargs):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv2.split(img)
    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv2.merge((blue_channel, green_channel, red_channel))
    return win

filters_pointer = {'Grey':grey,'Black&White':blackAndwhite, 'PencilSketch-Grey':pencil_sketch_grey, 'PencilSketch-Color':pencil_sketch_col, 'Bright':bright, 'Dark':dark, 'Sharp':sharpen,'Sepia':sepia,'Invert':invert,'HDR':HDR,'Summer':summer,'Winter':winter}

