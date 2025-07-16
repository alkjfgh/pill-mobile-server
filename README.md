# 🏥 알약 판별 AI REST API 서버 (Pill Recognition AI Server)

> **딥러닝 기반 알약 이미지 분석 및 의약품 정보 제공 시스템**
> 
> TensorFlow와 EfficientNet을 활용한 고정확도 알약 식별 서비스

---

## 📋 프로젝트 개요

본 프로젝트는 **컴퓨터 비전과 딥러닝 기술을 활용하여 알약 이미지를 자동으로 식별하고 해당 의약품의 상세 정보를 제공하는 REST API 서버**입니다. 

사용자가 스마트폰으로 촬영한 알약 이미지를 업로드하면, AI 모델이 알약을 분석하여 약품명과 효능·효과를 실시간으로 제공합니다. 의료진, 약사, 일반 사용자들이 신속하고 정확하게 알약을 식별할 수 있도록 지원합니다.

### 🎯 프로젝트 목적
- **의약품 안전성 향상**: 알약 오복용 방지 및 정확한 복약 지도
- **의료진 업무 효율성 증대**: 신속한 약물 식별을 통한 진료 시간 단축
- **일반인 접근성**: 누구나 쉽게 사용할 수 있는 약물 정보 서비스
- **AI 기술 실용화**: 실제 의료 현장에서 활용 가능한 AI 솔루션 구현

---

## 🚀 주요 기능

### 🔍 핵심 기능
- **AI 기반 알약 이미지 분석**: EfficientNet 모델을 활용한 고정확도 알약 식별
- **실시간 의약품 정보 제공**: 50여 종의 한국 의약품 데이터베이스 연동
- **신뢰도 기반 결과 제공**: 신뢰도 80% 이상일 때만 상세 정보 제공으로 오진 방지
- **다중 이미지 포맷 지원**: PNG, JPG, JPEG 형식 지원

### 💼 관리 기능
- **사용자 관리 시스템**: JWT 기반 인증 및 사용자 정보 관리
- **관리자 대시보드**: 웹 기반 관리 인터페이스 (사용자 관리, 로그 조회)
- **상세 로그 시스템**: 모든 분석 요청 및 결과 기록 관리
- **이미지 자동 관리**: 임시 파일 자동 정리 시스템
- **모바일 앱 릴리즈 관리**: APK 파일 배포 및 버전 관리

### 🌸 부가 기능
- **꽃 이미지 분석**: Oxford Flowers 102 데이터셋 기반 꽃 분류 (데모/테스트용)

---

## 🛠 기술 스택

### **Backend Framework**
- **Python 3.11+**: 메인 개발 언어
- **FastAPI 0.115+**: 고성능 비동기 웹 프레임워크
- **Uvicorn**: ASGI 웹 서버
- **Pydantic**: 데이터 검증 및 설정 관리

### **AI/Machine Learning**
- **TensorFlow 2.18+**: 딥러닝 프레임워크
- **PyTorch 2.1+**: 신경망 모델링 (일부 모듈)
- **TensorFlow Datasets**: Oxford Flowers 102 데이터셋 처리
- **EfficientNet**: 이미지 분류 모델 아키텍처
- **NumPy, SciPy**: 수치 연산 라이브러리

### **Database & ORM**
- **MySQL**: 메인 데이터베이스 (운영 환경)
- **SQLite**: 개발/테스트 환경 지원
- **SQLAlchemy 2.0+**: Python ORM
- **Alembic**: 데이터베이스 마이그레이션 도구
- **PyMySQL**: MySQL 커넥터

### **Authentication & Security**
- **JWT (Python-JOSE)**: 토큰 기반 인증
- **Passlib**: 비밀번호 해싱
- **Session Middleware**: 세션 관리
- **CORS Middleware**: 크로스 오리진 리소스 공유

### **Image Processing**
- **Pillow (PIL)**: 이미지 처리 라이브러리
- **File Upload/Management**: 이미지 업로드 및 관리 시스템

