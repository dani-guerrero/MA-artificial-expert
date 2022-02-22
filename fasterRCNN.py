import settings

import torch
import torchvision

import numpy as np

import cv2

import os

from dataset import InferenceDataset

class Cropper():
    def __init__(self, photoList):

        self.dataset = InferenceDataset(photoList)
        self.dataloader = torch.utils.data.DataLoader(self.dataset, batch_size=settings.fasterRCNN['batch_size'], shuffle=False, num_workers=0)
        self.photoList = photoList

        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        PATH = settings.fasterRCNN['filename']
        self.model = torch.load(PATH, map_location=self.device)
        self.model.eval()
        self.model.to(self.device)

        self.boxes = {}
        self.scores = {}

        for i, inputs in enumerate(self.dataloader):
            for j in range(inputs.size()[0]):
                filepath = os.path.join(settings.MEDIA_ROOT,self.dataset.photoList[j])
                img = cv2.imread(filepath, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
                image /= 255.0 #normalization
                image = torchvision.transforms.ToTensor()(image)
                image = image.unsqueeze(1).to(self.device)
                dictlist = self.model(image)

                max_score = 0

                for dict in dictlist:
                    keep = torchvision.ops.batched_nms(dict['boxes'], dict['scores'], dict['labels'], 0.1)
                    if len (dict['boxes']):
                        box = [round(a) for a in dict['boxes'][keep.tolist()[0]].tolist()]
                        score = dict['scores'].tolist()[0]
                        if score > max_score:
                            max_score = score
                            best_box = box
                print(filepath, best_box)

                self.boxes[self.dataset.photoList[j]] = { 
                    'xtl': best_box[0],
                    'ytl': best_box[1],
                    'xbr': best_box[2],
                    'ybr': best_box[3],
                    'score': score,
                    'class': 'insect'
                }
        