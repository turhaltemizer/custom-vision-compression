# Compress a model exported from Custom Vision Service

## Installation
1. Clone this repository.
```bash
$ git clone https://github.com/vJenny/custom-vision-compression.git
```
2. Install all files in the *requirements.txt* file.
```bash
$ pip install -r requirements.txt
```

## Testing
We use a subset of [COCO](http://cocodataset.org/#home) dataset for our experiments. You don't need to download the whole dataset to reproduce our experiments. 
```bash
# Download and unpack the annotation file
$ wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
$ unzip annotations_trainval2017.zip
$ rm -rf annotations_trainval2017.zip
# Run the data downloading script
$ python coco-load-pets.py
```

Open [model-compression](https://github.com/vJenny/custom-vision-compression/blob/master/model-compression.ipynb) notebook and go through its cells.  
You need to create your own [Custom Vision](https://www.customvision.ai) Model in case you want to test the API and provide the notebook with your credentials. You can find all the exported models in the [models](https://github.com/vJenny/custom-vision-compression/tree/master/models) folder.  

## Usage 
To reproduce this experiment on your own dataset, you need to do the following steps:
1. Mark up your dataset. To make this step easier, we've used [VoTT](https://github.com/Microsoft/VoTT) tool. 
2. Create your own [Custom Vision](https://www.customvision.ai) account and [export compact models](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-your-model).
3. Move your dataset to the **data** folder (don't forget about the **.json** file containing VoTT meta information). 
4. Put all the exported models into **models/coreml** and **models/tflite** folders respectively.

## Results


<table>
<tr><th> Online Custom Vision Predictions </th><th> Original CoreML Predictions (43Mb) </th><th> Original TFLite Predictions (43Mb) </th></tr>
<tr><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td></tr>

<tr><th>  </th><th> CoreML 16FP Predictions (22Mb) </th><th> TFLite 8FP Prediction (11Mb)  </th></tr>
<tr><td>


</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td></tr>

<tr><th>  </th><th> CoreML 8FP Predictions (11Mb) </th><th>  </th></tr>
<tr><td>


</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat| | |
|dog| | |

</td><td>


</td></tr>
</table>
