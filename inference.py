import settings

import os
import sys

import torch
from torchvision import transforms          
from torch.utils.data import Dataset

from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class InferenceDataset(Dataset):
    def __init__(self, photoList):
        self.photoList = photoList
        self.transform =  transforms.Compose([
            transforms.Resize((224,224)),
        #  transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def __len__(self):
        return len(self.photoList)

    def __getitem__(self, idx):
        img_path = os.path.join(settings.MEDIA_ROOT, self.photoList[idx])
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image

class Classifier:
    def infer(self,model):
        model.eval()
        with torch.no_grad():
            self.scores = {}
            for i, inputs in enumerate(self.dataloader):
                try:
                    inputs = inputs.to(device)
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    for j in range(inputs.size()[0]):
                        probabilities = torch.nn.functional.softmax(outputs[j], dim=0).tolist()
                        self.scores[self.dataset.photoList[j]] = probabilities
                                           
                except:
                    print('eception: file '+ str(i) , file = sys.stderr)

            


    def __init__(self,photoList):
        self.dataset = InferenceDataset(photoList)
       # self.class_names = ['mosquito', 'not-diptera', 'other-diptera']
        self.dataloader = torch.utils.data.DataLoader(self.dataset, batch_size=32, shuffle=False, num_workers=0)


        if (os.path.isfile('model.pth')):
            model_ft = torch.load('model.pth', map_location=device)

        self.infer(model_ft)