### **Web & Template**
- **Jinja2**: HTML 템플릿 엔진
- **Static Files**: 정적 파일 서빙
- **HTML/CSS**: 관리자 대시보드 UI

### **Additional Libraries**
- **Redis (aioredis)**: 세션 스토어
- **Python-multipart**: 파일 업로드 처리
- **Python-dotenv**: 환경 변수 관리
- **Email-validator**: 이메일 검증
- **BSON**: 바이너리 JSON 처리

---

## 🏗 시스템 아키텍처

### **Clean Architecture 구조**
```
pill-mobile-server/
├── app/
│   ├── api/               # API 계층
│   │   ├── endpoints/     # 엔드포인트 정의
│   │   │   ├── disPill.py      # 알약/꽃 분석 API
│   │   │   ├── users.py        # 사용자 관리 API
│   │   │   ├── logs.py         # 로그 관리 API
│   │   │   ├── admin.py        # 관리자 API
│   │   │   └── release.py      # 릴리즈 관리 API
│   │   └── router.py      # 라우팅 설정
│   ├── core/              # 핵심 설정 및 유틸리티
│   │   ├── config.py      # 애플리케이션 설정
│   │   ├── pillTrans.py   # 알약 정보 번역
│   │   ├── flowerTrans.py # 꽃 정보 번역
│   │   ├── pillDescription.json  # 알약 정보 DB
│   │   └── flowerTrans.json     # 꽃 번역 DB
│   ├── models/            # 데이터 모델
│   │   ├── user.py        # 사용자 모델
│   │   ├── log.py         # 로그 모델
│   │   ├── admin.py       # 관리자 모델
│   │   └── description.py # 설명 모델
│   ├── services/          # 비즈니스 로직
│   │   ├── DisImageService.py   # AI 이미지 분석
│   │   ├── user_service.py      # 사용자 서비스
│   │   ├── log_service.py       # 로그 서비스
│   │   ├── image_service.py     # 이미지 파일 관리
│   │   └── descriptionService.py # 설명 서비스
│   └── db/                # 데이터베이스 설정
├── model/                 # AI 모델 파일
│   ├── best_model.keras   # 알약 분류 모델 (54MB)
│   └── oxford_flowers_model.h5  # 꽃 분류 모델 (10MB)
├── build/                 # 모바일 앱 빌드 파일
│   └── *.apk             # Android APK 파일들
├── templates/             # HTML 템플릿
│   ├── admin/            # 관리자 페이지
│   └── download.html     # 앱 다운로드 페이지
└── alembic/              # 데이터베이스 마이그레이션
```

### **API 설계 원칙**
- **RESTful API**: 표준 HTTP 메서드 및 상태 코드 사용
- **비동기 처리**: FastAPI의 async/await 패턴 활용
- **계층형 구조**: 프레젠테이션 - 비즈니스 - 데이터 계층 분리
- **의존성 주입**: FastAPI Depends를 통한 의존성 관리

---

## 🤖 AI 모델 상세

### **알약 분류 모델** (`best_model.keras`)
- **아키텍처**: EfficientNet 기반 커스텀 모델
- **학습 데이터**: 한국 의약품 50여 종
- **입력 크기**: 224×224 RGB 이미지
- **전처리**: EfficientNet 표준 전처리 적용
- **신뢰도 임계값**: 80% (0.8) 이상에서만 결과 제공
- **지원 의약품**: 미래트리메부틴정, 콘택골드캡슐, 노바스크정, 타이레놀 등 50종

### **꽃 분류 모델** (`oxford_flowers_model.h5`)
- **데이터셋**: Oxford Flowers 102
- **클래스 수**: 102개 꽃 종류
- **입력 크기**: 224×224 RGB 이미지
- **용도**: 시스템 테스트 및 데모

---

## 📡 API 엔드포인트

### **🔍 알약 분석 API**
```http
POST /api/disPill/
Content-Type: multipart/form-data

{
  "file": [이미지 파일 (PNG, JPG, JPEG)]
}
```

