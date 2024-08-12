from helpers.customStack import Stack
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import os
import json

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

def get_new_image(given_values, to_find, questionNumber = 1):
    
    folder_path = 'meta'
    ouput_folder_path = "images"
    meta_data = None

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(folder_path, filename)
            
            # Open the JSON file
            with open(file_path, 'r') as json_file:
                # Load and print the content
                tmp_meta_data = json.load(json_file)
                if tmp_meta_data['toFind'] == to_find:
                    meta_data = tmp_meta_data

    if meta_data:
        image_path = meta_data["image_path"]

        img = cv2.imread(image_path)

        old_given_vals = meta_data["givenValues"]

        # instance text detector
        reader = easyocr.Reader(['en'], gpu=False)

        # detect text on image
        text_ = reader.readtext(img)

        threshold = 0.25

        for t_, t in enumerate(text_):
            updated_text = ''
            bbox, text, score = t

            for k in old_given_vals:
                if str(old_given_vals[k]) in text:
                    updated_text = str(given_values[k]) + ' cm'

            if score > threshold:
                x, y = bbox[0]
                w = bbox[1][0] - x
                h = bbox[2][1] - y
                img = remove_text(img, x, y , w, h)
                cv2.putText(img, updated_text, bbox[3], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        plt.axis('off')
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        name = f'{ouput_folder_path}/right_triangle_{questionNumber}.png'
        plt.savefig(name)  # Save as image
        return name
    return None


if __name__ == "__main__":
    given_values = {'base': 4, 'height': 12}
    # langchain_agent()
    print(get_new_image(given_values, "hypotenuse", 3))