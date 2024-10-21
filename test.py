import torch
print(torch.cuda.is_available())  # Trueが出力されれば成功
print(torch.cuda.get_device_name(0))  # 使用可能なGPU名を表示
