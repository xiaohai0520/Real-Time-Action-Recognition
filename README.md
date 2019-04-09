# action_recognition_on_C3D
A small program for action recognition on C3D

[![watch video](https://github.com/xiaohai0520/action_recognition_on_C3D/blob/master/image/test2.png?raw=true)](https://www.youtube.com/watch?v=6_QowqAsjWs)

## Content
- [Deployment](#deployment)
- [Usage](#usage)
  - [Dataset](#dataset)
  - [Experiments](#experiments)
- [Reference](#reference)

# Deployment

The program depends on *[Pytorch](https://github.com/pytorch/pytorch)*,*[OpenCV](https://github.com/opencv/opencv)*,*[PyQt](https://github.com/PyQt5/PyQt)* and so on.  

# Usage
1. Install dependency:
    For PyTorch dependency, see [pytorch.org](https://pytorch.org/) for more details.

    For custom dependencies:
    ```Shell
    conda install opencv
    pip install tqdm scikit-learn tensorboardX
    pip install pyqt5
    ```
2. Download pretrained model from [BaiduYun](https://pan.baidu.com/s/1saNqGBkzZHwZpG-A5RDLVw) or 
[GoogleDrive](https://drive.google.com/file/d/19NWziHWh1LgCcHU34geoKwYezAogv9fX/view?usp=sharing).   

3. Configure your dataset and pretrained model path.

4. Train the Model.

    ```Shell
    python train.py
    ```
5. Run the GUI to test on camera.
    ```Shell
    python GUI.py

    ```

## Datasets:
Dataset directory tree is shown below

- **UCF101**
Make sure to put the files as the following structure:
  ```
  UCF-101
  ├── ApplyEyeMakeup
  │   ├── v_ApplyEyeMakeup_g01_c01.avi
  │   └── ...
  ├── ApplyLipstick
  │   ├── v_ApplyLipstick_g01_c01.avi
  │   └── ...
  └── Archery
  │   ├── v_Archery_g01_c01.avi
  │   └── ...
  ```
After pre-processing, the output dir's structure is as follows:
  ```
  ucf101
  ├── ApplyEyeMakeup
  │   ├── v_ApplyEyeMakeup_g01_c01
  │   │   ├── 00001.jpg
  │   │   └── ...
  │   └── ...
  ├── ApplyLipstick
  │   ├── v_ApplyLipstick_g01_c01
  │   │   ├── 00001.jpg
  │   │   └── ...
  │   └── ...
  └── Archery
  │   ├── v_Archery_g01_c01
  │   │   ├── 00001.jpg
  │   │   └── ...
  │   └── ...
  ```

## Experiments
These models were trained in machine with NVIDIA TITAN X 12gb GPU. Note that I splited
train/val/test data for each dataset using sklearn. If you want to train models using
official train/val/test data, you can look in [dataset.py](https://github.com/jfzhang95/pytorch-video-recognition/blob/master/dataloaders/dataset.py), and modify it to your needs.

- **UCF101**

<p align="center"><img src="https://github.com/xiaohai0520/action_recognition_on_C3D/blob/master/image/ucf101_results.png?raw=true" align="center" width=900 height=auto/></p>


# Reference
The paper: *["Learning Spatiotemporal Features with 3D Convolutional Networks"](https://arxiv.org/pdf/1412.0767.pdf) by Du Tran1,2
, Lubomir Bourdev1
, Rob Fergus1
, Lorenzo Torresani2
, Manohar Paluri1*.
