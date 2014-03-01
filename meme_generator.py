"""Meme generator.
This a fairly basic Meme generator, with massive room for improvement."""
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import os.path
from math import ceil
import textwrap

impact = "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf"

class MemeGenerator(object):
    START_SIZE = 48
    INTERLINE = 4
    Y_OFFSET = 5
    X_OFFSET = 15
    MIN_SIZE = 22

    def __init__(self, image):
        self.img = Image.open(image)
        self.extension = os.path.splitext(image)[1]
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.maxWidth = self.width - (self.X_OFFSET * 2) # times 2 because from left and right

    def add_text(self, text1, text2, path, number):
        self.draw = ImageDraw.Draw(self.img)
        self.handle_text(self.Y_OFFSET, text1)
        self.handle_text(self.height - 60, text2, True)
        self.outname = datetime.now().strftime("%d%m%Y") + "-" + str(number) + self.extension
        self.img.save(path + self.outname)

    def get_file_name(self):
        return self.outname

    def handle_text(self, y, text, lower = False, current_size = 48):
        font = ImageFont.truetype(impact, current_size)
        while font.getsize(text)[0] > self.maxWidth and current_size >= self.MIN_SIZE:
            current_size = current_size - 1
            font = ImageFont.truetype(impact, current_size)
        # Ok, too long...
        if current_size < self.MIN_SIZE:
            font = ImageFont.truetype(impact, self.MIN_SIZE)
            line_height = font.getsize(text)[1] + self.INTERLINE
            potential_lines = ceil(float(font.getsize(text)[0]) / self.maxWidth)
            lines = textwrap.wrap(text, width = len(text) / potential_lines)
            count = 0
            if lower:
                y = self.height - self.Y_OFFSET
                y = y - (len(lines) * line_height)

            for line in lines:
                self.print_at(font, line, y + (line_height * count))
                count = count + 1
        else:
            self.print_at(font, text, y)

    def print_at(self, font, text, y):
        x = self.X_OFFSET + ((self.maxWidth) / 2) - (font.getsize(text)[0] / 2)
        # Border
        self.draw.text((x-1,y), text, (0, 0, 0), font=font)
        self.draw.text((x+1,y), text, (0, 0, 0), font=font)
        self.draw.text((x-1,y-1), text, (0, 0, 0), font=font)
        self.draw.text((x+1,y-1), text, (0, 0, 0), font=font)
        self.draw.text((x,y-1), text, (0, 0, 0), font=font)
        self.draw.text((x,y+1), text, (0, 0, 0), font=font)
        self.draw.text((x-1,y+1), text, (0, 0, 0), font=font)
        self.draw.text((x+1,y+1), text, (0, 0, 0), font=font)
        self.draw.text((x,y), text, (255, 255, 255), font=font)
