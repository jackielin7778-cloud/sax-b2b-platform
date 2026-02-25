"""
台灣薩克斯風B2B交易平台 - Streamlit 前端
奢華精品風格 (Selmer Style)
"""
import streamlit as st
import requests
from datetime import datetime

# ============== API 設定 ==============
API_BASE_URL = "https://sax-b2b-platform.zeabur.app"

# ============== 亮色奢華 CSS 風格 ==============
st.markdown("""
<style>
    /* 全局 - 亮色背景 */
    .stApp {
        background-color: #FAFAFA;
        color: #1A1A1A;
    }
    
    /* 標題 */
    h1, h2, h3, h4 {
        color: #B8860B !important;
        font-family: 'Georgia', serif;
        font-weight: 500;
    }
    
    /* 奢華金色 */
    :root {
        --gold: #B8860B;
        --gold-light: #D4A84B;
        --gold-dark: #8B6914;
        --cream: #FAFAFA;
        --warm-white: #F5F5F0;
        --dark: #1A1A1A;
    }
    
    /* 按鈕 */
    .stButton > button {
        background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
        color: white !important;
        border: none !important;
        border-radius: 3px !important;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: var(--gold-light) !important;
    }
    
    /* 側邊欄 */
    section[data-testid="stSidebar"] {
        background-color: #F0F0F0;
    }
    
    /* 區塊標題 */
    .section-title {
        color: #B8860B;
        font-size: 28px;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-align: center;
        margin: 40px 0 20px 0;
    }
    
    /* 品牌字體 */
    .brand-title {
        font-family: 'Georgia', serif;
        font-size: 42px;
        color: #B8860B;
        letter-spacing: 8px;
    }
    
    /* 產品卡片 */
    .product-item {
        background: white;
        border: 1px solid #E0E0E0;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .product-item:hover {
        border-color: var(--gold);
        box-shadow: 0 4px 16px rgba(184, 134, 11, 0.2);
        transform: translateY(-5px);
    }
    
    /* 測試帳號 */
    .test-account {
        color: #333333 !important;
        background: #F5F5F5;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    
    /* 分隔線 */
    hr {
        border-color: #E0E0E0;
    }
    
    /* 輸入框 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: white;
        border: 1px solid #E0E0E0;
        color: #1A1A1A;
    }
</style>
""", unsafe_allow_html=True)

# ============== 初始化 ==============
if 'page' not in st.session_state: 
    st.session_state.page = 'home'
if 'user' not in st.session_state: 
    st.session_state.user = None

# ============== API 函數 ==============
def api_get(url, params=None):
    try:
        r = requests.get(f"{API_BASE_URL}{url}", params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def api_post(url, data=None, files=None):
    try:
        r = requests.post(f"{API_BASE_URL}{url}", data=data, files=files, timeout=30)
        return r.json() if r.status_code == 200 else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}

