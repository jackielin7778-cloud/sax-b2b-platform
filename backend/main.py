"""
台灣薩克斯風B2B交易平台 - FastAPI 後端
Zeabur 部署專用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 建立 FastAPI 應用
app = FastAPI(
    title="台灣薩克斯風B2B交易平台 API",
    description="後端 API 服務",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該限制網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== API 路由 ==============
@app.get("/")
async def root():
    return {
        "message": "台灣薩克斯風B2B交易平台 API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ============== 會員相關 ==============
@app.post("/api/auth/register")
async def register(email: str, password: str, company_name: str):
    """會員註冊"""
    return {"message": "註冊成功", "email": email}

@app.post("/api/auth/login")
async def login(email: str, password: str):
    """會員登入"""
    return {"message": "登入成功", "token": "dummy_token"}

# ============== 商品相關 ==============
@app.get("/api/products")
async def get_products(
    page: int = 1,
    limit: int = 20,
    category: str = None,
    brand: str = None
):
    """取得商品列表"""
    return {
        "products": [],
        "total": 0,
        "page": page,
        "limit": limit
    }

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """取得商品詳情"""
    return {"id": product_id, "name": "Sample Product"}

# ============== 詢價相關 ==============
@app.post("/api/inquiry")
async def create_inquiry(product_id: int, message: str):
    """建立詢價"""
    return {"message": "詢價已發送", "inquiry_id": 1}

# ============== 訂單相關 ==============
@app.get("/api/orders")
async def get_orders():
    """取得訂單列表"""
    return {"orders": []}

@app.post("/api/orders")
async def create_order():
    """建立訂單"""
    return {"message": "訂單已建立", "order_id": 1}

# ============== 訊息相關 ==============
@app.get("/api/messages")
async def get_messages():
    """取得訊息列表"""
    return {"messages": []}

@app.post("/api/messages")
async def send_message(receiver_id: int, content: str):
    """發送訊息"""
    return {"message": "訊息已發送"}

# ============== 庫存相關 ==============
@app.get("/api/inventory")
async def get_inventory():
    """取得庫存"""
    return {"inventory": []}

# ============== 帳務相關 ==============
@app.get("/api/finance/invoices")
async def get_invoices():
    """取得發票列表"""
    return {"invoices": []}

@app.get("/api/finance/reports")
async def get_reports():
    """取得報表"""
    return {"reports": []}

# ============== 啟動訊息 ==============
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # Zeabur 環境需要綁定 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=port)
