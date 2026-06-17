from PIL import Image

images = [
 "pacman_back1.png",
 "pacman_back2.png",
 "pacman_back3.png",
 "pacman_back4.png",
 "pacman_back5.png",
 "pacman_back6.png",

 "pacman_face1.png",
 "pacman_face2.png",
 "pacman_face3.png",
 "pacman_face4.png",
 "pacman_face5.png",
 "pacman_face6.png",

 "pacman_side1.png",
 "pacman_side2.png",
 "pacman_side3.png",
 "pacman_side4.png",
 "pacman_side5.png",
 "pacman_side6.png",

 "pacman_side7.png",
 "pacman_side8.png",
 "pacman_side9.png",
 "pacman_side10.png",
 "pacman_side11.png",
 "pacman_side12.png",

]

rows = 4
cols = 6
w, h = 250, 250

sheet = Image.new("RGBA", (cols * w, rows * h))

for i, path in enumerate(images):
    img = Image.open(path)
    col = i % cols
    row = i // cols
    sheet.paste(img, (col * w, row * h))

sheet.save("spritesheet.png")
