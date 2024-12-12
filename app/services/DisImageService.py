import tensorflow as tf
import tensorflow_datasets as tfds
import os
from app.core.flowerTrans import FlowerTrans


class DisImageService:
    def __init__(self):
        # 현재 디렉토리 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 모델 로드
        model_path = os.path.join(current_dir, "../../model/oxford_flowers_model.h5")
        self.model = tf.keras.models.load_model(model_path)

        # 클래스 이름 로드
        dataset_builder = tfds.builder("oxford_flowers102")
        dataset_builder.download_and_prepare()
        self.categories = dataset_builder.info.features["label"].names

        # 꽃 이름 번역
        self.flowerTrans = FlowerTrans()

    def predict_image(self, image_path):
        print("DisImageService predict_image")
        try:
            print("image_path: ", image_path)
            # 이미지 전처리
            img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            # 예측 수행
            predictions = self.model.predict(img_array)
            predicted_idx = tf.argmax(predictions[0]).numpy()
            predicted_label = self.categories[predicted_idx]

            print("predicted_label: ", predicted_label)
            translated_label = self.flowerTrans.trans(predicted_label)
            print("translated predicted_label: ", translated_label)
            return predicted_label, translated_label

        except Exception as e:
            return f"에러 발생: {str(e)}"
