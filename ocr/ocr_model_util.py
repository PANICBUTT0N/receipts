import cv2

def should_resize_image(img_path: str) -> bool:
    """
    Checks if image at img_path should be resized based on the provided width and height.
    """
    img =  cv2.imread(img_path)
    height, width,_ = img.shape
    return width > 1500 or height > 1500

def resize_image(img_path: str, width: int = 0, height: int = 0) -> bool:
    """
    Loads an image from a path and resizes it to the given width and/or height 
    while maintaining aspect ratio if only one dimension is provided.
    Overwrites the image at img_path with the resized version.
    returns true if resizing was successful, false otherwise.
    """
    image = cv2.imread(img_path)

    if width == 0 and height == 0:
        return False

    h, w = image.shape[:2]
    if width == 0:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    elif height == 0:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    else:
        dim = (width, height)

    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_path, resized_image)
    return True

# greyscale image
def greyscale_image(img_path: str):
    """
    Converts the image at img_path to greyscale and overwrites the original image file.
    """
    image = cv2.imread(img_path)

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(img_path, grey)
