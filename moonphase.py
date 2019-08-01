import urllib.request as req
import os
import imageio

def addZeros(imageNumber):
    numAdd = 4 - len(str(imageNumber))
    return "0" * numAdd + str(imageNumber)

def getImage(imageNumber, directory):
    URL = "https://svs.gsfc.nasa.gov/vis/a000000/a004600/a004604/frames/730x730_1x1_30p/moon." + imageNumber + ".jpg" 
    imageName = directory + imageNumber + ".jpg"
    req.urlretrieve(URL, imageName)
    return

def makeVideo(directory):
	files = [image for image in os.listdir(directory) if ".jpg" in image]
	images = []

	for frameFile in files:
		images.append(imageio.imread(directory + frameFile))
	imageio.mimsave(directory + 'movie.gif', images)	
	return

def main(startNumber=1, thinning=10):
    
    directory = 'images/'

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for imageNumber in range(startNumber, 8761, thinning):
        while True:
            try:
                imageNumber = addZeros(imageNumber)
                getImage(imageNumber, directory)
                print("Done " + imageNumber)
            except Exception as e:
                print(e)
                continue
            break
            
    print("Making video...")
    makeVideo(directory)
    return

main(1, 20)

