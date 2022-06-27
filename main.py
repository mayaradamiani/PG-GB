import cv2
import numpy as np
from matplotlib import pyplot as plt
import scipy
from scipy.interpolate import UnivariateSpline

teste = {}

class Sticker():         
    def __init__(self, x, y, image): 
        self.x = x
        self.y = y 
        self.image = image

def mouseCallback(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONUP:
        if imageSticker is not None :
            sticker = Sticker(x, y,  cv2.resize(imageSticker, (54,54)))
            stickers.append(sticker)

def LookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))

def greyscale(img):
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return greyscale

def bright(img, beta_value):
    img_bright = cv2.convertScaleAbs(img, beta=beta_value)
    return img_bright

def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 8.5, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(img, -1, kernel)
    return img_sharpen

def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) 
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) 
    img_sepia[np.where(img_sepia > 255)] = 255 
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia

def pencilSketchGrey(img):
    sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_gray

def invert(img):
    inv = cv2.bitwise_not(img)
    return inv

def summer(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv2.split(img)
    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    sum= cv2.merge((blue_channel, green_channel, red_channel ))
    return sum

def winter(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv2.split(img)
    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv2.merge((blue_channel, green_channel, red_channel))
    return win

def HDR(img):
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return  hdr

def blur(img):
    blurredImage = cv2.GaussianBlur(img, (15, 15), 0)
    return  blurredImage

def saveImage(img, filename):
    cv2.imwrite(filename, img)

def select_filter():
    match selectedFilter:
        case 1:
            return summer(image)
        case 2:
            return greyscale(image)
        case 3:
            return bright(image, 60)
        case 4:
            return bright(image, -60)
        case 5:
            return sharpen(image)
        case 6:
            return sepia(image)
        case 7:
            return pencilSketchGrey(image)
        case 8:
            return invert(image)
        case 9:
            return HDR(image)
        case 10:
            return blur(image)
        case 11:
            return winter(image)
        case _:
            return image

def select_sticker():
    match selectedSticker:
        case 1:
            return cv2.imread("Stickers/cubo.jpg", cv2.IMREAD_UNCHANGED)
        case 2:
            return cv2.imread("Stickers/sol.jpg", cv2.IMREAD_UNCHANGED)
        case 3:
            return cv2.imread("Stickers/boca.jpg", cv2.IMREAD_UNCHANGED)
        case 4:
            return cv2.imread("Stickers/lua.jpg", cv2.IMREAD_UNCHANGED)
        case 5:
            return cv2.imread("Stickers/gato.jpg", cv2.IMREAD_UNCHANGED)
        case 6:
            return cv2.imread("Stickers/cachorro.jpg", cv2.IMREAD_UNCHANGED)
        case 7:
            return cv2.imread("Stickers/bom dia.jpg", cv2.IMREAD_UNCHANGED)
        case 8:
            return cv2.imread("Stickers/oculos.jpg", cv2.IMREAD_UNCHANGED)
        case 9:
            return cv2.imread("Stickers/disco.jpg", cv2.IMREAD_UNCHANGED)
        case 10:
            return cv2.imread("Stickers/quadro.jpg", cv2.IMREAD_UNCHANGED)
        case _:
            return None

def options(image):
    cv2.putText(image, "space - mudar filtro", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)
    cv2.putText(image, "x - mudar sticker", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)
    cv2.putText(image, "y - limpar stickers", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)
    cv2.putText(image, "s - salvar imagem", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)
    cv2.putText(image, "esc - sair", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 1)


inputTeclado = input ("ESCOLHA UMA DAS OPÇÕES:\n1 - Capturar imagem\n2 - Upload imagem\nnúmero:")
cv2.namedWindow("Window")
cv2.setMouseCallback("Window", mouseCallback)

selectedFilter = 0
selectedSticker = 1
stickers = []
image = None
imageFilter = None
imageSticker = None
vid = None
sticker = 0

bocaOriginal =  cv2.imread("Stickers/boca.jpg", cv2.IMREAD_UNCHANGED)
boca =  cv2.resize(bocaOriginal, (92,54));

if(inputTeclado == '1'):
    vid = cv2.VideoCapture(0)
    ret, image = vid.read()
if(inputTeclado == '2'):
    filename = input ("\nIndique o caminho da imagem:")
    image = cv2.imread(filename)

while True:

    if(inputTeclado == '1'):
        ret, image = vid.read()
    
    keypressed = cv2.waitKey(1) & 0xFF
    if keypressed == 27:
        break
    if keypressed == 32:
        selectedFilter += 1
        if(selectedFilter == 12):
            selectedFilter = 0
    if keypressed == 120:
        selectedSticker += 1
        if(selectedSticker == 11):
            selectedSticker = 0
    if keypressed == 121:
        stickers = []
    if(keypressed == 115):
        cv2.imwrite("imagem.png", imageFilter)

    imageFilter = select_filter()
    imageSticker = select_sticker()
    for num in range(len(stickers)):
        imageFilter[stickers[num].y:stickers[num].y + stickers[num].image.shape[0], stickers[num].x:stickers[num].x + stickers[num].image.shape[1] ] = stickers[num].image
    options(imageFilter)
    cv2.imshow('Window', imageFilter)
    

vid.release()
cv2.destroyAllWindows()

