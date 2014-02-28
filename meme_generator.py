"""Meme generator.
This a fairly basic Meme generator, with massive room for improvement."""
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

impact = "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf"

class MemeGenerator(object):
    START_SIZE = 48
    def __init__(self, image):
        self.img = Image.open(image)
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        self.maxWidth = self.width - 15

    def add_text(self, text1, text2, outname):
        self.draw = ImageDraw.Draw(self.img)
        self.handle_text(5, text1)
        self.handle_text(self.height - 50, text2)
        self.img.save(outname)

    def handle_text(self, y, text):
        font = ImageFont.truetype(impact, self.START_SIZE)
        while font.getsize(text)[0] > self.maxWidth and self.START_SIZE > 16:
            font = ImageFont.truetype(impact, self.START_SIZE)
        # Ok, too long...
        if self.START_SIZE < 16 and textIs:
            font = ImageFont.truetype(impact, 16)
            if text_is_cuttable(text):
                text_displayed = cut_text(text)
                handle_text(y, text_diplayed[0], 16)
                handle_text(y + font.getsize(text)[1], text_diplayed[1], 16)
                # If text is not cuttable, we do nothing : we're doomed. 
                # TODO : add some exception, this might be Python, but we're not animals.
                # We found the right size, nice
        else:
            x = 15 + (self.maxWidth / 2) - (font.getsize(text)[0] / 2)

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
         
def text_is_cuttable(text):
    t =  text.split(' ')
    if len(t) > 0:
        return True
    return False

def cut_text(text):
    t = text.split(' ')
    middle = len(text_diplayed)/2
    return [t[len/2:], t[:len/2]]