**응답 예시:**
```json
{
  "message": "알약 이미지 판별 성공",
  "name": "미래트리메부틴정 100mg/병",
  "description": "식도역류 및 열공헤르니아, 위 십이지장염..."
}
```

### **🌸 꽃 분석 API**
```http
POST /api/disPill/flower
Content-Type: multipart/form-data

{
  "file": [이미지 파일]
}
```

### **👥 사용자 관리 API**
```http
GET /api/users/{email}        # 사용자 조회
POST /api/users/              # 사용자 등록
POST /api/users/login         # 사용자 로그인
POST /api/users/update        # 사용자 정보 수정
DELETE /api/users/{email}     # 사용자 삭제
```

### **📊 로그 관리 API**
```http
POST /api/logs/                    # 로그 생성
GET /api/logs/{email}              # 사용자별 로그 조회
GET /api/logs/image/{image_path}   # 이미지 파일 조회
```

### **⚙️ 관리자 대시보드**
```http
GET /admin/login         # 관리자 로그인 페이지
GET /admin/dashboard     # 관리자 대시보드
GET /admin/users         # 사용자 관리 페이지
GET /admin/logs          # 로그 관리 페이지
DELETE /admin/logs/{id}  # 특정 로그 삭제
DELETE /admin/logs       # 모든 로그 삭제
PUT /admin/users/{id}    # 사용자 정보 수정
DELETE /admin/users/{email} # 사용자 삭제
```

### **📱 릴리즈 관리 API**
```http
GET /release/download    # 모바일 앱 다운로드 페이지
```

---

## 🚀 설치 및 실행

### **1. 환경 요구사항**
- Python 3.11 이상

### **2. 저장소 클론**
```bash
git clone [repository-url]
cd pill-mobile-server
```

### **3. 가상환경 설정**
```bash
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### **4. 의존성 설치**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **5. 환경 변수 설정**
`.env` 파일 생성:
```bash
# 데이터베이스 설정 (MySQL)
DATABASE_URL=mysql+pymysql://username:password@localhost/pilldb

# 또는 SQLite (개발용)
# DATABASE_URL=sqlite:///./pill.db

# JWT 설정
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 서버 설정
PORT=8883
UPLOAD_DIR=/home/horizon/pill/uploads
```

### **6. 데이터베이스 마이그레이션**
```bash
alembic upgrade head
```

### **7. 서버 실행**
```bash
python run.py
```

서버가 `http://localhost:8883`에서 실행됩니다.

---

## 📚 API 문서

### **자동 생성 문서**
- **Swagger UI**: http://localhost:8883/docs
- **ReDoc**: http://localhost:8883/redoc
- **OpenAPI Schema**: http://localhost:8883/openapi.json

### **관리자 계정**
- **아이디**: `admin`
- **비밀번호**: `wjdqhqhdks`

### **모바일 앱 다운로드**
- **다운로드 페이지**: http://localhost:8883/release/download

---

## 📝 로그 및 모니터링

### **로그 확인**
```bash
# 시스템 로그 (systemd 환경)
sudo journalctl -u pill-server -f

# 애플리케이션 로그
tail -f logs/app.log
```

### **데이터베이스 관리**
```bash
# 현재 마이그레이션 상태 확인
alembic current

# 마이그레이션 히스토리
alembic history

# 특정 버전으로 롤백
alembic downgrade <revision_id>
```

---

## 🔧 개발 정보

### **개발 환경**
- **IDE**: VS Code, PyCharm
- **버전 관리**: Git

### **배포 환경**
- **웹 서버**: Uvicorn
---

## 📞 연락처

- **개발자**: [alkjfgh]
- **이메일**: alkfgh@gmail.com
- **GitHub**: https://github.com/alkjfgh
- **이슈 리포트**: [GitHub Issues](https://github.com/alkjfgh/pill-mobile-server/issues)