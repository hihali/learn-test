import PIL.Image as Image
import numpy as np
import os
import threading

'''
程序的目的是实现二维码和图像的融合
即用二维码给图像做掩码
使用numpy的掩码矩阵，just like：mask = x < 255
                                         mx = ma.array(x,mask=mask)
这是后话
'''
shape = (430, 430, 3)


class ImgThread(threading.Thread):
    rgbs = mask1 = mask2 = None

    def __init__(self, name, ID=0, *args):
        threading.Thread.__init__(self)
        self.name = name
        self.ID = ID  # 标记是那种处理
        self.fileName = args[0]

    def run(self):
        if self.ID == 0:
            ImgThread.shape, ImgThread.rgbs = \
                readImg(filename=self.fileName)
        if self.ID == 1:
            while True:
                print(shape)
                if shape is not None:
                    ImgThread.mask1, ImgThread.mask2 = \
                        readQD(filename=self.fileName, shape=shape)
                    break


def readImg(filename):
    '''
     读取图像
    :param filename: 图像的名字
    :return: 返回图像的矩阵数据，是一个np.array的三维数组
    '''

    imgPath1 = os.getcwd() + r'/img/' + filename
    im1 = Image.open(imgPath1).resize((430, 430))
    rgbs = np.array(im1, dtype=int)
    shape = rgbs.shape
    return shape, rgbs


def readQD(filename, shape):
    '''
    由于qd数据是一维的，将其转化为三维的
    :param filename: 文件名字
    :return:
    '''

    imgPath2 = os.getcwd() + r'/img/' + filename
    im2 = Image.open(imgPath2)

    qd = np.array(im2, dtype=int)
    qds = np.zeros(shape=shape,dtype=int)
    for i in range(3):
        qds[:, :, i] = qd
    qds = np.array(qds,dtype=int)

    mask1 = qds == 0
    mask2 = qds > 0
    return mask1, mask2


def main(rgbs=None, mask1=None, mask2=None):
    '''
    进行图像融合
    :param rgbs:
    :param mask1:
    :param mask2:
    :return:
    '''
    rgbs[mask2] = 100
    newImg = rgbs
    print('new',newImg)
    filePath = os.getcwd() + r'/img/I_Q.jpg'
    newImg = Image.fromarray(np.uint8(newImg))
    newImg.save(filePath)
    newImg.show()


if __name__ == '__main__':
    '''
    使用多线程
    使用多线程类来保存多线程的返回值
    '''

    imgName = 'timg.jpg'
    qdName = 'QD.jpg'
    t1 = ImgThread('Img', 0, imgName)
    t2 = ImgThread('QD', 1, qdName)
    for t in (t1, t2):
        t.start()
    for t in (t1, t2):
        t.join()
    main(rgbs=ImgThread.rgbs, mask1=ImgThread.mask1, mask2=ImgThread.mask2)
