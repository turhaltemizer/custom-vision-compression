# How to compress a model exported from Custom Vision Service

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
Open [model-compression](https://github.com/vJenny/custom-vision-compression/blob/master/model-compression.ipynb) notebook and go through cells. 

## Usage 

## Results