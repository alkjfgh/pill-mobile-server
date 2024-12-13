import tensorflow as tf
import tensorflow_datasets as tfds
import os
from app.core.flowerTrans import FlowerTrans
import numpy as np


class DisImageService:
    def load_categories2(self):
        return [
            "미래트리메부틴정 100mg/병",
            "큐레틴정(빌베리건조엑스)",
            "콘택골드캡슐 10mg/PTP",
            "에스케이코스카플러스정",
            "에스케이코스카플러스에프정",
            "클로미딘정 100mg/병",
            "사리돈에이정 250mg/PTP",
            "스트라테라캡슐 25mg",
            "마도파정125",
            "노바스크정 5mg",
            "네비레트정(네비보롤염산염)",
            "대웅알벤다졸정 400mg/PTP",
            "토르셈정 10mg",
            "세비보정(텔비부딘)",
            "마도파정",
            "코다론정(아미오다론염산염)",
            "렉스펜정 300mg/PTP",
            "아프로벨정 150mg",
            "아프로벨정 300mg",
            "로자살탄정 100mg",
            "웰부트린엑스엘정 300mg",
            "모푸렌정(모사프리드시트르산염)",
            "레보펙신정 500mg",
            "캐롤에프정 368.9mg/PTP",
            "디오반필름코팅정 320mg",
            "엑스포지정 5/160mg",
            "미니린멜트설하정 60mcg",
            "미니린멜트설하정 120mcg",
            "리피논정 20mg",
            "리피논정 40mg",
            "플라벤정 500mg/PTP",
            "심바스트씨알정(심바스타틴)",
            "심발타캡슐 30mg",
            "임팩타민정 50mg/PTP",
            "우루사정 300mg",
            "제스판골드정 80mg/PTP",
            "프레미나정 0.3mg",
            "프레미나정 0.625mg",
            "맥시부펜이알정 300mg",
            "익수허브콜캡슐 490mg/포",
            "레보펙신정 250mg",
            "리피토정 80mg",
            "보령모사프리드시트르산염수화물정",
            "휴트라돌정",
            "쎄로켈서방정 400mg",
            "쎄로켈서방정 300mg",
            "쎄로켈서방정 50mg",
            "쎄로켈서방정 200mg",
            "자누메트정 50/500mg",
            "자누메트정 50/1000mg",
        ]

    def __init__(self):
        print("DisImageService __init__ start")
        # 현재 디렉토리 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 모델 로드
        model_path = os.path.join(current_dir, "../../model/oxford_flowers_model.h5")
        self.model = tf.keras.models.load_model(model_path)

        # 꽃 클래스 이름 로드
        dataset_builder = tfds.builder("oxford_flowers102")
        dataset_builder.download_and_prepare()
        self.categories = dataset_builder.info.features["label"].names

        model_path2 = os.path.join(current_dir, "../../model/best_model.keras")
        if os.path.exists(model_path2):
            self.model2 = tf.keras.models.load_model(model_path2)
        else:
            self.model2 = None

        self.categories2 = self.load_categories2()

        # 꽃 이름 번역
        self.flowerTrans = FlowerTrans()

        print("DisImageService __init__ end")

    def predict_image(self, image_path):
        print("DisImageService predict_image start")
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
            print("DisImageService predict_image end")
            return predicted_label, translated_label

        except Exception as e:
            return f"에러 발생: {str(e)}"

    def preprocess_image(self, image_path):
        image = tf.io.read_file(image_path)
        image = tf.image.decode_png(image, channels=3)
        image = tf.image.resize(image, (224, 224))
        image = tf.keras.applications.efficientnet.preprocess_input(image)
        return tf.expand_dims(image, axis=0)

    def predict_pill(self, image_path):
        print("DisImageService predict_pill start")
        try:
            print("image_path: ", image_path)

            processed_image = self.preprocess_image(image_path)
            predictions = self.model2.predict(processed_image)
            predicted_class = np.argmax(predictions, axis=1)[
                0
            ]  # 가장 높은 확률의 클래스 인덱스
            confidence = np.max(predictions)  # 가장 높은 확률 값

            print(f"Predicted Class: {self.categories2[predicted_class]}")
            print(f"Confidence: {confidence:.2f}")
            if confidence >= 0.8:
                predicted_label = self.categories2[predicted_class]
            else:
                predicted_label = "알약을 인식하지 못했습니다."

            predicted_label = self.categories2[predicted_class]

            print("predicted_label: ", predicted_label)
            print("DisImageService predict_pill end")
            return predicted_label, confidence
        except Exception as e:
            return f"에러 발생: {str(e)}"
