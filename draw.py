from PIL import Image, ImageDraw
import random
from item import Item

log = 0


def draw(ans: tuple[Item], output=False, L=2440, W=1220) -> None:
    global log
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
    if output:
        img.save(f"output/{str(log)}.jpeg", quality=50)
        log += 1
    else:
        # img.show()
        ...
