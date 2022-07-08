import colorsys
from PIL import Image
import datetime
import sys
import os


def get_dominant_color(image):

    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')

    #生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))

    color_prefix = 'rgb(%d, %d, %d)'
    max_score = 0  #原来的代码此处为None
    dominant_color = 0  #原来的代码此处为None，但运行出错，改为0以后 运行成功，原因在于在下面的 score > max_score的比较中，max_score的初始格式不定

    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue

        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

        y = (y - 16.0) / (235 - 16)

        # 忽略高亮色
        if y > 0.9:
            continue

        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count

        if score > max_score:
            max_score = score
            dominant_color = toHex(255 - r, 255 - g, 255 - b)

    return dominant_color


def toHex(r, g, b):
    color = "#"
    color += str(hex(r)).replace('x', '0')[-2:]
    color += str(hex(g)).replace('x', '0')[-2:]
    color += str(hex(b)).replace('x', '0')[-2:]

    return color


today = datetime.date.today()
folder_index = sys.argv[1]

upload_dir = os.getenv('YOUTUBE_FILE_PATH') + '/upload'
cover_path = '%s/%s/%s/cover.png' % (upload_dir, today, folder_index)
print(get_dominant_color(Image.open(cover_path)))