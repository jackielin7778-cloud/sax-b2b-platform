# 台灣薩克斯風B2B交易平台

![GitHub](https://img.shields.io/github/license/example/sax-b2b-platform)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## 專案結構

```
sax-b2b-platform/
├── frontend/          # Streamlit 前端
│   ├── app.py         # 主應用
│   ├── pages/         # 頁面
│   └── requirements.txt
├── backend/           # FastAPI 後端 (Zeabur)
│   ├── main.py        # API 主程式
│   ├── routers/       # API 路由
│   └── requirements.txt
└── README.md
```

## 快速開始

### 前端（Streamlit）

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 後端（Zeabur）

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 環境變數

請參考 `.env.example` 設定環境變數。

## 技術棧

| 項目 | 技術 |
|------|------|
| 前端框架 | Streamlit |
| 後端框架 | FastAPI |
| 部署平台 | Zeabur |
| 代碼托管 | GitHub |

## License

MIT
