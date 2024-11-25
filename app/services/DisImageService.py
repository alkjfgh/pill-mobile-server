import torch
from torchvision import models, transforms
from PIL import Image
import os


class DisImageService:
    def __init__(self):
        # ResNet50 모델 로드 및 평가 모드로 설정
        self.model = models.resnet50(pretrained=True)
        self.model.eval()

        # 이미지 전처리를 위한 transform 설정
        self.transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        # 절대 경로로 파일 위치 지정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        classes_file = os.path.join(current_dir, "imagenet_classes.txt")

        with open(classes_file, "r") as f:
            self.categories = [s.strip() for s in f.readlines()]

    def predict_image(self, image_path):
        try:
            # 이미지 로드 및 전처리
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.transform(image)
            image_tensor = image_tensor.unsqueeze(0)  # 배치 차원 추가

            # 예측 수행
            with torch.no_grad():
                outputs = self.model(image_tensor)

            # 가장 높은 확률의 클래스 가져오기
            _, predicted_idx = torch.max(outputs, 1)
            predicted_label = self.categories[predicted_idx.item()]
            if len(predicted_label.split(",")) > 1:
                return predicted_label.split(",")[1]
            else:
                return predicted_label

        except Exception as e:
            return f"에러 발생: {str(e)}"
