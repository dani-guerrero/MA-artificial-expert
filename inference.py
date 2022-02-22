import os
import sys

import torch
from dataset import InferenceDataset

from logger import log


class Classifier:

    def infer(self,model):

        model.eval()
        with torch.no_grad():
            self.scores = {}
            for i, inputs in enumerate(self.dataloader):
                try:
                    inputs = inputs.to(self.device)
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    for j in range(inputs.size()[0]):
                        probabilities = torch.nn.functional.softmax(outputs[j], dim=0).tolist()
                        self.scores[self.dataset.photoList[j]] = probabilities
                                           
                except:
                    log("error in classification")

            


    def __init__(self,classifierPath,photoList,crops=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dataset = InferenceDataset(photoList, crops)
        self.dataloader = torch.utils.data.DataLoader(self.dataset, batch_size=32, shuffle=False, num_workers=0)


        if (os.path.isfile(classifierPath)):
            model_ft = torch.load(classifierPath, map_location=self.device)

        self.infer(model_ft)
