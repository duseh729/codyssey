# 📝 FastAPI Todo API 예제

간단한 **FastAPI** 기반 Todo 리스트입니다.
가상환경(`venv`)을 사용하며, 의존성은 `requirements.txt`로 관리합니다.

---

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
uvicorn todo:app --reload
```
