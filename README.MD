# 📚 Belajar FastAPI

## Pengenalan FastAPI

FastAPI adalah framework web modern untuk membangun API REST yang cepat dan efisien menggunakan Python. FastAPI dirancang dengan fokus pada:
- **Kecepatan**: Performa tinggi, setara dengan NodeJS dan Go
- **Kemudahan**: Mudah dipelajari dan digunakan
- **Validasi otomatis**: Menggunakan type hints Python dan Pydantic
- **Dokumentasi interaktif**: Swagger UI dan ReDoc otomatis

## 🎯 Tujuan Pembelajaran

Setelah menyelesaikan pembelajaran FastAPI, Anda akan mampu:

1. **Memahami Dasar-dasar FastAPI**
   - Membuat aplikasi FastAPI pertama
   - Memahami routing dan path parameters
   - Menggunakan query parameters dan request body

2. **Bekerja dengan Data**
   - Validasi data menggunakan Pydantic models
   - Menangani berbagai tipe data
   - Error handling yang tepat

3. **Fitur Lanjutan**
   - Authentication dan authorization
   - Database integration
   - Middleware dan CORS
   - File uploads dan downloads

4. **Best Practices**
   - Struktur project yang baik
   - Testing aplikasi
   - Deployment ke production
   - API documentation

## 📋 Prasyarat

- **Python 3.7+** (disarankan 3.10 atau lebih tinggi)
- Pemahaman dasar Python (functions, dictionaries, classes)
- Pengetahuan dasar tentang REST API
- Editor kode (VS Code, PyCharm, dll)

## 🚀 Getting Started

### 1. Instalasi FastAPI

```bash
pip install fastapi
pip install uvicorn[standard]
```

### 2. Aplikasi Pertama

Buat file `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### 3. Jalankan Server

```bash
uvicorn main:app --reload
```

Server akan berjalan di: `http://127.0.0.1:8000`

Dokumentasi interaktif tersedia di:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 📚 Topik-topik Pembelajaran

### Level Dasar
- [ ] Setup dan instalasi
- [ ] Struktur aplikasi FastAPI
- [ ] Request dan response
- [ ] Path parameters
- [ ] Query parameters
- [ ] Request body dengan Pydantic

### Level Menengah
- [ ] Model validation
- [ ] Response models
- [ ] Status codes
- [ ] Error handling
- [ ] Documentation
- [ ] Testing

### Level Lanjutan
- [ ] Database integration (SQLAlchemy)
- [ ] Authentication (JWT, OAuth2)
- [ ] CORS dan middleware
- [ ] File handling
- [ ] Background tasks
- [ ] Deployment

## 📁 Struktur Project

```
FastAPI/
├── main.py              # Entry point aplikasi
├── requirements.txt     # Dependencies
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py        # Pydantic models
│   ├── schemas.py       # Request/response schemas
│   ├── database.py      # Database configuration
│   └── routers/         # Route handlers
│       ├── users.py
│       └── items.py
├── tests/               # Unit dan integration tests
│   ├── test_main.py
│   └── test_users.py
└── README.md
```

## 🔗 Konsep Penting

### 1. Routing
```python
@app.get("/users/")
@app.post("/users/")
@app.put("/users/{user_id}")
@app.delete("/users/{user_id}")
```

### 2. Request Body dengan Pydantic
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    return user
```

### 3. Dependency Injection
```python
async def get_query(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(params: dict = Depends(get_query)):
    return params
```

### 4. Error Handling
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return {"item_id": item_id}
```

## 📖 Sumber Daya

- **Dokumentasi Resmi**: https://fastapi.tiangolo.com/
- **GitHub FastAPI**: https://github.com/tiangolo/fastapi
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Pydantic Docs**: https://docs.pydantic.dev/

## 🛠️ Tools & Dependencies

```
fastapi>=0.95.0
uvicorn[standard]>=0.21.0
pydantic>=1.10.0
sqlalchemy>=2.0.0
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.5
```

## ✅ Checklist Pembelajaran

- [ ] Instalasi FastAPI berhasil
- [ ] Membuat aplikasi Hello World
- [ ] Memahami routing basics
- [ ] Implementasi query parameters
- [ ] Implementasi request body
- [ ] Validasi data dengan Pydantic
- [ ] Error handling
- [ ] Membuat API lengkap (CRUD)
- [ ] Testing aplikasi
- [ ] Deployment ke production

## 💡 Tips & Best Practices

1. **Gunakan Type Hints** - FastAPI menggunakannya untuk validasi otomatis
2. **Dokumentasi Otomatis** - Manfaatkan Swagger UI yang disediakan
3. **Validasi Input** - Gunakan Pydantic models untuk validasi
4. **Testing** - Tulis unit tests menggunakan pytest
5. **Environment Variables** - Gunakan .env untuk konfigurasi
6. **Logging** - Implementasikan logging yang baik
7. **API Versioning** - Pertimbangkan versioning untuk API Anda

## 📝 Catatan Pembelajaran

Tambahkan catatan dan insight pembelajaran Anda di sini saat proses belajar.

---

**Mulai belajar FastAPI sekarang dan bangun API yang powerful dan scalable!** 🎉
