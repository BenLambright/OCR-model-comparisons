# OCR models Evalutation Report -- parseq, tesseract (v4 & v5), and doctr

### Introduction
The following repo provides 20 sample images from slates from public broadcasting. We determine which of the following models parseq, tesseract (v4 & v5), and doctr most efficiently and effectively transcribe these images. We conclude that doctr is the most effective, but tesseract4 is the most efficient if running on CPU.

### Data
The images/ directory includes the images used for these experiments. These images came from a [dataset](https://www.kaggle.com/datasets/madisoncourtney/transcribed-slates) from Kaggle of transcribed slates, so that we can compare our results to the annotator's transcriptions.

### Pipeline
Because this is a CLAMS project, I include some mmif files that store the timepoints at which these slates would be in the source videos they came from. The `mp4-mmifs` are the original source videos in mmif file format, and the `swt-mmifs` are the timepoint predictions.

### Evaluation
In order to compare all of these OCR models, I wrote the script `ocr-eval.py` to compare all of the models to each other. 

#### parseq
In a separate script and on Hugging Face's online [demo](https://huggingface.co/spaces/baudm/PARSeq-OCR), parseq consistently proved that it could not handle images with multiple lines of text on a single image. If you look at the demo, all of the example images are one line of text (either vertical or horizontal), and whenever I put in images that were greater than 1-2 lines, the model was completely wrong (both on the demo and when running the model locally). This is also consistent with the parseq app for clams chyrons, which automatically snips the image it's processing to be smaller in order for parseq to handle the single line of text. Because of all this, I concluded parseq is not suitable for slates and did not include it in the evaluation script.

#### tesseract4
Tesseract4 is the default version in the tesseract CLAMS app.

#### tesseract5
Tesseract5 (specifically 5.5) is the newest version of the tesseract model. The CLAMS app was not able to support it yet, so I had to run the files locally on my computer, which is why I have put all of the tesseract5 output files here.

#### doctr
Supposedly the best but slowest model for OCR, we have a CLAMS app for it.

### Results
We used CER from the `jiwer` package to test the predictions of each model output to the gold transcription. The results were as follows in percent:

| tesseract4 | tesseract5 | doctr   |
|------------|------------|---------|
| 35.4       | 18.5       | 9.61    |

### Current Limitations with CLAMS Apps
While tesseract5 clearly performs better thant tesseract4, it is currently not supported by the CLAMS Apps. Given this performance difference, the next step will likely be updating the [tesseract](https://github.com/clamsproject/app-tesseractocr-wrapper/tree/main) CLAMS app.


