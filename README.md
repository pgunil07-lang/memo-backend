# memo-backend

메모 CRUD API. FastAPI + SQLAlchemy(SQLite)로 만들고 Render에 배포한다.
프론트엔드 저장소: https://github.com/pgunil07-lang/memo-frontend

## 배포 주소

- API: https://<서비스>.onrender.com  ← 배포 후 채운다
- Swagger UI: https://<서비스>.onrender.com/docs

## 구성

| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI 앱, CORS 설정, 엔드포인트 3종 |
| `database.py` | DB 엔진·세션. `DATABASE_URL` 환경변수로 SQLite ↔ PostgreSQL 전환 |
| `models.py` | `memos` 테이블 모델 |
| `requirements.txt` | Render가 설치할 패키지 목록 |

## API

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/memos` | 메모 목록 |
| POST | `/memos` | 메모 추가 `{"content": "..."}` |
| DELETE | `/memos/{id}` | 메모 삭제 |
| GET | `/health` | 상태 확인 |

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py             # http://127.0.0.1:8000/docs
```

## Render 설정

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- 환경변수: `ALLOWED_ORIGINS` = Vercel 배포 주소 (예: `https://memo-frontend-xxxx.vercel.app`)

무료 플랜은 파일시스템이 임시라서 재배포·슬립 시 SQLite 데이터가 초기화된다.
