import subprocess
import os
import shutil

subprocess.call('bash ./trainyolo.sh', shell=True) # Bash files that runs Yolov5 train.py and export.py scripts
shutil.move(os.path.join('../input/data', 'train_annotation', 'synset.txt'), '../model/synset.txt') # Moves annotation classes to output
shutil.move('yolov5/runs/train/exp/weights/best.onnx', '../model/model.onnx') # Moves onnx model to output
shutil.move('yolov5/runs/train/exp/weights/best.pt', '../model/model.pt') # Moves standard Yolov5 model to output