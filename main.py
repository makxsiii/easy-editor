#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN 
import os

workdir = ''

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'modifed'
        self.original_image = None
    
    def loadImage(self, dir, filename):
        self.filename = filename
        self.dir = dir
        dir = os.path.join(dir, filename)
        self.image = Image.open(dir)
        self.original_image = self.image.copy()
    
    def showImage(self, path):
        piximage = QPixmap(path)
        lw, lh = picture.width(), picture.height()
        scaled = piximage.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
        picture.setPixmap(scaled)
        picture.setVisible(True)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)    

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    
    def resetImage(self):
        self.image = self.original_image.copy()
        self.showImage(os.path.join(workdir, self.filename))

showimage = ImageProcessor()
  

def showChosenImage():
    if fails.currentRow() >= 0:
        filename = fails.currentItem().text()
        showimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, showimage.filename)
        showimage.showImage(image_path)
  
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extentions):
    result = []
    for results in files:
        for res in extentions:
            if results.endswith(res):
                result.append(results)
    return result

def showFilenamesList():
    extentions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extentions)
    fails.clear()
    for filename in filenames:
        fails.addItem(filename)

app = QApplication([])
main = QWidget()
main.resize(700, 500)
main.setWindowTitle('Easy Editor')

papka = QPushButton('Папка')
fails = QListWidget()
picture = QLabel('Картинка')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
contrast = QPushButton('Резкость')
baw = QPushButton('Ч/б')
save = QPushButton('Сохранить')
offfilters = QPushButton('Сбросить фильтры')

h1_line = QHBoxLayout()
v1_line = QVBoxLayout()
v2_line = QVBoxLayout()
h2_line = QHBoxLayout()

h2_line.addWidget(left)
h2_line.addWidget(right)
h2_line.addWidget(mirror)
h2_line.addWidget(contrast)
h2_line.addWidget(baw)
h2_line.addWidget(save)
h2_line.addWidget(offfilters)
v1_line.addWidget(papka)
v1_line.addWidget(fails)
v2_line.addWidget(picture)
h1_line.addLayout(v1_line, 30)
h1_line.addLayout(v2_line, 70)
v2_line.addLayout(h2_line)
main.setLayout(h1_line)

papka.clicked.connect(showFilenamesList)
left.clicked.connect(showimage.do_left)
right.clicked.connect(showimage.do_right)
mirror.clicked.connect(showimage.do_flip)
contrast.clicked.connect(showimage.do_sharpen)
baw.clicked.connect(showimage.do_bw)
save.clicked.connect(showimage.saveImage)
offfilters.clicked.connect(showimage.resetImage)

fails.currentRowChanged.connect(showChosenImage)  

main.show()
app.exec_()
