from PIL import Image

images = [
 "pacman_death1.png",
 "pacman_death2.png",
 "pacman_death3.png",
 "pacman_death4.png",
 "pacman_death5.png",
 "pacman_death6.png",
 "pacman_death7.png",
 "pacman_death8.png",

]

rows = 8
cols = 1
w, h = 600, 250

sheet = Image.new("RGBA", (cols * w, rows * h))

for i, path in enumerate(images):
    img = Image.open(path)
    col = i % cols
    row = i // cols
    sheet.paste(img, (col * w, row * h))

sheet.save("spritesheet.png")
