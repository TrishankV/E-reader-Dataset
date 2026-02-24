from pdf2image import convert_from_path
import pytesseract
import os 
# Convert PDF pages into images
# pages = convert_from_path("agilecut.pdf", dpi=300)

# pages = convert_from_path("cloudopscut.pdf" , dpi = 300)

pages = convert_from_path("leadershipcut.pdf" , dpi = 300)

text_output = ""

for i, page in enumerate(pages):
    image_path = f"page_{i}.png"
    page.save(image_path, "PNG")

    # Extract text using Tesseract
    text_output += pytesseract.image_to_string(image_path, lang="eng")
    text_output += "\n\n--- PAGE BREAK ---\n\n"

    
    os.remove(image_path)
    print(f"Deleted {image_path}")

# Save output
with open("leadersjip.txt", "w") as f:
    f.write(text_output)

print("OCR complete! Text saved to output.txt")