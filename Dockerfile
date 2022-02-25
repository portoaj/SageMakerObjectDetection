FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib" \
    PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

ENV WORKDIR=/workspace
ENV SHELL=/bin/bash

# Install build dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    ca-certificates \
    curl \
    cmake \
    git \
    libopencv-dev \
    wget \
    unzip \
    libopenblas-dev \
    ninja-build \
    python3-dev \
    python3-pip \
    python3-setuptools \
    libxft-dev \
    zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools \
    boto3

# Install yolov5 and its dependencies
RUN mkdir -p ${WORKDIR}
RUN cd ${WORKDIR} \
   && git clone https://github.com/ultralytics/yolov5.git \
   && cd yolov5 \
   && python3 -m pip install -r requirements.txt \
   && python3 -m pip install onnx>=1.9.0

RUN python3 -m pip --no-cache-dir install --upgrade \
    sagemaker-training\
    opencv-python


# Copy the training script inside the container
COPY train.py /opt/ml/code/train.py
COPY trainyolo.sh /opt/ml/code/trainyolo.sh
COPY convertdataset.py /opt/ml/code/convertdataset.py

# Define train.py as the script entry point
ENV SAGEMAKER_PROGRAM train.py