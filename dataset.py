import torch
from torchvision import transforms          
from torch.utils.data import Dataset

import os
from PIL import Image

import settings


class InferenceDataset(Dataset):
    def __init__(self, photoList, crops = None):
        self.photoList = photoList
        self.crops = crops
        self.transform =  transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def __len__(self):
        return len(self.photoList)

    def __getitem__(self, idx):
        img_path = os.path.join(settings.MEDIA_ROOT, self.photoList[idx])
        image = Image.open(img_path).convert("RGB")

        if self.crops and self.photoList[idx] in self.crops:
            crop = self.crops[self.photoList[idx]]
            image = image[crop[0]:crop[1], crop[2]:crop[3]]

        return self.transform(image)