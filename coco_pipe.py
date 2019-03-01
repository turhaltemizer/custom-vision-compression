from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region
from pycocotools.coco import COCO
import mPyPl as mp
from os.path import join


def bbox_to_dict(bbox, tag):
    x, y, w, h = bbox
    return {
        'x1' : x,
        'y1' : y,
        'width' : w,
        'height' : h,
        'tag' : tag
    }


def most_common(lst):
    return max(lst, key=lst.count)


def get_coco_stream(tags, ann_file, data_dir, threshold=0.1):
    coco = COCO(ann_file)
    catIds = coco.getCatIds(catNms=tags)
    imgIds = sum([coco.getImgIds(catIds=catId) for catId in catIds], [])
    stream = (
        coco.loadImgs(imgIds)
        | mp.as_field('meta')
        | mp.apply('meta', 'width', lambda x: x['width'])
        | mp.apply('meta', 'height', lambda x: x['height'])
        | mp.apply('meta', 'url', lambda x: x['coco_url'])
        | mp.apply('meta', 'filename', lambda x: x['file_name'])
        | mp.apply('meta', 'anns_ids', lambda x: coco.getAnnIds(imgIds=x['id'], catIds=catIds, iscrowd=None))
        | mp.apply('anns_ids', 'anns', lambda x: coco.loadAnns(x))
        | mp.apply('anns', 'ground_truth', lambda x: x 
            | mp.select(lambda m: bbox_to_dict(m['bbox'], coco.cats[m['category_id']]['name'])) 
            | mp.as_list
         )
        | mp.apply('ground_truth', 'class_id', lambda x: most_common(x
            | mp.select(lambda m: m['tag'])
            | mp.as_list
        ))
        | mp.iter('meta', lambda x: coco.download(data_dir, [x['id']]))
        | mp.delfield(['meta', 'anns_ids', 'anns'])
    )
    return stream


def coco_to_custom_vision(stream, project_id, trainer, data_dir):
    stream = stream | mp.as_list
    tags = stream | mp.select_field('class_id') | mp.dedup() | mp.as_list
    cv_tags = { tag : trainer.create_tag(project_id, tag) for tag in tags }

    stream = (
        stream
        | mp.apply(['width', 'height', 'ground_truth'], 'ground_truth', lambda x: 
            x[2] 
            | mp.where(lambda box: (box['width'] >= x[0] * 0.1) and (box['height'] >= x[1] * 0.1))
            | mp.as_list
        )
        | mp.filter('ground_truth', lambda x: len(x) > 0)  
        | mp.apply(['width', 'height', 'ground_truth'], 'regions', lambda x: 
            x[2] 
            | mp.select(lambda box:
                Region(
                    tag_id=cv_tags[box['tag']].id,
                    left=box['x1'] / x[0],
                    top=box['y1'] / x[1],
                    width=box['width'] / x[0],
                    height=box['height'] / x[1])
                )
            | mp.as_list
        )
        | mp.apply(['filename', 'regions'], 'tagged_img', lambda x: 
            ImageFileCreateEntry(
                name=x[0], 
                contents=open(join(data_dir, x[0]), mode="rb").read(), 
                regions=x[1])
            )
        | mp.as_list
    )
    tagged_images_with_regions = stream | mp.select_field('tagged_img') | mp.as_list
    for i in range(0, len(tagged_images_with_regions), 50):
        trainer.create_images_from_files(project_id, images=tagged_images_with_regions[i:i + 50])