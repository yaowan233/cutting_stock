from item import Item
from generate_pattern import W, L
from PIL import Image, ImageDraw
import random


def draw(ans: tuple[Item]) -> None:
    img = Image.new("RGB", (L, W))
    draw = ImageDraw.Draw(img)
    for item in ans:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for i in item.place:
            for num in range(i[2]):
                draw.rectangle(
                    (
                        i[0] + num * item.length,
                        i[1],
                        i[0] + (num + 1) * item.length,
                        i[1] + item.width,
                    ),
                    fill=color,
                    outline=(155, 155, 155),
                    width=10,
                )
    img.show()
