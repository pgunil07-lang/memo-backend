import os

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models

Base.metadata.create_all(bind=engine)   # 앱 시작 시 테이블이 없으면 생성

app = FastAPI(title="Memo API", description="메모 CRUD API (React 프론트엔드 연동 실습용)")

# ── CORS 설정 ──────────────────────────────────────────
# 바뀌는 값은 코드가 아니라 환경변수로: ALLOWED_ORIGINS="https://a.vercel.app,https://b.com"
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_origin_regex=r"https://.*\.vercel\.app",   # Vercel 프리뷰/프로덕션 주소는 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청마다 DB 세션을 열고, 끝나면 반드시 닫는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── 데이터 모델 (Pydantic v2) ──────────────────────────
class MemoIn(BaseModel):        # 요청 본문: 클라이언트가 보내는 데이터
    content: str


class MemoOut(BaseModel):       # 응답 본문: 서버가 돌려주는 데이터
    id: int
    content: str
    model_config = {"from_attributes": True}  # ORM 객체 → Pydantic 변환 허용(v2 문법)


# ── 엔드포인트 ─────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Memo API is running", "docs": "/docs", "memos": "/memos"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/memos", response_model=list[MemoOut])
def list_memos(db: Session = Depends(get_db)):
    return db.query(models.Memo).all()


@app.post("/memos", response_model=MemoOut)
def create_memo(memo: MemoIn, db: Session = Depends(get_db)):
    new = models.Memo(content=memo.content)
    db.add(new); db.commit(); db.refresh(new)
    return new


@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Memo, memo_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Memo not found")
    db.delete(obj); db.commit()
    return {"ok": True}
