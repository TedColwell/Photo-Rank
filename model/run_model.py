import argparse
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def prepare_image(image):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    Transform = transforms.Compose([
            transforms.Resize([224,224]),      
            transforms.ToTensor(),
            ])
    image = Transform(image)   
    image = image.unsqueeze(0)
    return image.to(device)

def predict(image, model):
    print('Predicting')
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    return r'%.5f' % preds.item()

def run_model(image_path):
    print('Run Model Run')
    image = Image.open(image_path)
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load('model/model-resnet50.pth', map_location=device)) 
    model.eval().to(device)
    return predict(image, model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='images/0.jpg')
    config = parser.parse_args()
    image_path = config.image_path
    run_model(image_path)
