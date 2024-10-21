FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Pythonと必要なツールをインストール
RUN apt-get update && apt-get install -y python3 python3-pip

# Pythonパッケージのアップグレード
RUN pip3 install --upgrade pip

# 機械学習ライブラリのインストール
RUN pip3 install numpy pandas scikit-learn jupyter matplotlib tqdm transformers vllm
