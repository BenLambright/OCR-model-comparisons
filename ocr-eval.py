import ast
from doctr.io import DocumentFile  # reading a document
from doctr.models import ocr_predictor  # getting the ocr model
import os
from PIL import Image
import pytesseract
from jiwer import cer
import chardet


SAMPLE_SIZE = 19


def process_gold(gold_path, tesseract_five_path) -> tuple[list[str], list[str]]:
    """Reformatting the gold files so it can be compared to OCR outputs, as well as the order"""
    with open(gold_path, "r") as file:
        golds = file.read()
        # print(f"correct_order: {golds}")


    golds = golds.replace("true", "True").replace("false", "False")  # ast won't be recognize this as a list without this, you also have to remove some other lines manually
    golds = ast.literal_eval(golds)
    gold_output = [golds[i][5] for i in list(range(0, SAMPLE_SIZE))]

    correct_order = [os.path.join(tesseract_five_path, golds[i][0][:-3] + "txt") 
                        for i in list(range(0, SAMPLE_SIZE))]

    return gold_output, correct_order

def calc_doctr(image_path) -> str:
    """calculating the doctr result for an image, matching the style of the gold, so newlines are with \n"""
    single_img_doc = DocumentFile.from_images(image_path)
    model = ocr_predictor(pretrained=True)
    result = model(single_img_doc)

    json_output = result.export()
    sentences = []
    for page in json_output["pages"]:
        for block in page["blocks"]:
            for line in block["lines"]:
                words = [word["value"] for word in line["words"]]
                sentences.append(" ".join(words))

    return "\n".join(sentences)


def calc_tesseract(image_path) -> str:
    """tesseract4 output for a single image"""
    tesseract_output = pytesseract.image_to_string(Image.open(image_path))

    return tesseract_output

def process_tesseract_five(correct_order) -> list[str]:
    """tesseract5 output extraction for all images"""
    outputs = []
    for output in correct_order:
        with open(output, "r", encoding="utf-8", errors="ignore") as f:  # we had to clarify the output because the tesseract outputs were not all
            output_lines = [line.strip() for line in f]
            output_str = "\n".join(output_lines)
            outputs.append(output_str)

    return outputs


def calc_cer(gold_output, doctr_output, tesseract_output) -> tuple[int, int]:
    """Calculating the cer for doctr and tesseract4"""
    doctr_results = cer(gold_output, doctr_output)
    tesseract_results = cer(gold_output, tesseract_output)

    return doctr_results, tesseract_results


def output_as_file(doctr_outputs, tesseract_outputs):
    """Outputs the tesseract4 and doctr outputs as a file"""
    # write a file for the tessearct4
    with open("tesseract4_and_doctr_outputs/tesseract4.txt", "w") as tesseractf:
        tesseractf.write(str(tesseract_outputs))
    
    with open("tesseract4_and_doctr_outputs/doctr.txt", "w") as doctrf:
        doctrf.write(str(doctr_outputs))


def main_tests(images, gold_outputs):
    """running and logging the doctr and tesseract4 tests"""
    # run the doctr tests
    print("loading doctr...")
    model = ocr_predictor(pretrained=True)

    print("calculating doctr results...")
    doctr_outputs = [calc_doctr(image) for image in images]

    # run the tesseract tests
    print("running tesseract...")
    tesseract_outputs = [calc_tesseract(image) for image in images]

    # calc the cer
    doctr_results, tesseract_results = calc_cer(gold_outputs, doctr_outputs, tesseract_outputs)
    print(f"doctr_results: {doctr_results}")
    print(f"tesseract4_results: {tesseract_results}")

    # put the outputs in a file
    print("outputting doctr and tesseract4 results into file output")
    output_as_file(doctr_outputs, tesseract_outputs)

def tesseract_five_test(correct_order, tesseract_five_path):
    """running and logging the tesseract5 test"""

    print("processing tesseract5")
    tesseract_outputs = process_tesseract_five(correct_order)
    print(f"outputs: {tesseract_outputs}")
    print(f"gold outputs: {gold_outputs}")
    print(f"tesseract5_results: {cer(gold_outputs, tesseract_outputs)}")



if __name__ == "__main__":
    image_dir = "images"
    gold_path = "img_arr_prog.js"  
    tesseract_five_path = "tesseract_five_outputs"

    # getting the gold outputs
    gold_outputs, correct_order = process_gold(gold_path, tesseract_five_path)

    # getting the list of image files
    images = os.listdir(image_dir)
    images = [os.path.join(image_dir, image) for image in images]

    # main tests
    # main_tests(images, gold_outputs)

    # calculating tesseract5
    tesseract_five_test(correct_order, tesseract_five_path)




