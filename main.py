import urllib.request
import sys
import re
from pathlib import Path
import time


website = sys.argv[1]
output = 'output/' + sys.argv[2]


folderRegex = r'<a href="([0-9]+/)">'
fileRegex = r'<a href="([a-zA-Z.0-9_-]+)">'
reduceRegex = r'-([0-9]+)x([0-9]+)'


uploadFolder = '/wp-content/uploads/'


yearFolderHtml = urllib.request.urlopen(website + uploadFolder).read()
years = re.findall(folderRegex, str(yearFolderHtml))

folder = Path('output')
if folder.exists() and folder.is_file():
    folder.unlink()
if not folder.exists():
    folder.mkdir()

folder = Path(output)
if folder.exists() and folder.is_file():
    folder.unlink()
if not folder.is_dir():
    folder.mkdir()


for year in years:
    monthFolderHtml = urllib.request.urlopen(website + uploadFolder + year).read()
    months = re.findall(folderRegex, str(monthFolderHtml))
    for month in months:
        imageFolderHtml = urllib.request.urlopen(website + uploadFolder + year + month).read()
        images = re.findall(fileRegex, str(imageFolderHtml))
        for image in images:
            if not re.search(reduceRegex, image):
                print(year + month + image)
                img = Path('{}/{}'.format(output, image))
                if not img.exists:
                    open('{}}/{}'.format(output, image), 'x')
                urllib.request.urlretrieve(website + uploadFolder + year + month + image, '{}/{}'.format(output, image))
