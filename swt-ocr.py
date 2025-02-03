# testing all the different kinds of ocr

IMAGE_PATH = "images/cpb-aacip-00ec5c2cf39_07557983_00065032_00065065.jpg"
gold_path = "img_arr_prog.js"



###         SETTING UP THE FILE         ###
import ast
with open(gold_path, "r") as file:
    golds = file.read()

golds = golds.replace("true", "True").replace("false", "False")
golds = ast.literal_eval(golds)
gold_output = [golds[0][5]]
print(gold_output)

###             DOCTR           ###
# imports for doctr
# !pip install python-doctr, mplcursors, matplotlib
from doctr.io import DocumentFile  # reading a document
from doctr.models import ocr_predictor  # getting the ocr model

print("loading doctr...")
model = ocr_predictor(pretrained=True)
single_img_doc = DocumentFile.from_images(IMAGE_PATH)

print("calculating result...")
result = model(single_img_doc)

print("printing results...")
json_output = result.export()
sentences = []
for page in json_output["pages"]:
    for block in page["blocks"]:
        for line in block["lines"]:
            words = [word["value"] for word in line["words"]]
            sentences.append(" ".join(words))

# print(sentences)
doctr_output = ["\n".join(sentences)]
print(doctr_output)

print()
print()
print()



###             JIWER           ###
# !pip install pytesseract
from PIL import Image
import pytesseract

print("running tesseract...")
tesseract_output = pytesseract.image_to_string(Image.open(IMAGE_PATH))
tesseract_output  = [tesseract_output]
print(tesseract_output)



print()
print()
print()

###         RUNNING JIWER        ###
from jiwer import cer

print("evaluating doctr...")
print(cer(gold_output, doctr_output))

print("evaluating tesseract...")
print(cer(gold_output, tesseract_output))


# conclusion with parseq: this model only works if you crop the image to just one line of text, which is impractical for slates. 
# Doctr is built off of it and seems to outperform it anyways.

# # imports for parseq
# import torch
# from PIL import Image
# from parseq.strhub.data.module import SceneTextDataModule

# # open image
# img = Image.open(IMAGE_PATH).convert('RGB')

# # have this run in the parseq directory
# import sys
# sys.path.append('parseq')

# # Load model and image transforms
# print("running parseq...")
# parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()
# img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)

# # Preprocess. Model expects a batch of images with shape: (B, C, H, W)
# img = img_transform(img).unsqueeze(0)

# logits = parseq(img)
# logits.shape  # torch.Size([1, 26, 95]), 94 characters + [EOS] symbol

# # Greedy decoding
# pred = logits.softmax(-1)
# label, confidence = parseq.tokenizer.decode(pred)
# print('Decoded label = {}'.format(label[0]))




# example: gold, doctr, tesseract
# ['University of\nNorth Carolina\nTELEVISION\nUNC Bicentennial\nReel #1\nSync begins 1:57:00\ninto Reel #1\nReel length: 2:00:00\nShow length: 2:27:27 STEREO']
# ['University of\nNorth Carolina\nTE - E V.. o oN\nUNC Bicentennial\nReel #1 -\nSync begins\n1:57:00\ninto Reel #1\nReellength: 2:00:00\nShow length: 2:27.27 STEREO']
# ['oppure 22\nAUN Osten cnel\nio beal\nSync begins 1:57:00\ninto Reel #1\nReel length: 2:00:00\nShow length: 2:27:27 STEREO\n\x0c']
