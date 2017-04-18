from PIL import Image
import os
import time

pic_folder = "/var/www/app_dancmc/mff/ocr_scripts/uploaded_screenshots"
total_files = 0
total_files_deleted = 0

start = time.time()
for filename in os.listdir(pic_folder):
    total_files +=1
    try:
        im = Image.open(filename)
        # print("w = "+str(im.size[0])+" & h = "+str(im.size[1]))
        if im.size[0]==1 and im.size[1]==1:
            os.remove(os.path.join(pic_folder, filename)) 
            total_files_deleted +=1
    except:
        pass

print("Total files : "+str(total_files))
print("Files deleted : "+str(total_files_deleted))
print("Time taken : "+str(int((time.time()-start)*1000))+" ms")
