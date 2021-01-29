from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from os.path import isfile, join
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.models.detection import maskrcnn_resnet50_fpn

import numpy as np

class Imagen:

    def __init__(self, file_dir, file_name):
        self.im_nombre = file_name
        self.im_directorio = file_dir
        if isfile(join(file_dir, file_name)):
            archivo = join(file_dir, file_name)
        else:
            print('No existe archivo')
            return
        
        # pill image
        self.pil_img = Image.open(archivo).convert('RGB')
        size_img = 500, 500
        self.pil_img.thumbnail(size_img)

        # qt pixmap image
        image = ImageQt(self.pil_img)
        self.imqt = QtGui.QPixmap.fromImage(image)

        # tensor image
        img = np.asarray(self.pil_img, dtype=np.float)/255
        self.tsimg = torch.as_tensor(img, dtype=torch.float32).permute(2, 0, 1)

        self.mtx = np.asarray(self.pil_img)

        self.predictions = {}


class Dermia_Model:

    def __init__(self):
        self.model_path = 'model/'
        self.model_parmeters_file = 'ISICModel_parameters.pt'
        self.num_classes = 4
        model_filename = join(self.model_path, self.model_parmeters_file)
        # load model
        self.model = self.get_instance_segmentation_model(self.num_classes)
        self.model.load_state_dict(torch.load(model_filename))
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)
        self.model.eval()
        self.score_threshold = 0.8


    def get_instance_segmentation_model(self, num_classes):
        # load an instance segmentation model pre-trained on COCO
        model = maskrcnn_resnet50_fpn(pretrained=True)

        # get the number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        # replace the pre-trained head with a new one
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

        # now get the number of input features for the mask classifier
        in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
        hidden_layer = 256
        # and replace the mask predictor with a new one
        model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                           hidden_layer,
                                                           num_classes)
        return model

    def restart(self):
        model_filename = join(self.model_path, self.model_parmeters_file)
        # load model
        self.model = self.get_instance_segmentation_model(self.num_classes)
        self.model.load_state_dict(torch.load(model_filename))
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)
        self.model.eval()

    def evaluate(self, imagen):
        with torch.no_grad():
            prediction = self.model([imagen.tsimg.to(self.device)])

        scores = prediction[0]['scores'].cpu()
        labels = prediction[0]['labels'].cpu()
        masks = prediction[0]['masks'].cpu()
        detect_ok = scores >= self.score_threshold
        scores = scores[detect_ok].numpy()
        labels = labels[detect_ok].numpy()
        masks = masks[detect_ok]
        imagen.predictions = {}  # initialize predictions
        for i in range(len(scores)):
            imagen.predictions[i] = {'score': scores[i],
                                     'label': labels[i],
                                     'mask': masks[i, 0]}  # mask is a tensor, max = 1








