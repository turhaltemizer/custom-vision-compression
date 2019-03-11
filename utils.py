from metrics import * 
from pipe import Pipe
from PIL import Image
from os.path import join
import mPyPl as mp


def cv_prediction_as_dict(prediction, width=None, height=None):
    return {
        'tag' : prediction.tag_name,
        'prob' : prediction.probability,
        'x1' : prediction.bounding_box.left * width if width else prediction.bounding_box.left,
        'y1' : prediction.bounding_box.top * height if height else prediction.bounding_box.top,
        'width' : prediction.bounding_box.width * width if width else prediction.bounding_box.width,
        'height' : prediction.bounding_box.height * height if height else prediction.bounding_box.height
    }


def format_dict(prediction, width=None, height=None):
    return {
        'tag' : prediction['tagName'],
        'prob' : prediction['probability'],
        'x1' : prediction['boundingBox']['left'] * width if width else prediction['boundingBox']['left'],
        'y1' : prediction['boundingBox']['top'] * height if height else prediction['boundingBox']['top'],
        'width' : prediction['boundingBox']['width'] * width if width else prediction['boundingBox']['width'],
        'height' : prediction['boundingBox']['height'] * height if height else prediction['boundingBox']['height']
    }


def print_report(stream, input_tags, prob_thresh, overlap_thresh, pred_field='predictions', gt_field='ground_truth'):
    top = '{:15.12} | {:^12.10} | {:^12.10}'.format("Tag", "Precision", "Recall")
    print(top)
    print('-' * len(top))
    for tag in input_tags:
        precision, recall = precision_recall(stream, tag, prob_thresh, overlap_thresh, pred_field=pred_field, gt_field=gt_field)
        print('{:15.12} | {:^12.5} | {:^12.5}'.format(tag, float(precision), float(recall)))
     

@Pipe
def apply_quantized_model(stream, data_dir, model, dest_field):
    return (
        stream 
        | mp.apply('filename', dest_field + '_raw', lambda x: model.predict_image(Image.open(join(data_dir, x))))
        | mp.apply([dest_field + '_raw', 'width', 'height'], dest_field, lambda x: x[0]
            | mp.select(lambda p: format_dict(p, x[1], x[2]))
            | mp.as_list
        )
        | mp.delfield([dest_field + '_raw'])
    ) 