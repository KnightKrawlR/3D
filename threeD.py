"""
 *****************************************************************************
   FILE: threeD.py      

   AUTHOR: Wlajimir Alexis        

 *****************************************************************************
"""

from cs1graphics import *


def grayscaleImage(image):

    """ Takes an image and makes each pixel grayscale: the red, blue, and\
        green components are the average of the respective components in each\
        original pixel. Returns a new image. The original image is not\
        modified """

    # Creating a blank list
    newData = []
    width, height = image.size()
    # Create a blank image that is set to the demensions of the original image
    greyImage = Image(width, height)
    # Finding pixels of original image
    data = image.getPixels()
    
    # Finding the average of each tuple 
    for pixel in data:
        red, green, blue, alpha = pixel
        avg = ((red + green + blue)/3)
        # Appending new tuples to a new list, leaving alpha alone.
        newData.append((avg, avg, avg, alpha))
    # Set pixels of the new image to that of the tuples in the new list
    greyImage.setPixels(newData)
    return greyImage


def invertImage(image):

    """ Applies invertPixel to each pixel in the image. Returns a new\
        image. The original image is not modified. """

    # Creating a blank list
    newData = []
    width, height = image.size()
    # Create a blank image that is set to the demensions of the original image
    negImage = Image(width, height)
    # Finding pixels of original image
    data = image.getPixels()

    # Applying invert image to each pixel
    for pixel in data:
        # Calling invertPixel to return a new pixel
        newPixel = invertPixel(pixel)
        newData.append(newPixel)
    # Set pixels in the new image to the new List
    negImage.setPixels(newData)
    return negImage


def invertPixel(pixel):

    """ Takes a 4-tuple representing a pixel and returns a new pixel\
        representing the inverted (photographic negative) pixel """

    # Inverts every color in the pixel and returns the new pixel
    return (255 - pixel[0], 255 - pixel[1], 255 - pixel[2], pixel[3])
    

# Could combine two below but the lab asks to only pass image for makeThumbnail
def makeThumbnail(image):

    """ Creates a small version (width 300 pixels) of the original image by\
        scaling. The small version will have the same aspect ratio as the\
        original. Returns a new image. The original image is not modified. """

    # Finding the width and height of the old image
    width, height = image.size()
    # Creating a Blank Image with demensions of old image
    thumbnail = Image(width, height)
    # Getting the pixels of the old image
    pixList = image.getPixels()
    # Seting the new Image to the pixels of the old image
    thumbnail.setPixels(pixList)
    # Finding the ratio of height over width
    aspectRatio = float(height) / width
    # Use the ratio to resize new Image into a thumbnail
    thumbnail = thumbnail.resize(300, int(300 * aspectRatio))
    # Returns the Thumbnail
    return thumbnail

def makeNewSize(image, newWidth):

    """ Creates a new size with respect to aspect ratio of the original image.\
        The second version will have the same aspect ratio as the original.\
        Returns a new image. The original image is not modified. """

    # Finding the width and height of the old image
    width, height = image.size()
    # Creating a Blank Image with demensions of old image
    newSize = Image(width, height)
    # Getting the pixels of the old image
    pixList = image.getPixels()
    # Seting the new Image to the pixels of the old image
    newSize.setPixels(pixList)
    # Finding the ratio of height over width
    aspectRatio = float(height) / width
    # Use the ratio to resize new Image into a new size
    newSize = newSize.resize(newWidth, int(newWidth * aspectRatio))
    # Returns the new size
    return newSize


def cropping(imageA, imageB, overlayX, overlayY):

    """ Crops imageA and imageB according to the dx and dy of overlay and\
        returns the cropped images """

    # If the moving image is below: 
    if overlayY > 0:
        # Crop the top of the stationary image
        imageA = imageA.crop(overlayY, 0, 0, 0)
        # Crop the bottom of the moving image
        imageB = imageB.crop(0, overlayY, 0, 0)
    # If not:
    else:
        # Crop the bottom of the stationary image
        imageA = imageA.crop(0, (overlayY * -1), 0, 0)
        # Crop the top of the moving image
        imageB = imageB.crop((overlayY * -1), 0, 0, 0)

    # If the moving image is to the Left:
    if overlayX < 0:
        # Crop the right of the stationary image
        imageA = imageA.crop(0, 0, 0, (overlayX * -1))
        # Crop the left of the moving image
        imageB = imageB.crop(0, 0, (overlayX * -1), 0)
    else:
        # Crop the left of the stationary image
        imageA = imageA.crop(0, 0, overlayX, 0)
        # Crop the right of the moving image
        imageB = imageB.crop(0, 0, 0, overlayX)

    # Return the images    
    return imageA, imageB


