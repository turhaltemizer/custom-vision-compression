# Compress a model exported from Custom Vision Service

Sometimes you might face such business cases when you need to use a Machine Learning model on a mobile device. However, there is a possibility to rest against restrictions on the size of the model to be placed on a device.  
[Microsoft Custom Vision Service](https://www.customvision.ai) allows you to easily customize your own state-of-the-art computer vision models for your unique use case. And this repository will guide you through the ways of Custom Vision exported models compression. 

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
We use a subset of [COCO](http://cocodataset.org/#home) dataset for our experiments. You don't need to download the whole dataset to reproduce our experiments. The data will be automatically loaded during the notebook execution, however it requires some preparation work. 
```bash
# Download and unpack the annotation file
$ wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
$ unzip annotations_trainval2017.zip
$ rm -rf annotations_trainval2017.zip
```

Open [model-compression](https://github.com/vJenny/custom-vision-compression/blob/master/model-compression.ipynb) notebook and go through its cells.  
You need to create your own [Custom Vision](https://www.customvision.ai) Model in case you want to test the API and provide the notebook with your credentials. You can find all the exported models in the [models](https://github.com/vJenny/custom-vision-compression/tree/master/models) folder.  

## Usage 
To reproduce this experiment on your own dataset, you need to create your own [Custom Vision](https://www.customvision.ai) account and [export compact models](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-your-model). Then put all the exported models into **models/coreml** and **models/tflite** folders respectively.  
The only thing you should carry about is your dataset mark-up process. To make this step easier, we usually use the [VoTT](https://github.com/Microsoft/VoTT) tool. 

## Results
Taking everything into consideration, we can come up with the following conclusion: 
* Compression of the mentioned model is **possible** with an insignificant loss of accuracy, however the loss of significant digits causes some fluctuation. 
* In case of **CoreML** (iOS platform), we have the following options: **16FP format (22Mb)** and **8FP format (11Mb)**. The second one is better in terms of the expected size, however it inferiors in quality. 
* As for the **TFLite model** (Android platform), the only possible option is to quantize the model to **8FP format (11Mb)**. 
* **Custom Vision API** works a bit better than all the exported models. 
   

<table>
<tr><th> Online Custom Vision Predictions </th><th> Original CoreML Predictions (43Mb) </th><th> Original TFLite Predictions (43Mb) </th></tr>
<tr><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|0.96667|0.14146 |
|dog|0.70833|0.2602|

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|1.0|0.087805|
|dog|0.7377|0.22959|

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|1.0|0.087805|
|dog|0.76271|0.22959|

</td></tr>

<tr><th>  </th><th> CoreML 16FP Predictions (22Mb) </th><th> TFLite 8FP Prediction (11Mb)  </th></tr>
<tr><td>


</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|1.0|0.087805|
|dog|0.7377|0.22959|

</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|1.0|0.087805|
|dog|0.74242|0.25|

</td></tr>

<tr><th>  </th><th> CoreML 8FP Predictions (11Mb) </th><th>  </th></tr>
<tr><td>


</td><td>

| Tag | Precision | Recall|
|--|--|--|
|cat|0.31683|0.1561|
|dog|0.65455|0.18367|

</td><td>


</td></tr>
</table>

❗️ The model was trained on a small dataset, so it's not well trained. The main objective of this project is not to train a perfect model, but to compare compressed models and create a reproducible example on an open dataset.
