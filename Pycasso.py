import requests
from time import sleep
from PIL import Image
import io

colors = [
    (255, 255, 255),
    (0, 85, 0),
    (0, 170, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 85, 255),
    (0, 170, 255),
    (0, 255, 255),
    (255, 0, 0),
    (255, 85, 0),
    (255, 170, 0),
    (255, 255, 0),
    (255, 0, 255),
    (255, 85, 255),
    (255, 170, 255),
    (0, 0, 0)]

def get_data(filename):
    original = Image.open(filename)
    w, h = original.size
    data = list(original.getdata())
    RGB = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(data.pop(0))
        RGB.append(row)
    return RGB

def regress(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            color = 15
            old_delta = 765
            for k in range(len(colors)):
                new_delta = abs(colors[k][0] - data[i][j][0]) + abs(colors[k][1] - data[i][j][1]) + abs(colors[k][2] - data[i][j][2])
                if old_delta > new_delta:
                    old_delta = new_delta
                    color = k
            data[i][j] = color
            assert 0 <= color <= 15, f"color out of range: {color}"
    return data

def post_pixel(x, y, color):
    headers = {"Cookie": "cia-nsa-metaverse-tracking-id=s%3ADkLz3pYSo-IoEE1YeleFZnBMKDC0_aPi.FwjF9sMoxu%2FbOtzEjTTbvzHZQSSa7PBSyv5LA4Z38sY"}
    payload = {"x": x, "y": y, "color": color}
    req = requests.post("https://jackhsullivan.com/place", headers = headers, json = payload)
    print(payload)
    sleep(0.1)

def paint(filename, x_start, y_start):
    data = get_data(filename)
    data = regress(data)
    for i in range(len(data)):
        for j in range(len(data[0])):
            post_pixel(x_start + j, y_start + i, data[i][j])
            print(f"Painting, {round(((i * len(data[0]) + j) / (len(data) * len(data[0]))) * 100, 2)}% done")

def get_board():
    req = requests.get("https://jackhsullivan.com/board", stream = True)
    stream = io.BytesIO(req.content)
    board = []
    for i in range(512):
        row = []
        for j in range(0, 512, 2):
            data = stream.read(1)
            data = int.from_bytes(data, "big")
            first_half = data >> 4
            second_half = data & 0x0f
            row.append(first_half)
            row.append(second_half)
        board.append(row)
    return board

def show_board():
    im = Image.new(size = (512, 512), mode = "RGB")
    board = get_board()
    for i in range(512):
        for j in range(512):
            im.putpixel((j, i), colors[board[i][j]])
    im.show()

def anti_grief(filename, x_start, y_start):
    data = get_data(filename)
    data = regress(data)
    board = get_board()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if board[i + y_start][j + x_start] != data[i][j]:
                post_pixel(j + x_start, i + y_start, data[i][j])

if __name__ == "__main__":
    while(True):
        anti_grief("bubbas.jpg", 401, 76)
        anti_grief("winston_sunset.jpg", 3, 359)
        sleep(60)
