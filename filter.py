import cv2
import math
import numpy as np

def get_lt(rt):
    x, y, _, _=rt
    return (x,y)
def get_rd(rt):
    x, y, w, h=rt
    return (x+w,y+h)
def get_center(rt):
    x, y, w, h=rt
    return (int(x+w/2), int(y+h/2))
def getw(rt):
    x, y, w, h=rt
    return w
def geth(rt):
    x, y, w, h=rt
    return h

def dis_center(rt0,rt1):
    pt0=get_center(rt0)
    pt1=get_center(rt1)
    return dis(pt0,pt1)

def dis(pt0,pt1):
    x0,y0=pt0
    x1,y1=pt1
    return math.sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))

'''
       x1
     _______
    |       \
 l1 |        \ 
    |___x2____\
 l2 |          \
    |___________\
         x3
l1/l2=(x2-x1)/(x3-x2)

'''
def is_right(rt0,rt1,rtnew):
    dis0_1=dis_center(rt0, rt1)
    dis1_new=dis_center(rt1, rtnew)
    new_w=getw(rtnew)
    new_h=geth(rtnew)

    rt0_w=getw(rt0)
    rt0_h=geth(rt0)
    print("rt0_w",rt0_w)
    print("rt0_h",rt0_h)

    rt1_w=getw(rt1)
    rt1_h=geth(rt1)
    print("rt1_w",rt1_w)
    print("rt1_h",rt1_h)

    square0=rt0_w*rt0_h
    square1=rt1_w*rt1_h

    flag=square0<square1
    
    # rt0 is more convince than rt2, so according to rt1 square to resize width/height
    rt1_new_w=rt0_w*math.sqrt(square1/square0)
    rt1_new_h=rt0_h*math.sqrt(square1/square0)

    rtnew_predict_w=0
    rtnew_predict_h=0

    if flag:
        # l2(x2-x1)/l1+x2
        rtnew_predict_w=dis1_new*(rt1_new_w-rt0_w)/dis0_1+rt1_new_w
        rtnew_predict_h=dis1_new*(rt1_new_h-rt0_h)/dis0_1+rt1_new_h
    else:
        # x1=x2-l1(x3-x2)/l2
        rtnew_predict_w=rt1_new_w-dis1_new*(rt0_w-rt1_new_w)/dis0_1
        rtnew_predict_h=rt1_new_h-dis1_new*(rt0_h-rt1_new_h)/dis0_1
    # new_w compare rtnew_predict_w
    # new_h compare rtnew_predict_h

def rectang(img,rt):
    cv2.rectangle(img,get_lt(rt),get_rd(rt),color,3)
    return img

def circ(img,rt):
    img=cv2.circle(img,get_center(rt),2,color,2)
    return img
    
rt1=(35,70,200,300)
rt2=(100,190,150,250)
rt3=(200,190,100,200)
rt=[rt1,rt2]
img = 255*np.ones((512,512,3),np.uint8)#生成一个空彩色图像
# img=cv2.imread("1.jpg")
print(img.shape)
# print(img.height)


color=(0,0,100)

# lt=(30,30)
# rb=(100,100)
print(get_center(rt[0]))
print(get_center(rt[0])[0])
print(get_center(rt[0])[1])
img=rectang(img,rt[0])
img=circ(img,rt[0])
img=rectang(img,rt[1])
img=circ(img,rt[1])
img=rectang(img,rt3)
img=circ(img,rt3)
# cv2.circle(img,100, color)
# 3 param is radius
# last param is line width
# cv2.circle (img,get_center(rt[0]),2,color,2)
# cv2.imshow("xx",img)
# cv2.waitKey()
print(get_center(rt[0]))
print("ccccc")
print(dis(rt2,rt1))

# print(dist.euclidean(get_center(rt[0]),get_center(rt[1])))