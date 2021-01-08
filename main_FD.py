import cv2
import face_recognition
from PIL import Image
from numpy import average, dot, linalg

import os

####################################################
# face detection part


####################################################
# compare part
def get_thum(image, size=(64, 64), greyscale=False):
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        image = image.convert('L')
    return image


def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_thum(image1)
    image2 = get_thum(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res

image = face_recognition.load_image_file("image.jpg")
face_locations = face_recognition.face_locations(image)

for face_locations in face_locations:
	top,right,bottom,left = face_locations

#print face_locations
#for i in face_locations:
#	cv2.rectangle(image,(i[3],i[0]),(i[1],i[2]),color=(0,255,255),thickness=3)

cropped = image[top:bottom,left:right]

cv2.imwrite("/home/pi/result/result.jpg",cropped)
#image_result = face_locations
#image_result.save("/home/pi/result/result.jpg")

#boring
image1 = Image.open('/home/pi/result/result.jpg')
image2 = Image.open('/home/pi/database/boring.jpg')
cosin = image_similarity_vectors_via_numpy(image1, image2)
simi1 = cosin
print('Boring', simi1)

#hungry
image1 = Image.open('/home/pi/result/result.jpg') 
image2 = Image.open('/home/pi/database/hungry.jpg')
cosin = image_similarity_vectors_via_numpy(image1, image2)
simi2 = cosin
print('Hungry',simi2)

#uncomfortable
image1 = Image.open('/home/pi/result/result.jpg') 
image2 = Image.open('/home/pi/database/uncomfortable.jpg')
cosin = image_similarity_vectors_via_numpy(image1, image2)
simi3 = cosin
print('Uncomfortable',simi3)

#selection
if max(simi1,simi2,simi3) <= 0.40:
	print('Everything is fine!')
else:
	if simi1 == max(simi1, simi2, simi3):
		os.system('python /home/pi/mail_main1.py')
	else:
		if simi2 == max(simi1, simi2, simi3):
			os.system('python /home/pi/mail_main2.py')
		else:
			os.system('python /home/pi/mail_main3.py')

######################################################################