# ============== 頁面：首頁 ==============
def page_home():
    # Hero
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(180deg, #F5F5F0 0%, #FAFAFA 100%); margin: -60px -2rem 40px -2rem; border-bottom: 1px solid #E0E0E0;">
        <h1 style="font-size: 48px; letter-spacing: 10px; color: #B8860B !important; font-family: Georgia, serif; margin-bottom: 20px;">SAXOPHONE B2B</h1>
        <p style="color: #666; font-size: 16px; letter-spacing: 4px;">全球專業薩克斯風交易平台</p>
        <p style="color: #999; font-size: 14px; margin-top: 30px;">連接製造商與經銷商的橋樑</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 精選品牌
    st.markdown('<div class="section-title">精選品牌</div>', unsafe_allow_html=True)
    
    brands = [
        ("Selmer", "法國", "1922"),
        ("Yamaha", "日本", "1964"),
        ("Yanagisawa", "日本", "1951"),
        ("Keilwerth", "德國", "1925")
    ]
    
    cols = st.columns(4)
    for i, (brand, country, year) in enumerate(brands):
        with cols[i]:
            st.markdown(f"""
            <div class="product-item" style="padding: 40px 20px; background: white;">
                <h3 style="color: #B8860B !important; font-size: 24px; margin-bottom: 15px;">{brand}</h3>
                <p style="color: #666; font-size: 14px;">{country}</p>
                <p style="color: #999; font-size: 12px;">Since {year}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 商品分類
    st.markdown('<div class="section-title">商品分類</div>', unsafe_allow_html=True)
    
    cats = [
        ("Alto", "中音薩克斯風"),
        ("Tenor", "次中音薩克斯風"),
        ("Soprano", "高音薩克斯風"),
        ("Baritone", "上低音薩克斯風")
    ]
    
    cols = st.columns(4)
    for i, (name, desc) in enumerate(cats):
        with cols[i]:
            st.markdown(f"""
            <div class="product-item">
                <h4 style="color: #B8860B !important;">{name}</h4>
                <p style="color: #666; font-size: 13px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 精選商品
    st.markdown('<div class="section-title">精選商品</div>', unsafe_allow_html=True)
    
    result = api_get("/api/products?limit=4")
    if result and result.get('products'):
        cols = st.columns(4)
        for i, p in enumerate(result['products']):
            with cols[i]:
                img_html = ""
                if p.get('images'):
                    img_html = f'<img src="{p["images"][0]}" style="width: 100%; height: 180px; object-fit: cover; margin-bottom: 15px;">'
                
                st.markdown(f"""
                <div class="product-item">
                    {img_html}
                    <h4 style="color: #B8860B !important; font-size: 16px; margin-bottom: 10px;">{p['name']}</h4>
                    <p style="color: #666; font-size: 13px;">{p.get('brand', '')} • {p.get('category', '')}</p>
                    <p style="color: #1A1A1A; font-size: 18px; margin-top: 10px;">${p.get('price', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

# ============== 頁面：商品 ==============
def page_products():
    st.markdown('<div class="section-title">全部商品</div>', unsafe_allow_html=True)
    
    # 篩選
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        cat = st.selectbox("類型", ["全部", "Alto", "Tenor", "Soprano", "Baritone"])
    with c2:
        brand = st.selectbox("品牌", ["全部", "Selmer", "Yamaha", "Yanagisawa", "Keilwerth"])
    with c3:
        status = st.selectbox("庫存", ["active", "inactive"])
    
    params = {}
    if cat != "全部": params["category"] = cat
    if brand != "全部": params["brand"] = brand
    params["status"] = status
    
    result = api_get("/api/products", params)
    
    if result and result.get('products'):
        # 網格顯示
        for i in range(0, len(result['products']), 4):
            row = result['products'][i:i+4]
            cols = st.columns(4)
            for j, p in enumerate(row):
                with cols[j]:
                    img_html = ""
                    if p.get('images'):
                        img_html = f'<img src="{p["images"][0]}" style="width: 100%; height: 180px; object-fit: cover; margin-bottom: 15px;">'
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="product-item">
                            {img_html}
                            <h4 style="color: #B8860B !important; font-size: 16px; margin-bottom: 10px;">{p['name']}</h4>
                            <p style="color: #666; font-size: 13px;">{p.get('brand', '')} • {p.get('category', '')}</p>
                            <p style="color: #1A1A1A; font-size: 18px; margin-top: 10px;">${p.get('price', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.session_state.user:
                            if st.button(f"加入購物車", key=f"add_{p['id']}"):
                                res = api_post("/api/cart", {"buyer_id": st.session_state.user['id'], "product_id": p['id']})
                                if res and "error" not in res:
                                    st.success("已加入!")
    else:
        st.info("尚無商品")

# ============== 頁面：購物車 ==============
def page_cart():
    st.markdown('<div class="section-title">購物車</div>', unsafe_allow_html=True)
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    result = api_get(f"/api/cart?buyer_id={st.session_state.user['id']}")
    
    if not result or not result.get('items'):
        st.info("購物車是空的")
        return
    
    total = 0
    for item in result['items']:
        p = item['product']
        qty = item['quantity']
        price = p.get('price', 0)
        subtotal = price * qty
        total += subtotal
        
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1: st.write(f"**{p['name']}**")
        with c2: st.write(f"x{qty}")
        with c3: st.write(f"${price}")
        with c4: st.write(f"${subtotal}")
    
    st.markdown("---")
    st.write(f"### 總計: ${total}")
    
    with st.form("checkout"):
        payment = st.selectbox("付款方式", ["bank_transfer", "credit_card", "cod", "installment"])
        address = st.text_area("收貨地址")
        if st.form_submit_button("結帳", type="primary"):
            if not address:
                st.error("請填寫地址")
            else:
                res = api_post("/api/orders", {"buyer_id": st.session_state.user['id'], "seller_id": 2, "payment_method": payment, "shipping_address": address})
                if res and "error" not in res:
                    st.success("訂單建立成功!")

# ============== 頁面：後台 ==============
def page_admin():
    st.markdown('<div class="section-title">後台管理</div>', unsafe_allow_html=True)
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    tabs = st.tabs(["商品管理", "新增商品", "庫存", "帳務"])
    
    # 商品列表
    with tabs[0]:
        result = api_get("/api/products")
        if result and result.get('products'):
            for p in result['products']:
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                with c1: st.write(f"**{p['name']}**")
                with c2: st.write(f"庫存:{p.get('stock', 0)}")
                with c3: st.write(f"${p.get('price', 0)}")
    
    # 新增商品
    with tabs[1]:
        with st.form("new_product"):
            name = st.text_input("商品名稱")
            brand = st.selectbox("品牌", ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth"])
            category = st.selectbox("類型", ["Alto", "Tenor", "Soprano", "Baritone"])
            price = st.number_input("價格", 0.0, 100000.0, 0.0)
            stock = st.number_input("庫存", 0, 10000, 0)
            files = st.file_uploader("圖片", type=['png','jpg','jpeg'])
            
            if st.form_submit_button("建立", type="primary"):
                if name:
                    form_data = {"name": name, "brand": brand, "category": category, "price": price, "stock": stock}
                    file_data = None
                    if files:
                        file_data = [("files", (files.name, files.getvalue(), files.type))]
                    res = api_post("/api/products", data=form_data, files=file_data)
                    if res and "error" not in res:
                        st.success("建立成功!")
                        st.rerun()
    
    # 庫存
    with tabs[2]:
        result = api_get("/api/inventory")
        if result and result.get('inventory'):
            for inv in result['inventory']:
                st.write(f"{inv['product_id']}. {inv['name']} - 庫存: {inv['stock']}")
    
    # 帳務
    with tabs[3]:
        result = api_get("/api/finance/summary")
        if result:
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("總營收", f"${result.get('total_sales', 0)}")
            with c2: st.metric("總訂單", result.get('total_orders', 0))
            with c3: st.metric("待處理", result.get('pending_orders', 0))

# ============== 頁面：登入 ==============
def page_login():
    st.markdown('<div class="section-title">會員登入</div>', unsafe_allow_html=True)
    
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("密碼", type="password")
        
        if st.form_submit_button("登入", type="primary"):
            result = api_post("/api/auth/login", {"email": email, "password": password})
            if result and "error" not in result:
                st.session_state.user = result.get('user')
                st.success("登入成功!")
                st.rerun()
            else:
                st.error("登入失敗")
    
    st.caption("測試帳號: buyer@sax.com / buyer123")
    
    # 亮色背景區塊
    st.markdown("""
    <div style="background: #F0F0F0; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px;">
        <p style="color: #333; font-weight: bold; margin-bottom: 5px;">測試帳號</p>
        <p style="color: #1A1A1A; font-size: 13px;">buyer@sax.com<br>buyer123</p>
    </div>
    """, unsafe_allow_html=True)

# ============== 側邊欄 ==============
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <h2 style="color: #B8860B; text-align: center; letter-spacing: 3px; margin-bottom: 30px;">MENU</h2>
        """, unsafe_allow_html=True)
        
        # 頁面選單
        pages = {
            "home": "🏠 首頁",
            "products": "🎷 商品",
            "cart": "🛒 購物車",
            "admin": "⚙️ 後台",
            "login": "🔐 登入"
        }
        
        for key, label in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
        
        st.markdown("---")
        
        # 用戶資訊
        if st.session_state.user:
            st.write(f"👤 {st.session_state.user.get('company_name', '')}")
            if st.button("登出"):
                st.session_state.user = None
                st.rerun()
        else:
            st.warning("未登入")

# ============== 主程式 ==============
def main():
    render_sidebar()
    
    page = st.session_state.page
    
    if page == "home":
        page_home()
    elif page == "products":
        page_products()
    elif page == "cart":
        page_cart()
    elif page == "admin":
        page_admin()
    elif page == "login":
        page_login()
    else:
        page_home()

if __name__ == "__main__":
    main()
