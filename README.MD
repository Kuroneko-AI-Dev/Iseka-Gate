# Isekai Gate Project

Isekai Gate adalah AI Virtual Assistant berbasis React, Vite, FastAPI, dan Live2D Cubism SDK.

## Teknologi

* React
* Vite
* FastAPI
* PostgreSQL
* Live2D Cubism SDK for Web
* WebGL

---

# Instalasi

Clone project

```bash
git clone <repository>
```

Masuk ke folder frontend

```bash
cd frontend
```

Install dependency

```bash
npm install
```

Jalankan development server

```bash
npm run dev
```

Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

# Struktur Project

```
frontend/
│
├── public/
│   └── live2d/
│
├── src/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   └── live2d/
│
└── docs/
```

---

# Live2D

Semua dokumentasi integrasi Live2D berada pada

```
docs/live2d.md
```

---

# Menambah Model Live2D

1. Masukkan folder model ke

```
public/live2d/
```

Contoh

```
public/
└── live2d/
    └── Hiyori/
```

2. Edit

```
src/live2d/app/lappdefine.ts
```

ubah

```ts
export const Model = [
    "Hiyori"
];
```

Tidak perlu mengubah React Component.

---

# Menjalankan

Frontend

```bash
npm run dev
```

Backend

```bash
uvicorn main:app --reload
```


```bash
npm run dev -- --host
```


```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```