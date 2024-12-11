import tensorflow as tf
import tensorflow_datasets as tfds

# 1. 학습된 모델 로드
model = tf.keras.models.load_model("oxford_flowers_model.h5")  # 학습된 모델 파일 로드

# 2. 데이터셋 클래스 이름 로드
# Oxford Flowers 102 데이터셋의 클래스 이름을 로드하여 예측 결과를 사람이 읽을 수 있게 변환
dataset_builder = tfds.builder("oxford_flowers102")
dataset_builder.download_and_prepare()  # 데이터셋 준비 (메타정보 로드)
class_names = dataset_builder.info.features["label"].names


# 3. 이미지 전처리 함수 정의
def preprocess_image(image_path):
    """
    이미지 경로를 입력받아 모델 입력 형식에 맞게 전처리합니다.
    - 이미지 크기를 (224, 224)로 리사이즈
    - [0, 255] 범위를 [0, 1]로 정규화
    - 배치 차원 추가
    """
    img = tf.keras.utils.load_img(
        image_path, target_size=(224, 224)
    )  # 이미지 로드 및 리사이즈
    img_array = tf.keras.utils.img_to_array(img)  # 이미지를 배열로 변환
    img_array = tf.expand_dims(img_array, axis=0)  # 배치 차원 추가
    img_array = img_array / 255.0  # 정규화
    return img_array


# 4. 이미지 경로 및 전처리
img_path = (
    "./test_img/flower3.png"  # flower1.jpg의 경로 (사용자가 업로드한 이미지 경로)
)
img_array = preprocess_image(img_path)  # 전처리된 이미지 배열

# 5. 예측 수행
predictions = model.predict(img_array)  # 모델 예측
predicted_class_idx = tf.argmax(
    predictions[0]
).numpy()  # 가장 높은 확률의 클래스 인덱스
predicted_class_name = class_names[predicted_class_idx]  # 클래스 이름 가져오기

# 6. 결과 출력
print(f"예측된 클래스: {predicted_class_name}")
