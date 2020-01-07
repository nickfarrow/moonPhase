import urllib.request as req
import os
import imageio
import argparse
import subprocess

# Argument parser
parser = argparse.ArgumentParser("Download Moon Images and Create Video")
parser.add_argument("-t", "--thinning", default=1, help="Frequency of images to download, e.g. every 10th image")
parser.add_argument("-f", "--ffmpeg", action='store_true', help="Use ffmpeg to create video")
args = parser.parse_args()


def addZeros(imageNumber):
    """Add leading zeros to a number, up to 4 digits."""
    numAdd = 4 - len(str(imageNumber))
    return "0" * numAdd + str(imageNumber)

def getImage(imageNumber, directory):
    """Download an image given an image to an output directory"""
    URL = (
            "https://svs.gsfc.nasa.gov"
            "/vis/a000000/a004600/a004604/frames/"
            "730x730_1x1_30p/moon.{}.jpg"
            ).format(imageNumber)

    imageName = directory + imageNumber + ".jpg"
    req.urlretrieve(URL, imageName)
    return

def makeVideo(directory, startNumber, thinning, ffmpeg=False):
    """Create a video with the downloaded images"""
    
    # Get a list of all the files 
    files = [image for image in os.listdir(directory) if ".jpg" in image]
    

    # Create a video using ffmpeg command
    if ffmpeg:
        frameRate = str(len(files)/60)
        subprocess.run(
                ["ffmpeg",
                "-r", frameRate, 
                "-pattern_type", "glob",
                "-i", "./images/*.jpg",
                "-vb", "20M", "moon.mp4"], check=True)
    
    else:
        # Save each image frame to a list
        images = []
        for imageNumber in range(startNumber, 8761, thinning):
            imageName = directory + addZeros(imageNumber) + ".jpg"
            images.append(imageio.imread(imageName))

        imageio.mimsave('moon.gif', images)
    return

def main(startNumber=1, thinning=1, ffmpeg=False):
    
    directory = 'images/'

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for imageNumber in range(startNumber, 8761, thinning):
        imagePercent = imageNumber
        imageNumber = addZeros(imageNumber)
        
        # Skip if already downloaded
        if os.path.exists(directory + imageNumber + ".jpg"):
            print("Already downloaded " + imageNumber)  
            continue
            
        while True:
            try:
                getImage(imageNumber, directory)
                percent = imagePercent / 87.61
                percent=round(percent,2)
                barre = (
                        "["
                        + "#" * int((50 / 100) * percent)
                        + "-" * int((50 / 100) * (100 - percent))
                        + "]"
                )
                print('\033c')
                print(str(percent)+str("% ")+barre)
            except Exception as e:
                print(e)
                continue
            break
            
    print("Making video...")
    makeVideo(directory, startNumber, thinning, ffmpeg)
    return


main(1, int(args.thinning), args.ffmpeg)


