
import pytesseract

from PIL import Image



img = r"Shared_Responsibility_Model.png"

imge = Image.open(img)

text = pytesseract.image_to_string(img , lang="eng")

print(text)