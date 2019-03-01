from metrics import * 


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