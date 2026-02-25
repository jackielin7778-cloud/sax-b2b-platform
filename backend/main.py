"""
台灣薩克斯風B2B交易平台 - FastAPI 後端
完整版 API（包含所有功能）
"""
import os
import uuid
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

# 目錄
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="台灣薩克斯風B2B交易平台 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ============== 資料模型 ==============
class User(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    company_name: str
    role: str = "buyer"  # buyer, seller, admin
    created_at: Optional[str] = None

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    model: Optional[str] = None
    year: Optional[int] = None
    material: Optional[str] = None
    condition: str = "New"
    price: Optional[float] = None
    stock: int = 0
    description: Optional[str] = None
    images: List[str] = []
    status: str = "active"
    created_at: Optional[str] = None

class Inquiry(BaseModel):
    id: Optional[int] = None
    product_id: int
    buyer_id: int
    message: str
    status: str = "pending"  # pending, replied, accepted, rejected
    created_at: Optional[str] = None

class CartItem(BaseModel):
    id: Optional[int] = None
    buyer_id: int
    product_id: int
    quantity: int = 1

class Order(BaseModel):
    id: Optional[int] = None
    order_number: str
    buyer_id: int
    seller_id: int
    items: List[dict] = []
    total_amount: float
    status: str = "pending"  # pending, paid, shipped, completed, cancelled
    payment_method: Optional[str] = None
    shipping_address: Optional[str] = None
    created_at: Optional[str] = None

class Message(BaseModel):
    id: Optional[int] = None
    sender_id: int
    receiver_id: int
    content: str
    read: bool = False
    created_at: Optional[str] = None

class Review(BaseModel):
    id: Optional[int] = None
    product_id: int
    buyer_id: int
    rating: int  # 1-5
    comment: Optional[str] = None
    created_at: Optional[str] = None

# ============== 模擬資料庫 ==============
users_db: List[User] = []
products_db: List[Product] = []
inquiries_db: List[Inquiry] = []
cart_db: List[CartItem] = []
orders_db: List[Order] = []
messages_db: List[Message] = []
reviews_db: List[Review] = []

next_id = {
    "user": 1, "product": 1, "inquiry": 1,
    "cart": 1, "order": 1, "message": 1, "review": 1
}

def now():
    return datetime.now().isoformat()

def save_images(files: List[UploadFile]) -> List[str]:
    urls = []
    for f in files:
        if f and f.filename:
            ext = os.path.splitext(f.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            filepath = UPLOAD_DIR / filename
            with open(filepath, "wb") as fp:
                fp.write(f.read())
            urls.append(f"/uploads/{filename}")
    return urls

# ============== 根路由 ==============
@app.get("/")
def root():
    return {"message": "台灣薩克斯風B2B交易平台 API", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# ============== 會員系統 ==============
@app.post("/api/auth/register")
def register(email: str = Form(...), password: str = Form(...), company_name: str = Form(...), role: str = Form("buyer")):
    for u in users_db:
        if u.email == email:
            raise HTTPException(status_code=400, detail="Email 已被註冊")
    
    user = User(
        id=next_id["user"],
        email=email,
        password=password,
        company_name=company_name,
        role=role,
        created_at=now()
    )
    users_db.append(user)
    next_id["user"] += 1
    return {"message": "註冊成功", "user_id": user.id}

@app.post("/api/auth/login")
def login(email: str = Form(...), password: str = Form(...)):
    for u in users_db:
        if u.email == email and u.password == password:
            return {
                "message": "登入成功",
                "token": f"token_{u.id}_{uuid.uuid4().hex[:8]}",
                "user": {"id": u.id, "email": u.email, "company_name": u.company_name, "role": u.role}
            }
    raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

@app.get("/api/users")
def get_users():
    return {"users": [{"id": u.id, "email": u.email, "company_name": u.company_name, "role": u.role} for u in users_db]}

# ============== 商品管理 ==============
@app.get("/api/products")
def get_products(page: int = 1, limit: int = 20, category: str = None, brand: str = None, status: str = "active"):
    filtered = [p for p in products_db if p.status == status]
    if category:
        filtered = [p for p in filtered if p.category == category]
    if brand:
        filtered = [p for p in filtered if p.brand == brand]
    
    start = (page - 1) * limit
    return {
        "products": [p.dict() for p in filtered[start:start+limit]],
        "total": len(filtered),
        "page": page,
        "limit": limit
    }

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    for p in products_db:
        if p.id == product_id:
            return p.dict()
    raise HTTPException(status_code=404, detail="商品不存在")

@app.post("/api/products")
def create_product(
    name: str = Form(...), brand: str = Form(...), category: str = Form(...),
    model: str = Form(None), year: int = Form(None), material: str = Form(None),
    condition: str = Form("New"), price: float = Form(None), stock: int = Form(0),
    description: str = Form(None), files: List[UploadFile] = File([])
):
    product = Product(
        id=next_id["product"],
        name=name, brand=brand, category=category, model=model,
        year=year, material=material, condition=condition, price=price,
        stock=stock, description=description, images=save_images(files),
        status="active", created_at=now()
    )
    products_db.append(product)
    next_id["product"] += 1
    return {"message": "商品建立成功", "product": product.dict()}

@app.put("/api/products/{product_id}")
def update_product(product_id: int, name: str = Form(None), price: float = Form(None), 
                   stock: int = Form(None), status: str = Form(None)):
    for p in products_db:
        if p.id == product_id:
            if name: p.name = name
            if price: p.price = price
            if stock is not None: p.stock = stock
            if status: p.status = status
            return {"message": "更新成功", "product": p.dict()}
    raise HTTPException(status_code=404, detail="商品不存在")

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    global products_db
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db.pop(i)
            return {"message": "刪除成功"}
    raise HTTPException(status_code=404, detail="商品不存在")

# ============== 詢價系統 ==============
@app.post("/api/inquiries")
def create_inquiry(product_id: int = Form(...), buyer_id: int = Form(...), message: str = Form(...)):
    inquiry = Inquiry(
        id=next_id["inquiry"],
        product_id=product_id, buyer_id=buyer_id, message=message,
        status="pending", created_at=now()
    )
    inquiries_db.append(inquiry)
    next_id["inquiry"] += 1
    return {"message": "詢價已發送", "inquiry": inquiry.dict()}

@app.get("/api/inquiries")
def get_inquiries(buyer_id: int = None, seller_id: int = None):
    result = inquiries_db
    if buyer_id:
        result = [i for i in result if i.buyer_id == buyer_id]
    return {"inquiries": [i.dict() for i in result]}

@app.put("/api/inquiries/{inquiry_id}")
def update_inquiry(inquiry_id: int, status: str = Form(...)):
    for i in inquiries_db:
        if i.id == inquiry_id:
            i.status = status
            return {"message": "更新成功", "inquiry": i.dict()}
    raise HTTPException(status_code=404, detail="詢價不存在")

# ============== 購物車 ==============
@app.get("/api/cart")
def get_cart(buyer_id: int):
    items = [c for c in cart_db if c.buyer_id == buyer_id]
    result = []
    for c in items:
        for p in products_db:
            if p.id == c.product_id:
                result.append({
                    "cart_id": c.id,
                    "product": p.dict(),
                    "quantity": c.quantity
                })
    return {"items": result}

@app.post("/api/cart")
def add_to_cart(buyer_id: int = Form(...), product_id: int = Form(...), quantity: int = Form(1)):
    for c in cart_db:
        if c.buyer_id == buyer_id and c.product_id == product_id:
            c.quantity += quantity
            return {"message": "數量更新", "cart": c.dict()}
    
    item = CartItem(id=next_id["cart"], buyer_id=buyer_id, product_id=product_id, quantity=quantity)
    cart_db.append(item)
    next_id["cart"] += 1
    return {"message": "已加入購物車", "cart": item.dict()}

@app.delete("/api/cart/{cart_id}")
def remove_from_cart(cart_id: int):
    global cart_db
    for i, c in enumerate(cart_db):
        if c.id == cart_id:
            cart_db.pop(i)
            return {"message": "已移除"}
    raise HTTPException(status_code=404, detail="購物車項目不存在")

@app.delete("/api/cart")
def clear_cart(buyer_id: int):
    global cart_db
    cart_db = [c for c in cart_db if c.buyer_id != buyer_id]
    return {"message": "購物車已清空"}

# ============== 訂單管理 ==============
@app.post("/api/orders")
def create_order(
    buyer_id: int = Form(...), seller_id: int = Form(...),
    payment_method: str = Form(...), shipping_address: str = Form(...)
):
    # 取得購物車項目
    cart_items = [c for c in cart_db if c.buyer_id == buyer_id]
    if not cart_items:
        raise HTTPException(status_code=400, detail="購物車為空")
    
    items = []
    total = 0
    for c in cart_items:
        for p in products_db:
            if p.id == c.product_id:
                items.append({"product_id": p.id, "name": p.name, "price": p.price, "quantity": c.quantity})
                total += (p.price or 0) * c.quantity
    
    order = Order(
        id=next_id["order"],
        order_number=f"ORD{now().replace('-','').replace(':','')[2:14]}{next_id['order']}",
        buyer_id=buyer_id, seller_id=seller_id, items=items, total_amount=total,
        payment_method=payment_method, shipping_address=shipping_address,
        status="pending", created_at=now()
    )
    orders_db.append(order)
    next_id["order"] += 1
    
    # 清空購物車
    global cart_db
    cart_db = [c for c in cart_db if c.buyer_id != buyer_id]
    
    return {"message": "訂單建立成功", "order": order.dict()}

@app.get("/api/orders")
def get_orders(buyer_id: int = None, seller_id: int = None):
    result = orders_db
    if buyer_id:
        result = [o for o in result if o.buyer_id == buyer_id]
    if seller_id:
        result = [o for o in result if o.seller_id == seller_id]
    return {"orders": [o.dict() for o in result]}

@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    for o in orders_db:
        if o.id == order_id:
            return o.dict()
    raise HTTPException(status_code=404, detail="訂單不存在")

@app.put("/api/orders/{order_id}")
def update_order(order_id: int, status: str = Form(...)):
    for o in orders_db:
        if o.id == order_id:
            o.status = status
            return {"message": "更新成功", "order": o.dict()}
    raise HTTPException(status_code=404, detail="訂單不存在")

# ============== 訊息系統 ==============
@app.post("/api/messages")
def send_message(sender_id: int = Form(...), receiver_id: int = Form(...), content: str = Form(...)):
    msg = Message(
        id=next_id["message"], sender_id=sender_id, receiver_id=receiver_id,
        content=content, read=False, created_at=now()
    )
    messages_db.append(msg)
    next_id["message"] += 1
    return {"message": "訊息已發送", "message_obj": msg.dict()}

@app.get("/api/messages")
def get_messages(user_id: int):
    msgs = [m for m in messages_db if m.sender_id == user_id or m.receiver_id == user_id]
    # 標記為已讀
    for m in msgs:
        if m.receiver_id == user_id:
            m.read = True
    return {"messages": [m.dict() for m in msgs]}

# ============== 庫存管理 ==============
@app.get("/api/inventory")
def get_inventory(seller_id: int = None):
    # 簡單版本：顯示所有商品庫存
    return {
        "inventory": [
            {"product_id": p.id, "name": p.name, "stock": p.stock, "status": p.status}
            for p in products_db
        ]
    }

@app.put("/api/inventory/{product_id}")
def update_stock(product_id: int, stock: int = Form(...)):
    for p in products_db:
        if p.id == product_id:
            p.stock = stock
            return {"message": "庫存更新成功", "product": p.dict()}
    raise HTTPException(status_code=404, detail="商品不存在")

# ============== 帳務對帳 ==============
@app.get("/api/finance/invoices")
def get_invoices(seller_id: int = None):
    # 取得已完成訂單作為發票
    completed = [o for o in orders_db if o.status == "completed"]
    return {"invoices": [o.dict() for o in completed]}

@app.get("/api/finance/summary")
def get_finance_summary(seller_id: int = None):
    # 營收統計
    total_sales = sum(o.total_amount for o in orders_db if o.status in ["paid", "shipped", "completed"])
    total_orders = len([o for o in orders_db if o.status != "cancelled"])
    pending = len([o for o in orders_db if o.status == "pending"])
    
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "pending_orders": pending,
        "completed_orders": len([o for o in orders_db if o.status == "completed"])
    }

# ============== 報表分析 ==============
@app.get("/api/reports/sales")
def sales_report(period: str = "month"):
    # 簡單銷售報表
    by_brand = {}
    by_category = {}
    
    for o in orders_db:
        if o.status in ["paid", "shipped", "completed"]:
            for item in o.items:
                brand = item.get("name", "Unknown")
                by_brand[brand] = by_brand.get(brand, 0) + item.get("price", 0) * item.get("quantity", 0)
                by_category[item.get("name", "Unknown")] = by_category.get(item.get("name", "Unknown"), 0) + 1
    
    return {
        "sales_by_brand": by_brand,
        "sales_by_category": by_category,
        "total_orders": len(orders_db),
        "total_revenue": sum(o.total_amount for o in orders_db if o.status in ["paid", "shipped", "completed"])
    }

# ============== 評價系統 ==============
@app.post("/api/reviews")
def create_review(product_id: int = Form(...), buyer_id: int = Form(...), 
                   rating: int = Form(...), comment: str = Form(None)):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="評分必須在1-5之間")
    
    review = Review(
        id=next_id["review"],
        product_id=product_id, buyer_id=buyer_id, rating=rating,
        comment=comment, created_at=now()
    )
    reviews_db.append(review)
    next_id["review"] += 1
    return {"message": "評價已發布", "review": review.dict()}

@app.get("/api/reviews")
def get_reviews(product_id: int = None):
    result = reviews_db
    if product_id:
        result = [r for r in result if r.product_id == product_id]
    return {"reviews": [r.dict() for r in result]}

@app.get("/api/reviews/product/{product_id}")
def get_product_reviews(product_id: int):
    product_reviews = [r for r in reviews_db if r.product_id == product_id]
    avg_rating = sum(r.rating for r in product_reviews) / len(product_reviews) if product_reviews else 0
    return {
        "reviews": [r.dict() for r in product_reviews],
        "average_rating": round(avg_rating, 1),
        "total_reviews": len(product_reviews)
    }

# ============== 分類 ==============
@app.get("/api/categories")
def get_categories():
    return {
        "categories": ["Alto", "Tenor", "Soprano", "Baritone"],
        "brands": ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth", "其他"],
        "conditions": ["New", "Used"],
        "payment_methods": ["bank_transfer", "credit_card", "cod", "installment"]
    }

# ============== 範例資料 ==============
@app.post("/api/seed")
def seed_data():
    global products_db, users_db, next_id
    
    # 建立範例會員
    users_db = [
        User(id=1, email="admin@sax.com", password="admin123", company_name="平台管理", role="admin", created_at=now()),
        User(id=2, email="seller@sax.com", password="seller123", company_name="薩克斯風工廠", role="seller", created_at=now()),
        User(id=3, email="buyer@sax.com", password="buyer123", company_name="音樂教室", role="buyer", created_at=now()),
    ]
    next_id = {"user": 4, "product": 1, "inquiry": 1, "cart": 1, "order": 1, "message": 1, "review": 1}
    
    # 建立範例商品
    products_db = [
        Product(id=1, name="Mark VI Tenor", brand="Selmer", category="Tenor", model="Mark VI", year=1965, condition="Used", price=12000, stock=2, description="經典 Vintage", images=[], status="active", created_at=now()),
        Product(id=2, name="YAS-62 Alto", brand="Yamaha", category="Alto", model="YAS-62", year=2024, condition="New", price=3200, stock=10, description="專業級", images=[], status="active", created_at=now()),
        Product(id=3, name="Reference 54 Alto", brand="Selmer", category="Alto", model="Reference 54", year=2024, condition="New", price=7500, stock=5, description="旗艦款", images=[], status="active", created_at=now()),
        Product(id=4, name="YTS-62 Tenor", brand="Yamaha", category="Tenor", model="YTS-62", year=2024, condition="New", price=3800, stock=8, description="專業次中音", images=[], status="active", created_at=now()),
    ]
    next_id["product"] = 5
    
    return {"message": "範例資料建立成功", "users": 3, "products": 4}
