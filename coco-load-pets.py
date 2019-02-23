from pycocotools.coco import COCO
import skimage.io as io
from tqdm import tqdm
from os.path import join, exists
from os import makedirs


data_dir = 'data'
images_dir = join(data_dir, 'images')

n_train = 100
coco = COCO('annotations/instances_val2017.json')

# Create train and test folders
if not exists(data_dir):
    makedirs(data_dir)
else:
    print("Data directory already exists") 

# Get cats and dogs categories
catImgIds = coco.getImgIds(catIds=coco.getCatIds(catNms=['cat']))
dogImgIds = coco.getImgIds(catIds=coco.getCatIds(catNms=['dog']))

imgs = coco.loadImgs(catImgIds[:n_train] + dogImgIds[:n_train])


# Save images 
for img in tqdm(train_imgs):
    I = io.imread(img['coco_url'])
    io.imsave(fname=join(images_dir, img['coco_url'].split('/')[-1]), arr=I)
   
print("Done")