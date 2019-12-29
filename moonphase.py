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

def makeVideo(directory, ffmpeg=False):
    """Create a video with the downloaded images"""
    
    # Get a list of all the files 
    files = [image for image in os.listdir(directory) if ".jpg" in image]
    
    if ffmpeg:
        frameRate = str(len(files)/60)
        subprocess.run(
                ["ffmpeg",
                "-r", frameRate, 
                "-pattern_type", "glob",
                "-i", "./images/*.jpg",
                "-vb", "20M", "moon.mp4"], check=True)
    
    else:
        # Save each frame to a list
        images = []
        for frameFile in files:
            images.append(imageio.imread(directory + frameFile))
            
        imageio.mimsave(directory + 'movie.gif', images)	
    return

def main(startNumber=1, thinning=1, ffmpeg=False):
    
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
    makeVideo(directory, ffmpeg)
    return


main(1, int(args.thinning), args.ffmpeg)


