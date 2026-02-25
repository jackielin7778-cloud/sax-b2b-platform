"""
台灣薩克斯風B2B交易平台 - FastAPI 後端
Zeabur 部署專用
包含商品管理、圖片上傳功能
"""
import os
import base64
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 建立目錄
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 建立 FastAPI 應用
app = FastAPI(
    title="台灣薩克斯風B2B交易平台 API",
    description="後端 API 服務",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 靜態文件服務（圖片）
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ============== 資料模型 ==============
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    brand: str
    category: str  # Alto, Tenor, Soprano, Baritone
    model: Optional[str] = None
    year: Optional[int] = None
    material: Optional[str] = None
    condition: str  # New, Used
    price: Optional[float] = None
    description: Optional[str] = None
    images: List[str] = []  # 圖片URL列表
    status: str = "active"  # active, inactive
    created_at: Optional[str] = None

# ============== 模擬資料庫 ==============
# 簡單的記憶體資料庫
products_db: List[Product] = []
next_id = 1

# ============== 工具函數 ==============
def save_product_images(files: List[UploadFile]) -> List[str]:
    """儲存上傳的圖片"""
    image_urls = []
    for file in files:
        if file and file.filename:
            # 產生唯一檔名
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            filepath = UPLOAD_DIR / filename
            
            # 儲存檔案
            content = file.read()
            with open(filepath, "wb") as f:
                f.write(content)
            
            image_urls.append(f"/uploads/{filename}")
    return image_urls

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

# ============== 商品相關 API ==============

@app.get("/api/products")
async def get_products(
    page: int = 1,
    limit: int = 20,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    status: str = "active"
):
    """取得商品列表"""
    global products_db
    
    # 過濾商品
    filtered = products_db
    if status:
        filtered = [p for p in filtered if p.status == status]
    if category:
        filtered = [p for p in filtered if p.category == category]
    if brand:
        filtered = [p for p in filtered if p.brand == brand]
    
    # 分頁
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]
    
    return {
        "products": [p.dict() for p in paginated],
        "total": len(filtered),
        "page": page,
        "limit": limit
    }

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """取得單一商品"""
    global products_db
    for p in products_db:
        if p.id == product_id:
            return p.dict()
    raise HTTPException(status_code=404, detail="商品不存在")

@app.post("/api/products")
async def create_product(
    name: str = Form(...),
    brand: str = Form(...),
    category: str = Form(...),
    model: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    material: Optional[str] = Form(None),
    condition: str = Form("New"),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    files: List[UploadFile] = File([])
):
    """建立商品（包含圖片上傳）"""
    global products_db, next_id
    
    # 儲存圖片
    image_urls = save_product_images(files)
    
    # 建立商品
    product = Product(
        id=next_id,
        name=name,
        brand=brand,
        category=category,
        model=model,
        year=year,
        material=material,
        condition=condition,
        price=price,
        description=description,
        images=image_urls,
        status="active"
    )
    products_db.append(product)
    next_id += 1
    
    return {
        "message": "商品建立成功",
        "product": product.dict()
    }

@app.put("/api/products/{product_id}")
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    brand: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    material: Optional[str] = Form(None),
    condition: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    files: List[UploadFile] = File([])
):
    """更新商品"""
    global products_db
    
    for i, p in enumerate(products_db):
        if p.id == product_id:
            # 儲存新圖片
            new_images = save_product_images(files)
            
            # 更新資料
            if name is not None:
                p.name = name
            if brand is not None:
                p.brand = brand
            if category is not None:
                p.category = category
            if model is not None:
                p.model = model
            if year is not None:
                p.year = year
            if material is not None:
                p.material = material
            if condition is not None:
                p.condition = condition
            if price is not None:
                p.price = price
            if description is not None:
                p.description = description
            if status is not None:
                p.status = status
            if new_images:
                p.images.extend(new_images)
            
            return {
                "message": "商品更新成功",
                "product": p.dict()
            }
    
    raise HTTPException(status_code=404, detail="商品不存在")

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    """刪除商品"""
    global products_db
    
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db.pop(i)
            return {"message": "商品刪除成功"}
    
    raise HTTPException(status_code=404, detail="商品不存在")

# ============== 圖片相關 ==============
@app.get("/api/images/{filename}")
async def get_image(filename: str):
    """取得圖片"""
    filepath = UPLOAD_DIR / filename
    if filepath.exists():
        return FileResponse(filepath)
    raise HTTPException(status_code=404, detail="圖片不存在")

# ============== 分類相關 ==============
@app.get("/api/categories")
async def get_categories():
    """取得商品分類"""
    return {
        "categories": ["Alto", "Tenor", "Soprano", "Baritone"],
        "brands": ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth", "其他"],
        "conditions": ["New", "Used"]
    }

# ============== 範例資料 ==============
@app.post("/api/seed")
async def seed_data():
    """建立範例資料"""
    global products_db, next_id
    
    sample_products = [
        Product(
            id=1,
            name="Mark VI Tenor Saxophone",
            brand="Selmer",
            category="Tenor",
            model="Mark VI",
            year=1965,
            material="Brass",
            condition="Used",
            price=12000.0,
            description="經典 Mark VI 中音薩克斯風，狀態良好",
            images=[],
            status="active"
        ),
        Product(
            id=2,
            name="YAS-62 Alto Saxophone",
            brand="Yamaha",
            category="Alto",
            model="YAS-62",
            year=2020,
            material="Brass",
            condition="New",
            price=3200.0,
            description="Yamaha 專業級中音薩克斯風",
            images=[],
            status="active"
        ),
        Product(
            id=3,
            name="Reference 54 Alto",
            brand="Selmer",
            category="Alto",
            model="Reference 54",
            year=2022,
            material="Brass",
            condition="New",
            price=7500.0,
            description="向 Mark VI 致敬的經典型號",
            images=[],
            status="active"
        ),
    ]
    
    products_db = sample_products
    next_id = 4
    
    return {"message": "範例資料建立成功", "count": len(sample_products)}

# ============== Zeabur Serverless 入口 ==============
