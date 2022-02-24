python3 convertdataset.py # Converts dataset to yolov5 training format
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
python3 train.py --img 640 --batch 16 --epochs 300 --data ../formatteddata/result.yaml --weights yolov5s.pt --noval --cache
python3 export.py --weights runs/train/exp/weights/best.pt --img 640 --batch 1 --include onnx
