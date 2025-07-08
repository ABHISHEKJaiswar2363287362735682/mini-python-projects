import qrcode
from PIL import Image

data = "https://www.youtube.com/@galaxyofgamesar"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

logo = Image.open('logo.png').convert("RGBA")

qr_width, qr_height = qr_img.size
logo_size = qr_width // 4  # Reduced to 1/4th to ensure scan reliability
logo = logo.resize((logo_size, logo_size))

pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

qr_img = qr_img.convert("RGBA")
mask = logo.split()[3]  # Extract alpha channel as mask

qr_img.paste(logo, pos, mask=mask)
qr_img.save("qr_code_with_logo.png")

print("QR Code with logo generated and saved as qr_code_with_logo.png")
