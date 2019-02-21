import sys
import tensorflow as tf
from tensorflow.contrib.lite.python.interpreter import Interpreter
from tensorflow.contrib.lite.python import interpreter
import numpy as np
from PIL import Image
from tflite.python.object_detection import ObjectDetection

MODEL_FILENAME = 'quantized_model.tflite'
LABELS_FILENAME = 'labels.txt'

class TFObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow
    """
    def __init__(self, model_path, labels):
        super(TFObjectDetection, self).__init__(labels)
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
            
    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float32)[:,:,(2,1,0)] # RGB -> BGR

        self.interpreter.set_tensor(self.input_details[0]['index'], inputs[np.newaxis,...])
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])

        return output[0]


def main(image_filename):
    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    od_model = TFObjectDetection(MODEL_FILENAME, labels)

    image = Image.open(image_filename)
    predictions = od_model.predict_image(image)
    print(predictions)
    
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('USAGE: {} image_filename'.format(sys.argv[0]))
    else:
        main(sys.argv[1])