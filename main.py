import cv2
import os
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import random

global isEatable
isEatable=True
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = FaceMeshDetector(maxFaces=1)
idList=[0,17,78,292]

folderEatable='Fruits/EATABLE'
listeatable=os.listdir(folderEatable)
folderNoneatable='Fruits/Noneatable'
listnoneatable=os.listdir(folderNoneatable)

eatables=[]
for object in  listeatable:
    eatables.append(cv2.imread(f'{folderEatable}/{object}',cv2.IMREAD_UNCHANGED))

noneatables=[]
for object in  listnoneatable:
    noneatables.append(cv2.imread(f'{folderNoneatable}/{object}',cv2.IMREAD_UNCHANGED))

currentobject=eatables[0]
pos=[300,0]
speed=5
def resetobject():
    global isEatable

    pos[0]=random.randint(100,1180)
    pos[1]=0

    randno=random.randint(0,1)
    if randno==0:
        isEatable=False
        currentobject=noneatables[random.randint(0,8)]
    else:
        currentobject=eatables[random.randint(0,8)]
        isEatable=True
    return currentobject

count=0
gameover=False
while True:

    success,img=cap.read()
    if gameover==False:
        img, faces = detector.findFaceMesh(img,draw=False)
        img=cvzone.overlayPNG(img,cv2.resize(currentobject,(100,100)),pos)
        pos[1]+=speed

        if pos[1]>520:
            currentobject=resetobject()

        if faces:
            face=faces[0]
            # for idNo,point in enumerate(face):
            #     cv2.putText(img,str(idNo),point,cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,0),1)
            # for id in idList:
            #     cv2.circle(img,face[id],5,(255,0,255),5)
            # cv2.line(img,(face[idList[0]]),(face[idList[1]]),(0,255,255),3)
            # cv2.line(img,(face[idList[2]]),(face[idList[3]]),(0,255,255),3)
            updown,_=detector.findDistance(face[idList[0]],face[idList[1]])
            leftright,_=detector.findDistance(face[idList[2]],face[idList[3]])
            ratio=int((updown/leftright)*100)
            # print(ratio)

            up=face[idList[0]]
            down=face[idList[1]]
            left=face[idList[2]]
            right=face[idList[3]]

            cx,cy=(up[0]+down[0])//2,(up[1]+down[1])//2
            # cv2.line(img,(cx,cy),(pos[0]+50,pos[1]+50),(255,0,255),3)

            distmouthobject,_=detector.findDistance((cx,cy),(pos[0]+50,pos[1]+50))
            print(distmouthobject)

            if(ratio>50):
                mouthstatus="Open"
            else:
                mouthstatus="Closed"
            print(mouthstatus)


            # cv2.putText(img, mouthstatus, (10,60), cv2.FONT_HERSHEY_COMPLEX,2, (255,  0,255), 2)
            if (distmouthobject<100) and ratio >50:
                if isEatable:
                    currentobject=resetobject()
                    count+=1
                else:
                    gameover=True
            cv2.putText(img, str(count), (10,60), cv2.FONT_HERSHEY_COMPLEX,2, (255, 0, 255), 2)

    else:
        cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 9, (255, 255, 0),10)

    cv2.imshow("Image",img)
    key=cv2.waitKey(1)
    if key==ord('r'):
        resetobject()
        gameover=False
        count=0
        currentobject=eatables[0]
        isEatable=True



    if (key & 0xFF == ord('x')):
        break
    cv2.destroyAllWindows
