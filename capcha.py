import pytesseract
import sys
import argparse
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output


def resolve(path):
    check_output(['convert', path, '-resample', '700', path])
    return ''.join(c for c in pytesseract.image_to_string(Image.open(path)) if c.isdigit())


if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path',help = 'Captcha file path')
    args = argparser.parse_args()
    path = args.path
    print('Resolving Captcha')
    captcha_text = resolve(path)
    print('Extracted Text',captcha_text)
