#this script will create "country" and "decor" directories 
#with subfolders filled with images with corresponding categories ( to classify by Country or Decor)
import pandas as pd
from PIL import Image
import os
import shutil

#path to traditional-decor-patterns direcotry
# enter path as in example: decor_path='foo/foo2/bar/traditional-decor-patterns'
decor_path= ' '

df = pd.read_csv(decor_path+"/decor.csv")

print("entries type: "+" , ".join(str(x) for x in df.type.unique()))

#deleting pattern type from data frame, as said in exercise clasificator must contain only products
df = df[df['type'] == 'product']

print("Country categories: "+" , ".join(str(x) for x in df.country.unique()))

print("Decor categories: "+" , ".join(str(x) for x in df.decor.unique()))

#create direcotires for categories
main_dir='country'
if not os.path.exists(main_dir):
    os.makedirs(main_dir)
for directory in set(df.country):
    if not os.path.exists(main_dir+'/'+directory):
        os.makedirs(main_dir+'/'+directory)

main_dir='decor'
if not os.path.exists('decor'):
    os.makedirs('decor')
for directory in set(df.decor):
    if not os.path.exists(main_dir+'/'+directory):
        os.makedirs(main_dir+'/'+directory)

#create direcotires for jpeg images
if not os.path.exists('jpegs'):
    os.makedirs('jpegs')

#paths do image direcotires, png and jpegs
png_path = decor_path+'/decor'
jpeg_path= 'jpegs'

#converting .png to .jpg for retrain.py
for i in range(len(df)):
    im = Image.open(png_path+'/'+df.iloc[i].file)
    im = im.convert("RGB")
    im.save(jpeg_path+'/'+df.iloc[i].file+'.jpg', 'JPEG')

#copy images to respective category directories
for i in range(len(df)):
    shutil.copy2('jpegs/'+df.iloc[i].file+'.jpg', 'country/'+df.iloc[i].country)
    shutil.copy2('jpegs/'+df.iloc[i].file+'.jpg', 'decor/'+df.iloc[i].decor)