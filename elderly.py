## Work in a new folder
import os 
import json
import math
import cv2 as cv
from glob import glob

dire={'images':os.path.join('images'),
     'labels':os.path.join('labels'),
     'source':os.path.join('source_images3')}

for key,value in dire.items():
    if not os.path.isdir(value):
        print('The path ',value,"doesn't exist")
        os.makedirs(value)

        
##The labels and images folder should contains folder containing folders of 
#images and thier respective json files in labels folder


##The labels and images folder should contains folder containing folders of 
#images and thier respective json files in labels folder

#This directory is for writing annotation files in txt format
valid_images_dire=os.path.join(dire['source'],'valid_images.{}'.format('txt')).replace("\\","/") 

for folder in os.listdir(dire['images']):
    json_folder_name=folder.split('.')[0]+'.json'
    json_fullpath=os.path.join(dire['labels'],json_folder_name).replace("\\","/")
    IMG_FPS=float(os.listdir(os.path.join(dire['images'],folder))[1].split('.')[0].split("_")[-1])-float(os.listdir(os.path.join(dire['images'],folder))[0].split('.')[0].split("_")[-1])
    
    with open(json_fullpath) as file:
        data=json.load(file)
    
    fps=data['annotations']['fps']
    start_frame=data['annotations']['object'][0]['startFrame']
    end_frame=data['annotations']['object'][0]['endFrame']
    img_startframe=math.floor(start_frame/(fps*IMG_FPS))
    img_endframe=math.ceil(end_frame/(fps*IMG_FPS))
    
    with open(valid_images_dire,'a') as file:
        file.write(folder)
        file.write('\n')
        file.write('{} {}'.format(str(img_startframe),str(img_endframe)))
        file.write('\n')
        file.write('\n')
        
        
    for n,img_dire in enumerate(glob(os.path.join(dire['images'],folder)+'/*.jpg')):
        
        img_dire=img_dire.replace("\\","/")
        img=cv.imread(img_dire)
        if type(img)==None:
            continue
        target_dire_folder=os.path.join(dire['source'],folder).replace("\\","/")
        if not os.path.exists(target_dire_folder):
            os.makedirs(target_dire_folder)
        target_img_path=os.path.join(target_dire_folder,"{:05d}.{}".format(n,'jpg')).replace("\\","/") 
        
        cv.imwrite(target_img_path,img)
            
    
            