'''
LastEditTime: 2022-03-10 21:49:43
'''
import glob
import random
import os
import numpy as np

import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

# Normalization parameters for pre-trained PyTorch models
mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])


def denormalize(tensors):
    """ Denormalizes image tensors using mean and std """
    for c in range(3):
        tensors[:, c].mul_(std[c]).add_(mean[c])
        #mul ".X"
    return torch.clamp(tensors, 0, 255)
    #将输入input张量每个元素的夹紧到区间 [min,max][min,max]，并返回结果到一个新张量。


class ImageDataset(Dataset):
    def __init__(self, root, hr_shape):
        hr_height, hr_width = hr_shape
        # Transforms for low resolution images and high resolution images
        self.lr_transform = transforms.Compose(#contribute with
            [
                transforms.Resize((hr_height // 4, hr_height // 4), Image.BICUBIC),
                #"//" is a division method, return a integer number.
                transforms.ToTensor(),
                #convert  image from "numpy" or "PIL" to "tensor" 
                transforms.Normalize(mean, std),
                #divide the L2(范数)
            ]
        )
        self.hr_transform = transforms.Compose(
            [
                transforms.Resize((hr_height, hr_height), Image.BICUBIC),
                transforms.ToTensor(),
                transforms.Normalize(mean, std),
            ]
        )

        self.files = sorted(glob.glob(root + "/*.*"))

    def __getitem__(self, index):
        img = Image.open(self.files[index % len(self.files)])
        img_lr = self.lr_transform(img)
        img_hr = self.hr_transform(img)

        return {"lr": img_lr, "hr": img_hr}

    def __len__(self):
        return len(self.files)
