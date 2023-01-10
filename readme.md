# Photo Rank

The goal of this tool is to rank photos to reduce the time spent looking through thousands of photos and to pick some of the best ones. Much of the code was written using Chat-GPT 3.5. Currently, the model is based on this GitHub repository: https://github.com/dingkeyan93/Intrinsic-Image-Popularity, though this may change in the future.

Dependencies
This tool requires the following Python libraries:

PyQt5
numpy
torch
torchvision
PIL
Running the Tool
To run the tool, simply run the ui.py file using Python.

Using the Tool
To use the tool, select the input directory containing the images you want to sort and select the output directory where you want to save the sorted images. Then, move the slider to choose the top percentage of images to save to the output directory. Finally, click the "Run" button to start the sorting process. The progress of the sorting process will be displayed in the progress bar.

Note: The feature to display the images being sorted is currently not implemented.