def overLay(win, imageA, imageB):

    """ Allows the user to move the top image to set the overlay to the\
        desired amount and then returns the dx and dy of overlay"""

    print "Set the desired overlay using the arrow keys or mouse clicks."
    print "Then press X when you are satisfied"
    
    finish = False
    while not finish:
        win.refresh()
        ev = win.wait()
        des = ev.getDescription()
        # The user to manipulates the the top picture with the arrow keys 
        if (des == "keyboard"):
            key = ev.getKey()
            if key == "Up Arrow":
                imageB.move(0, -1)
            elif key == "Left Arrow":
                imageB.move(-1, 0)
            elif key == "Down Arrow":
                imageB.move(0, 1)
            elif key == "Right Arrow":
                imageB.move(1, 0)
            elif key in "Xx":
                # Finds the reference point of each image
                p1 = imageA.getReferencePoint()
                p2 = imageB.getReferencePoint()
                # Find the dx and dy distance from the reference points
                overLayX = p2.getX() - p1.getX()
                overLayY = p2.getY() - p1.getY()
                # Stop the while loop on next cycle
                finish = True
                # Return the dx dy distances from refrence points
                return overLayX, overLayY       
        # Make mouse clicks move picture
        elif (des == "mouse click"):
            loc = ev.getMouseLocation()
            loc2 = win.wait().getMouseLocation()
            imageB.move((loc2.getX() - loc.getX()), \
                       ((loc2.getY() - loc.getY())))
        # ensure that the while loop stops even if window closes
        elif (des == "canvas close"):
            finish = True
            
      
def setTransparency(image, transparency):

    """ Changes the original image by setting the transparency component\
        (alpha) of each pixel to the value transparency. Does not return a\
        value. """

    
    newData = []
    # Getting the pixels of the original image
    data = image.getPixels()
    
    # Set the transparency of all pixels in image to desired transparency
    for pix in data:
        newData.append((pix[0], pix[1], pix[2], transparency))
    # Set the original image's pixels to show the modified trasparency
    image.setPixels(newData)
    

def threeDLeftChannel(image):

    """ Creates a new image from the original retaining only the red component\
        of each pixel (makes the green and blue components zero.) Returns a\
        new image. The original image is not modified. """

    newData = []
    width, height = image.size()
    # Create a blank image
    redImg = Image(width, height)
    # Setting the green and blue of each pixel to zero
    data = image.getPixels()
    
    for pix in data:
        red, green, blue, alpha = pix
        green = 0
        blue = 0
        # Appending to a list the pixels that have green and blue set to zero
        newData.append((red, green, blue, alpha))
    # Set pixels of redImage to newData to make it red
    redImg.setPixels(newData)
    return redImg


def threeDRightChannel(image):

    """ Creates a new image from the original retaining only the green and\
        blue components of each pixel (makes red component zero.) Returns a\
        new image. The original image is not modified. """

    newData = []
    width, height = image.size()
    # Create blank image
    cyanImg = Image(width, height)
    # Loop through the pixels of image to modify and append it to a newList
    data = image.getPixels()
    
    for pix in data:
        red, green, blue, alpha = pix
        red = 0
        newData.append((red, green, blue, alpha))
    # Set pixels in the new image to the new List
    cyanImg.setPixels(newData)
    return cyanImg


def threeDPixel(pixelA, pixelB):

    """ Computes a new pixel value with the red datum from pixelA and the\
        green and blue data from pixelB. Returns the new pixel value. The\
        original pixels are not modified."""

    # Returning the fused tuple
    return (pixelB[0], pixelA[1], pixelA[2], pixelA[3])

       

def addImages(imageA, imageB):

    """ takes two images and returns a new image in which the three color\
        components of each pixel are added. The fourth pixel component (alpha)\
        is taken from imageA. Returns a new image. The original images are not\
        modified. """

    # Create a black list to store data
    newData = []
    
    # Get the height and width for the new Image
    width, height = imageA.size()
    # Create a new blank image
    newImg = Image(width, height)

    # Get the pixels from image A and B
    pixelA = imageA.getPixels()
    pixelB = imageB.getPixels()

    # Creating the final anaglyph image using threeD pixel return fused pixel
    for i in range(len(pixelB)):
        pixTup = threeDPixel(pixelA[i], pixelB[i])
        newData.append(pixTup)
    newImg.setPixels(newData)
    return newImg          

def showGrayscale():

    """ Asks the user for an image filename, then displays both that image\
        and its grayscale version in a window."""

    # Asking to user for the file name of the image.
    fileName = "left1.jpg"    #raw_input("What is the image's filename? ")
    # Setting image equal to the image the user has requested.
    image = Image(fileName)
   
    # Resizing image to ensure it fits the screen
    image = makeNewSize(image, 600)
    
    # Calling the function greyscale to create a grey version of image.
    greyImage = grayscaleImage(image)

    # Finding the height and width of the image.
    width, height = image.size()
    # Setting the canvas equal to the size of two images side by side
    win = Canvas((width * 2), height, "white", "Showing the Grey Images")
    win.setAutoRefresh(False)    
    # Moving both images side by side of each other.
    image.moveTo(width/2.0, height/2.0)
    greyImage.moveTo((width/2 + width), height/2.0)
    # Adding the images to the canvas.
    win.add(image)
    win.add(greyImage)
    # Refrehing the Canvas
    win.refresh()

    win.wait()
    win.close()

