from PIL import Image
image = 'forextra1.png'

img = Image.open(image)


bounds1 = (0 ,0 , 1900 , 1200)

        # Crop the image
img = img.crop(bounds1)

img.save(image)



