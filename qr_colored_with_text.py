import qrcode
from PIL import Image, ImageDraw, ImageFont

data = "https://www.youtube.com/@galaxyofgamesar"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # fixed typo: 'correction' → 'constants'
    box_size=10,
    border=4,
)

qr.add_data(data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color='black', back_color='white')

custom_text = "Subscribe: Galaxy Of Games AR"  # fixed typo: 'custome' → 'custom'

try:
    font = ImageFont.truetype("arial.ttf", 30)
except:
    font = ImageFont.load_default()

qr_width, qr_height = qr_img.size
new_height = qr_height + 50  # add space below QR for text

new_img = Image.new("RGB", (qr_width, new_height), "white")
new_img.paste(qr_img, (0, 0))

draw = ImageDraw.Draw(new_img)
text_width, text_height = draw.textsize(custom_text, font=font)  # fixed typo: 'text_heeight' → 'text_height'
text_position = ((qr_width - text_width) // 2, qr_height + 10)

draw.text(text_position, custom_text, font=font, fill="black")

new_img.save("qr_colored_with_text.png")

print("Colored QR with custom text saved as qr_colored_with_text.png")
