import os
import shutil
import json
import random

original_path = '../input/data'
result_path = 'formatteddata'

original_stem = original_path
clean_result_path = True # Whether or not to delete all files in the result_path before converting the dataset
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
list_files('..')
val_split = 0
num_images = len([item for item in os.listdir(os.path.join(original_stem, 'train'))])
num_val_images = int(num_images * val_split)
val_indices = random.sample(range(num_images), num_val_images)
# Clean result path and make needed directories
if not os.path.exists(result_path):
    os.makedirs(result_path)

if clean_result_path:
    shutil.rmtree(result_path)

if not os.path.exists(os.path.join(result_path, 'train/images')):
    os.makedirs(os.path.join(result_path, 'train/images'))
if not os.path.exists(os.path.join(result_path, 'train/labels')):
    os.makedirs(os.path.join(result_path, 'train/labels'))
if not os.path.exists(os.path.join(result_path, 'val/images')):
    os.makedirs(os.path.join(result_path, 'val/images'))
if not os.path.exists(os.path.join(result_path, 'val/labels')):
    os.makedirs(os.path.join(result_path, 'val/labels'))

for i, imagename in enumerate(os.listdir(original_stem + '/train')):
    data_type_extension = 'val' if i in val_indices else 'train'
    # Make image copy in result path
    shutil.copyfile(os.path.join(original_stem, 'train', imagename), os.path.join(result_path, data_type_extension,'images', imagename))
    
    # Make converted annotation in result path
    if os.path.exists(os.path.join(original_stem, 'train_annotation', imagename.split('.')[0] + '.json')):
        with open(os.path.join(original_stem, 'train_annotation', imagename.split('.')[0] + '.json'), 'r') as original_annotation_file:
            original_annotation_data = json.load(original_annotation_file)
        with open(os.path.join(result_path, data_type_extension, 'labels', imagename.split('.')[0] + '.txt'), 'w') as annotation_file:
            image_width = float(original_annotation_data['image_size'][0]['width'])
            image_height = float(original_annotation_data['image_size'][0]['height'])
            for annotation in original_annotation_data['annotations']:
                scaled_x = str((float(annotation['left']) + 0.5 * float(annotation['width']))/ image_width)
                scaled_y = str((float(annotation['top']) + 0.5 * float(annotation['height']))/ image_height)
                scaled_width = str(float(annotation['width'])/ image_width)
                scaled_height = str(float(annotation['height'])/ image_height)
                annotation_file.write(' '.join([str(annotation['class_id']), scaled_x, scaled_y, scaled_width, scaled_height]))
# Get classes from synset.txt
with open(os.path.join(original_stem, 'train_annotation', 'synset.txt'), 'r') as synset_file:
        classes = synset_file.readline().split(' ')
# Make yaml file
with open(os.path.join(result_path, 'result.yaml'), 'w') as annotation_file:
    annotation_file.write('train: ../' + result_path + '/train/images' + '\n')
    annotation_file.write('val: ../' + result_path + '/train/images' + '\n')
    annotation_file.write('nc: ' + str(len(classes)) + '\n')
    annotation_file.write('names: [' + ', '.join(classes) + ']')

print('Finished dataset preparation with {} training images and {} validation images'.format(num_images - len(val_indices), len(val_indices)))