def showNegative():

    """ Asks the user for an image filename, then shows an original and\
        photographic negative image."""

    # Asking to user for the file name of the image.
    fileName = raw_input("What is the image's filename? ")
    # Setting image equal to the image the user has requested.
    image = Image(fileName)

    # Resizing image to ensure it fits the screen and runs quicker
    image = makeNewSize(image, 600)

    # Calling the function invertImage to create a negative version of image.
    negImage = invertImage(image)

    # Finding the height and width of the image.
    width, height = image.size()
    # Setting the canvas equal to the size of two images side by side
    win = Canvas((width * 2), height, "white", "Showing the Negative Images")
    win.setAutoRefresh(False)
    # Moving both images side by side of each other.
    image.moveTo(width/2.0, height/2.0)
    negImage.moveTo((width/2 + width), height/2.0)
    # Adding the images to the canvas.
    win.add(image)
    win.add(negImage)
    # Refrehing the Canvas
    win.refresh()

    win.wait()
    win.close()


def makeAnaglyph():

    """ Asks the user for a left, right, and composed filename, then shows a\
        thumbnail of the left and right image. Allows the user to adjust the\
        overlay then produes a threeD image with a width equal to the size of\
        the users requested amount."""

    # Asking to user for the file name of the left, right, and composed image.
    fileNameA = "left1.jpg"     #raw_input("What's the file name of the left Image? ")
    fileNameB = "right1.jpg"    #raw_input("What's the file name of the right Image? ")
    fileNameFinal = "threeD.py" #raw_input("What's the file name of the composite Image? ")
       
    # Set the width in pixels of the final anaglyph image to widthAna
    widthAna = 400              #int(raw_input("Enter the width of the final anaglylph image: "))

    # Setting images equal to the imageA and imageB the user has requested.
    imageA = Image(fileNameA)
    imageB = Image(fileNameB)
       
    # Resize the images
    thumbnailA = makeThumbnail(imageA)
    thumbnailB = makeThumbnail(imageB)

    # Making the thumbnails Cyan and Red
    thumbnailA = threeDRightChannel(thumbnailA)
    thumbnailB = threeDLeftChannel(thumbnailB)

    # Reducing the transparency of imageB.
    setTransparency(thumbnailB, 255/2)
    # Ensuring that imageB overlays imageA
    thumbnailB.setDepth(1)
    
    # Finding the height and width of the images.
    width, height = thumbnailA.size()
    # Setting the canvas equal to the size of the images side by side plus some
    win = Canvas(width + 100, height + 100, "white", "Thumbnails")
    win.setAutoRefresh(False)
    # Moving both images on top of each other.
    thumbnailA.moveTo((width + 100)/2, (height + 100)/2)
    thumbnailB.moveTo((width + 100)/2, (height + 100)/2)
    # Adding the images to the canvas.
    win.add(thumbnailA)
    win.add(thumbnailB)
      
    # Finding the correct overlay of the images
    overLayX, overLayY = overLay(win, thumbnailA, thumbnailB)
    win.close()

    # Resizing image A and B
    imageA = makeNewSize(imageA, widthAna)
    imageB = makeNewSize(imageB, widthAna)

    # Find the width and height of desired
    widthDesired, heightDesired = imageA.size()

    # Fing the ratio of overlay in respect to new image size
    overLayaspectX = int((overLayX / width) * widthDesired)
    overLayaspectY = int((overLayY / width) * heightDesired)

    # Crop the images
    imageA, imageB = cropping(imageA, imageB, \
                              int(overLayaspectX), int(overLayaspectY))
    
    # Make images red and cyan
    imageA = threeDRightChannel(imageA)
    imageB = threeDLeftChannel(imageB)
        
    # Make the final image with fused pixels
    imageFinal = addImages(imageA, imageB)

    # Saving the image
    imageFinal.save(fileNameFinal)
   
    # Finding the height and width of the final image.
    width2, height2 = imageFinal.size()
    # Setting the canvas equal to the size of the Final image plus some
    win2 = Canvas(width2 + 100, height2 + 100, "white", "ThreeD image!!!")
    # Moving the image to the center of the canvas
    imageFinal.move((width2 + 100)/ 2, (height2 + 100)/ 2)
    win2.add(imageFinal)
    
    # Make win2 only close with a mouse click
    done = False
    while not done:
        if (win2.wait().getDescription()) == "mouse click": 
            done = True
    win2.close()
        
if __name__ == "__main__":
    makeAnaglyph()
    
    
           
