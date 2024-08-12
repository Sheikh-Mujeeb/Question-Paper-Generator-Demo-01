from helpers.customStack import Stack
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np


def remove_text(image, x, y, w, h):
    # Create a mask for inpainting
    mask = np.zeros(image.shape[:2], np.uint8)
    mask[y:y+h, x:x+w] = 255
    # Perform inpainting to remove the text
    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_NS)
    return inpainted_image

def get_updated_image(imagePath : str, base, height, questionNumber):
  # read image
  image_path = imagePath

  img = cv2.imread(image_path)

  stack = Stack()

  # Push elements onto the stack
  stack.push(str(base) + ' cm')
  stack.push(str(height) + ' cm')

  # instance text detector
  reader = easyocr.Reader(['en'], gpu=False)

  # detect text on image
  text_ = reader.readtext(img)

  threshold = 0.25

  for t_, t in enumerate(text_):
      print(t)

      bbox, text, score = t

      if score > threshold:
          x, y = bbox[0]
          w = bbox[1][0] - x
          h = bbox[2][1] - y
          img = remove_text(img, x, y , w, h)
          cv2.putText(img, stack.pop(), bbox[3], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

  plt.axis('off')
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  name = f'right_triangle_{questionNumber}.png'
  plt.savefig(name)  # Save as image
  return name