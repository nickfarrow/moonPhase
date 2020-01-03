# moonPhase
Downloads all 8762 photos of the moon from a NASA website and uses them to create a fluid animation.

See [here for an introduction/tutorial](https://nicholasfarrow.com/Creating-a-Moon-Animation-Using-NASA-Images-and-Python/).

# Usage
```
python moonphase.py
```

```
optional arguments:
  -h, --help            show this help message and exit
  -t THINNING, --thinning THINNING
                        Frequency of images to download, e.g. every 10th image
  -f, --ffmpeg          Use ffmpeg to create video
```

If you are creating a gif via imageio then creating a `.gif` of 8761 images could take a long time and create a >100Mb file. Try using a smaller number of images with the `-t` flag:

Eg. use every 20th image:
```
python moonphase.py -t 20
```

If you are on a unix OS and have ffmpeg installed then you can compile an `.mp4` instead of a `.gif`:
```
python moonphase.py -f
```
