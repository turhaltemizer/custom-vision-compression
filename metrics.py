import mPyPl as mp

def intersection_over_union(boxA, boxB):
    x1, y1, w1, h1 = boxA
    x2, y2, w2, h2 = boxB
    # compute coords of intersection
    xA = max(x1, x2)
    yA = max(y1, y2)
    xB = min(x1+w1, x2+w2)
    yB = min(y1+h1, y2+h2)
    # compute the area of intersection rectangle
    interArea = max(0, xB-xA) * max(0, yB-yA)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(w1*h1 + w2*h2 - interArea)
    # return the intersection over union value
    return iou


def precision_recall(data, cls, prob_threshold, iou_treshold, pred_field='predictions', gt_field='ground_truth'):
    TP = 0.0 
    TPFP = 0.0 # total positive results / pred
    TPFN = 0.0 # total existing cases / rel
    for obj in data: 
        ground_truth = (
            obj[gt_field]
            | mp.where(lambda x: x['tag'] == cls)
            | mp.as_list
        )
        TPFN += len(ground_truth)
        predictions = (
            obj[pred_field] 
            | mp.where(lambda x: x['tag'] == cls and x['prob'] > prob_threshold) 
            | mp.as_list
        )
        for gt_box in ground_truth:
            pred_boxes = (
                predictions 
                | mp.apply(['x1', 'y1', 'width', 'height'], 'iou', lambda x: 
                           intersection_over_union(x, (gt_box['x1'], gt_box['y1'], gt_box['width'], gt_box['height'])))
                | mp.filter('iou', lambda x: x < iou_treshold)
                | mp.as_list
            )
            if len(pred_boxes) > 0:
                TP += 1
                TPFP += len(pred_boxes)
    return (
        float(TP > 0) if TPFP == 0 else TP / TPFP, 
        float(TP > 0) if TPFN == 0 else TP / TPFN
    )   