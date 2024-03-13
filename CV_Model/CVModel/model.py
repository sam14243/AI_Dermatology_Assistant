from transformers import pipeline
import numpy as np
import time

class visual_adapters:
    def __init__(self):
        self.normal_derm = pipeline("image-classification", model="RahulPil/dermi_model")
        time.sleep(2)
        '''"Acne","Blackhead","Purulent","Scars","Sebo-crystan-conglo","Syringoma","Whitehead","Conglobata","Crystanlline","Cystic","Flat_wart","Folliculitis","Keloid","Milium","Papular"'''
        
        self.cancer = pipeline("image-classification", model="ALM-AHME/swinv2-large-patch4-window12to16-192to256-22kto1k-ft-finetuned-Lesion-Classification-HAM10000-S")
        time.sleep(4)
        self.cancer_2 = pipeline('image-classification',model='ALM-AHME/beit-large-patch16-224-finetuned-Lesion-Classification-HAM10000-AH-60-20-20')
        time.sleep(1)
        self.cancer_3 = pipeline("image-classification", model="ALM-AHME/convnextv2-large-1k-224-finetuned-Lesion-Classification-HAM10000-AH-60-20-20-Shuffled")
        ''' melanoma, melanocytic nevus, basal cell carcinoma, actinic keratosis, benign keratosis, dermatofibroma and vascular lesion '''
        time.sleep(3)
        self.cancer_isic = pipeline("image-classification", model=r"D:\SAM\Sem-6\Misc\Avishkaar\checkpoint-5870")
        time.sleep(1)
        self.cancer_isic_2 = pipeline("image-classification", model="ahishamm/vit-base-isic-sharpened-patch-32")
        ''' actinic keratosis, basal cell carcinoma, dermatofibroma, melanoma, nevus, pigmented benign keratosis, seborrheic keratosis, squamous cell carcinoma, vascular lesion.'''
        time.sleep(2)
        self.something = pipeline("image-classification", model="youngp5/skin-conditions")
        '''"Basal Cell Carcinoma (BCC)","Benign Keratosis-like Lesions (BKL) ","Eczema","Melanocytic Nevi (NV)","Melanoma","Psoriasis pictures Lichen Planus and related diseases","Seborrheic Keratoses and other Benign Tumors","Tinea Ringworm Candidiasis and other Fungal Infections","Warts Molluscum and other Viral Infections"'''

    def __call__(self, image):
        x = self.processor(image)

        diseases={0:[],1:[]}
        for i in x:
            for j,k in enumerate(i[:2]):
                diseases[j].append(k['label'])
        return diseases
    
    def processor(self,image):
        dia_normal = self.normal_derm(image)

        dia_cancer_1 = self.cancer(image)
        dia_cancer_2 = self.cancer_2(image)
        dia_cancer_3= self.cancer_3(image)

        dia_cancer_isic_1 = self.cancer_isic(image)
        dia_cancer_isic_2 = self.cancer_isic_2(image)

        dia_others = self.something(image)

        dia_cancer = dia_cancer_1+dia_cancer_2+dia_cancer_3
        dia_cancer_isic = dia_cancer_isic_1 + dia_cancer_isic_2

        dia_cancer.sort(key = lambda x: x['score'],reverse=True)
        dia_cancer_isic.sort(key = lambda x: x['score'],reverse=True)

        return dia_normal,dia_cancer,dia_cancer_isic,dia_others