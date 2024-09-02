import tqdm
import sys

def export_image(image_data):
    w, h = len(image_data[0]), len(image_data)
    header = f"P6\n{w} {h}\n255\n".encode("ascii")
    body = []
    for row in image_data:
        for col in row:
            r, g, b = col
            body.append(bytes((r, g, b)))
    return header + b"".join(body)


def write_header(w, h):
    sys.stdout.buffer.write(f"P6\n{w} {h}\n255\n".encode("ascii"))


def write_color(r,g,b):
    sys.stdout.buffer.write(bytes((r, g, b)))


def test(size):
    data = []
    for i in tqdm.tqdm(range(size)):
        row = []
        for j in range(size):
            row.append((int((i / size) * 255), 0, int((j / size) * 255)))
        data.append(row)
    open("test.ppm", "wb").write(export_image(data))
