# 알약 판별 AI REST API 서버

## 프로젝트 소개
이 프로젝트는 딥러닝 모델을 활용하여 알약 이미지를 분석하고 판별하는 REST API 서버입니다. FastAPI 프레임워크를 기반으로 구축되었으며, 이미지를 입력받아 해당 알약의 정보를 반환합니다.

## 주요 기능
- 알약 이미지 업로드 및 분석
- 알약 정보 조회 API
- 실시간 이미지 처리 및 결과 반환

## 기술 스택
- Python 3.11+
- FastAPI
- PyTorch
- OpenCV
- SQLAlchemy (데이터베이스 연동)

## 설치 방법
1. 저장소 클론
```bash
git clone [repository URL]
cd [project directory]
```

2. 가상환경 생성 및 활성화
```bash
python3.11 -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```

3. 필요한 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 실행 방법
```bash
python run.py
```

서버는 기본적으로 https://localhost:8443 에서 실행됩니다.

## API 엔드포인트

### 이미지 분석 API
- **엔드포인트**: `/api/v1/analyze`
- **메소드**: POST
- **입력**: 이미지 파일
- **출력**: 알약 정보 (JSON)

### 알약 정보 조회 API
- **엔드포인트**: `/api/v1/medicine/{id}`
- **메소드**: GET
- **출력**: 알약 상세 정보

## API 문서
- Swagger UI: https://localhost:8443/docs
- ReDoc: https://localhost:8443/redoc

## 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성하고 다음 변수들을 설정하세요:
```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
MODEL_PATH=./models/pill_classifier.pt
```


## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여 방법
1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다.
3. 변경사항을 커밋합니다.
4. 브랜치에 푸시합니다.
5. Pull Request를 생성합니다.