# small helper to create a test sample if you don't have images
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("samples", exist_ok=True)
img = Image.new('RGB', (800, 400), color=(255,255,255))
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 28)
except:
    font = ImageFont.load_default()
text = """Patient: John Doe
DOB: 03/05/1980
Phone: +1-555-123-4567
Notes: Patient reports mild headache."""
d.text((30,30), text, fill=(0,0,0), font=font)
img.save("samples/sample1.jpg")
print("Saved samples/sample1.jpg")
