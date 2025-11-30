# Backend

개발 환경 :
    - OS: Ubuntu 22.04
    - Python version: 3.11
    - Dependency management: Poetry
    - Database: PostgreSQL 15

run command : poetry run uvicorn app.main:app --reload

🗄 DB 스키마 (PostgreSQL)
📌 ① ideas (원본 아이디어 저장)
```
id (PK)
user_id (FK optional)
raw_text (TEXT)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

➡️ 사용자 입력 원문 저장

📌 ② idea_metadata (요약 + 키워드 + classification 결과 저장)
```
id (PK)
idea_id (FK → ideas)
summary TEXT
keywords TEXT[]
tech_stack TEXT[]
difficulty INT
category TEXT
quality_score FLOAT
```

➡️ LLM 호출 결과 저장
➡️ 후속 검색 / 클러스터링 / 추천용 데이터

📌 ③ idea_vectors (벡터 DB)
```
id PK
idea_id FK → ideas

summary_vector VECTOR(1536)
keyword_vector VECTOR(1536)
tech_vector VECTOR(1536)

combined_vector VECTOR(1536)   ← 요약/키워드/기술 스택 weighted sum 벡터
```

벡터	설명
summary_vector	검색 정확도 높음 (내용 기반)
keyword_vector	빠른 태그 기반 검색
tech_vector	기술 스택 기반 추천
combined_vector	RAG/추천 시스템 최종 검색

📌 ④ competitions (대회/공모전/문제 정보)
```
id PK
title TEXT
description TEXT
source TEXT  (kaggle / 공모전 / hackathon)
created_at TIMESTAMP
```

📌 ⑤ competition_vectors
```
id PK
competition_id FK → competitions
vector VECTOR(1536)
```