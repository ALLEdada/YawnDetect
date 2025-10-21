Ultralytics 8.3.218  Python-3.10.11 torch-2.9.0+cu130 CUDA:0 (NVIDIA GeForce RTX 5080, 16303MiB)
| NVIDIA-SMI 581.08                 Driver Version: 581.08         CUDA Version: 13.0     

install torch packages:

pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130


start train:

open terminal:

yolo detect train model=yolo11s.pt data=driver_yawn.yaml epochs=100 imgsz=640 batch=32 device=0 amp=True 