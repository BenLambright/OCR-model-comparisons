# OCR models Evalutation Report -- parseq, tesseract (v4 & v5), and doctr

### Introduction
The following repo provides 20 sample images from slates from public broadcasting. We determine which of the following models parseq, tesseract (v4 & v5), and doctr most efficiently and effectively transcribe these images. We conclude that doctr is the most effective, but tesseract4 is the most efficient if running on CPU.

### Data
The images/ directory includes the images used for these experiments. These images came from a [dataset](https://www.kaggle.com/datasets/madisoncourtney/transcribed-slates) from Kaggle of transcribed slates, so that we can compare our results to the annotator's transcriptions.

### Pipeline
Because this is a CLAMS project, I include some mmif files that store the timepoints at which these slates would be in the source videos they came from. The mp4-mmifs are the original source videos in mmif file format, and the swt-mmifs are the timepoint predictions.

### Evaluation
In order to compare all of these OCR models, I 

### Results

### Current Limitations with CLAMS Apps
