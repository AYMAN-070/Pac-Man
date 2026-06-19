from PIL import Image

images = [
 "ghost1_back1.png",
 "ghost1_back2.png",
 "ghost1_back3.png",
 "ghost1_back4.png",
 "ghost1_back5.png",

 "ghost1_face1.png",
 "ghost1_face2.png",
 "ghost1_face3.png",
 "ghost1_face4.png",
 "ghost1_face5.png",

 "ghost1_side1.png",
 "ghost1_side2.png",
 "ghost1_side3.png",
 "ghost1_side4.png",
 "ghost1_side5.png",

 "ghost1_side6.png",
 "ghost1_side7.png",
 "ghost1_side8.png",
 "ghost1_side9.png",
 "ghost1_side10.png",

]

rows = 4
cols = 5
w, h = 250, 250

sheet = Image.new("RGBA", (cols * w, rows * h))

for i, path in enumerate(images):
    img = Image.open(path)
    col = i % cols
    row = i // cols
    sheet.paste(img, (col * w, row * h))

sheet.save("spritesheet.png")
