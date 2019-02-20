from pycocotools.coco import COCO
import skimage.io as io
from tqdm import tqdm
from os.path import join, exists
from os import makedirs

train_dir = 'data/train'
test_dir = 'data/test'
data_dir = 'data'

n_train = 100
n_test = 10
coco = COCO('annotations/instances_val2017.json')

# Create train and test folders
if not exists(data_dir):
    makedirs(data_dir)
    makedirs(train_dir)
    makedirs(test_dir)
else:
    print("Data directory already exists") 

# Get cats and dogs categories
catImgIds = coco.getImgIds(catIds=coco.getCatIds(catNms=['cat']))
dogImgIds = coco.getImgIds(catIds=coco.getCatIds(catNms=['dog']))

train_imgs = coco.loadImgs(catImgIds[:n_train] + dogImgIds[:n_train])
test_imgs = coco.loadImgs(catImgIds[n_train:(n_train + n_test)] + dogImgIds[n_train:(n_train + n_test)])

# Save images 
for img in tqdm(train_imgs):
    I = io.imread(img['coco_url'])
    io.imsave(fname=join(train_dir, img['coco_url'].split('/')[-1]), arr=I)

for img in tqdm(test_imgs):
    I = io.imread(img['coco_url'])
    io.imsave(fname=join(test_dir, img['coco_url'].split('/')[-1]), arr=I)
   
print("Done")