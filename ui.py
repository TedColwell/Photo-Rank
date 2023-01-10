import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QLineEdit, QVBoxLayout, QProgressBar, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from model.run_model import run_model

class UserInterface(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Photo Rank')
        #self.title = 'Image Sorter'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000
        self.num_output_images = 0 
        self.num_input_images = 100 

        self.initUI()

    
    def initUI(self):
   
        # Create input and output directory buttons
        self.input_button = QPushButton('Select Input Directory', self)
        self.input_button.clicked.connect(self.selectInputDir)
        self.output_button = QPushButton('Select Output Directory', self)
        self.output_button.clicked.connect(self.selectOutputDir)

        # Create input and output directory line edits
        self.input_line_edit = QLineEdit(self)
        self.output_line_edit = QLineEdit(self)

        # Create a label to display the input directory path
        self.input_label = QLabel(self)
        self.input_label.setText('Input directory:')
        self.input_label.setBuddy(self.input_line_edit)

        # Create a label to display the output directory path
        self.output_label = QLabel(self)
        self.output_label.setText('Output directory:')
        self.output_label.setBuddy(self.output_line_edit)

        # Create a run button to start evaluation
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run)       
        # Create a label to display the image
        self.image_label = QLabel(self)

        # Create a progress label
        self.progress_label = QLabel(self)

        # Create a progress bar
        self.progress_bar = QProgressBar(self)

        # Create a label to display the current value of the slider
        self.slider_label = QLabel(self)
        self.slider_label.setText('Move this slider to change the top % of images to save to the output directory \n')
        
        # Create a horizontal slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(5)
        self.slider.valueChanged.connect(self.updateSliderLabel)

        # Add a QLabel to display the score
        self.score_label = QLabel(self)



        # Create a layout and add the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_button)
        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_button)
        layout.addWidget(self.output_line_edit)
        layout.addWidget(self.run_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.score_label)

        

    def selectInputDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(self, 'Select Input Directory', '/', options=options)
        self.input_line_edit.setText(directory)

        # Store the list of files in the input directory
        files = os.listdir(directory)
        self.image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.num_input_images = len(self.image_files)

    def selectOutputDir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory', '/', options=options)
        self.output_line_edit.setText(directory)

    def updateSliderLabel(self):
        # Update the label to show the current value of the slider
        slider_value = self.slider.value()
        self.num_output_images = self.num_input_images*(slider_value/100)
        self.slider_label.setText(f'Top % of images to save to the output directory \n {slider_value} % = {int(self.num_output_images)} of {int(self.num_input_images)} Images')
    
    def run(self, layout):

        input_dir = self.input_line_edit.text()
        output_dir = self.output_line_edit.text()
        # check if the input directory exists
        if not os.path.isdir(input_dir):
            self.output_text_edit.setText("Input directory does not exist")
            return
        
        # check if the output directory exists, create it if it does not
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        
        # Use the stored image files and num_input_images variables
        image_files = self.image_files

        # Update the progress label in the run function
        self.progress_label.setText(f'Filtering for only .png, .jpg and .jpeg files')
        
        # create a dictionary to store the scores of each image
        scores = {}
        
        # initialize the progress bar
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(image_files))

        # Add the QPixmap widget to the layout  #TODO: FIx
        #self.layout.addWidget(self.image_display)
        #self.image_display = QPixmap()
        #self.addWidget(self.image_display)
        
        # loop through each image file
        
        for i, image_file in enumerate(image_files):
            # run the model on the image and store sores
            score = run_model(os.path.join(input_dir, image_file))
            scores[image_file] = score
            # update the progress bar
            self.progress_bar.setValue(i+1)
            self.progress_label.setText(f'Processing image {i+1} of {self.num_input_images}')
            #Update the current image #TODO
    
            #self.image_display.load(os.path.join(input_dir, image_file))
            #self.image_label.setPixmap(self.image_display)
            #self.score_label.setText(f'Score: {score}')

        # sort the dictionary by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # loop through the sorted scores
        for i, (image_file, score) in enumerate(sorted_scores):
            # if the current image is within the top percentage, copy it to the output directory
            if i < self.num_output_images:
                shutil.copy(os.path.join(input_dir, image_file), output_dir)
                # Split the file name and extension
                file_name, file_extension = os.path.splitext(image_file)
                # Construct the new file name by combining the score, file name, and extension
                new_file_name = "{}_{}{}".format(score, file_name, file_extension)
                # Rename the file using the new file name
                os.rename(os.path.join(output_dir, image_file), os.path.join(output_dir, new_file_name))

        
        # display a success message #Todo
        #self.output_text_edit.setText("Successfully sorted images")

def main():
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()