"""
台灣薩克斯風B2B交易平台 - Streamlit 前端
完整版（包含所有功能）
"""
import streamlit as st
import requests
from datetime import datetime

# ============== API 設定 ==============
API_BASE_URL = "https://sax-b2b-platform.zeabur.app"

# ============== 翻譯 ==============
TRANSLATIONS = {
    "zh-TW": {
        "title": "台灣薩克斯風B2B交易平台", "home": "首頁", "products": "商品",
        "cart": "購物車", "orders": "訂單", "messages": "訊息", "inquiry": "詢價",
        "login": "登入", "register": "註冊", "admin": "後台", "logout": "登出",
        "product_mgmt": "商品管理", "inventory": "庫存管理", "finance": "帳務",
        "add_product": "新增商品", "featured_brands": "精選品牌", "search": "搜尋...",
        "qty": "數量", "price": "價格", "total": "總計", "checkout": "結帳",
        "no_items": "購物車是空的", "order_success": "訂單建立成功！",
        "name": "名稱", "brand": "品牌", "category": "類型", "model": "型號",
        "year": "年份", "condition": "狀態", "description": "說明",
        "stock": "庫存", "status": "狀態", "actions": "操作",
    },
    "en": {
        "title": "Taiwan Sax B2B", "home": "Home", "products": "Products",
        "cart": "Cart", "orders": "Orders", "messages": "Messages", "inquiry": "Inquiry",
        "login": "Login", "register": "Register", "admin": "Admin", "logout": "Logout",
        "product_mgmt": "Products", "inventory": "Inventory", "finance": "Finance",
        "add_product": "Add Product", "featured_brands": "Brands", "search": "Search...",
        "qty": "Qty", "price": "Price", "total": "Total", "checkout": "Checkout",
        "no_items": "Cart is empty", "order_success": "Order created!",
        "name": "Name", "brand": "Brand", "category": "Category", "model": "Model",
        "year": "Year", "condition": "Condition", "description": "Description",
        "stock": "Stock", "status": "Status", "actions": "Actions",
    }
}

def t(key):
    lang = st.session_state.get('language', 'zh-TW')
    return TRANSLATIONS.get(lang, TRANSLATIONS['zh-TW']).get(key, key)

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

def api_put(url, data=None):
    try:
        r = requests.put(f"{API_BASE_URL}{url}", data=data, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def api_delete(url):
    try:
        return requests.delete(f"{API_BASE_URL}{url}", timeout=10).status_code == 200
    except:
        return False

# ============== 頁面配置 ==============
st.set_page_config(page_title="台灣薩克斯風B2B", page_icon="🎷", layout="wide")

# CSS
st.markdown("""
<style>
    :root { --primary-gold: #D4AF37; --dark-steel: #2C3E50; }
    .stButton > button { background-color: #D4AF37 !important; color: white !important; }
    h1, h2, h3 { color: #2C3E50 !important; }
    .hero { background: linear-gradient(135deg, #2C3E50, #1a252f); padding: 50px; border-radius: 10px; text-align: center; }
    .hero h1 { color: #D4AF37 !important; }
    .hero p { color: white; font-size: 20px; }
    .brand-card { border: 2px solid #D4AF37; border-radius: 10px; padding: 20px; text-align: center; background: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #F0F2F6; border-radius: 4px 4px 0px 0px; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37; color: white; }
</style>
""", unsafe_allow_html=True)

# ============== 初始化 ==============
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'user' not in st.session_state: st.session_state.user = None

# ============== 側邊欄 ==============
with st.sidebar:
    st.header("🎷 Menu")
    
    # 語言
    lang = st.selectbox("語言", ["zh-TW", "en"], format_func=lambda x: "中文" if x == "zh-TW" else "English")
    if lang != st.session_state.get('language'):
        st.session_state.language = lang
    
    st.divider()
    
    # 登入狀態
    if st.session_state.user:
        st.write(f"👤 {st.session_state.user.get('company_name', 'User')}")
        st.write(f"📧 {st.session_state.user.get('email', '')}")
        if st.button(t("logout"), key="logout_btn"):
            st.session_state.user = None
            st.rerun()
    else:
        st.warning("未登入")
        if st.button("🔐 " + t("login"), key="login_btn"):
            st.session_state.page = t("login")
            st.rerun()
    
    st.divider()
    
    # 導航
    pages = [t("home"), t("products"), t("cart"), t("orders"), t("inquiry"), t("messages"), t("admin"), t("login")]
    choice = st.radio("導航", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    st.session_state.page = choice
    
    st.divider()
    
    # API 測試
    if st.button("🔌 API 狀態"):
        result = api_get("/health")
        st.success(f"✅ 連線正常" if result else "❌ 連線失敗")

# ============== 頁面：首頁 ==============
def page_home():
    st.markdown(f"""
    <div class="hero">
        <h1>🎷 {t('title')}</h1>
        <p>連接全球製造商與經銷商</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("✨ " + t("featured_brands"))
    cols = st.columns(4)
    brands = [("Selmer", "法國"), ("Yamaha", "日本"), ("Yanagisawa", "日本"), ("Keilwerth", "德國")]
    for i, (b, c) in enumerate(brands):
        with cols[i]:
            st.markdown(f'<div class="brand-card"><h3>{b}</h3><p>{c}</p></div>', unsafe_allow_html=True)
    
    st.subheader("📦 商品分類")
    cats = ["Alto", "Tenor", "Soprano", "Baritone"]
    cols = st.columns(4)
    for i, c in enumerate(cats):
        with cols[i]:
            st.info(f"🎷 **{c}**")

# ============== 頁面：商品 ==============
def page_products():
    st.header("🎷 " + t("products"))
    
    # 篩選
    c1, c2, c3 = st.columns(3)
    with c1:
        cat_filter = st.selectbox("類型", ["全部", "Alto", "Tenor", "Soprano", "Baritone"])
    with c2:
        brand_filter = st.selectbox("品牌", ["全部", "Selmer", "Yamaha", "Yanagisawa", "Keilwerth"])
    with c3:
        status_filter = st.selectbox("狀態", ["active", "inactive"])
    
    params = {}
    if cat_filter != "全部": params["category"] = cat_filter
    if brand_filter != "全部": params["brand"] = brand_filter
    params["status"] = status_filter
    
    result = api_get("/api/products", params)
    
    if result and result.get('products'):
        for p in result['products']:
            with st.expander(f"🔹 {p['name']} - ${p.get('price', 'N/A')}"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.write(f"**品牌:** {p['brand']} | **類型:** {p['category']}")
                    st.write(f"**型號:** {p.get('model', '-')} | **年份:** {p.get('year', '-')}")
                    st.write(f"**狀態:** {p['condition']} | **庫存:** {p.get('stock', 0)}")
                with c2:
                    if p.get('images'):
                        st.image(p['images'][0], width=150)
                    if st.session_state.user and st.button(f"🛒 加入購物車", key=f"add_{p['id']}"):
                        res = api_post("/api/cart", {"buyer_id": st.session_state.user['id'], "product_id": p['id']})
                        if res and "error" not in res:
                            st.success("已加入購物車！")
    else:
        st.info("尚無商品")

# ============== 頁面：購物車 ==============
def page_cart():
    st.header("🛒 " + t("cart"))
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    result = api_get(f"/api/cart?buyer_id={st.session_state.user['id']}")
    
    if not result or not result.get('items'):
        st.info(t("no_items"))
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
        with c4: 
            if st.button(f"🗑️", key=f"del_cart_{item['cart_id']}"):
                api_delete(f"/api/cart/{item['cart_id']}")
                st.rerun()
    
    st.divider()
    st.write(f"### {t('total')}: ${total}")
    
    # 結帳
    with st.form("checkout"):
        payment = st.selectbox("付款方式", ["bank_transfer", "credit_card", "cod", "installment"])
        address = st.text_area("收貨地址")
        if st.button(t("checkout"), type="primary"):
            if not address:
                st.error("請填寫收貨地址")
            else:
                # 找第一個 seller（簡化）
                seller_id = 2
                res = api_post("/api/orders", {
                    "buyer_id": st.session_state.user['id'],
                    "seller_id": seller_id,
                    "payment_method": payment,
                    "shipping_address": address
                })
                if res and "error" not in res:
                    st.success(t("order_success"))
                    st.rerun()

# ============== 頁面：訂單 ==============
def page_orders():
    st.header("📋 " + t("orders"))
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    user_id = st.session_state.user['id']
    result = api_get(f"/api/orders?buyer_id={user_id}")
    
    if result and result.get('orders'):
        for o in result['orders']:
            with st.expander(f"📦 {o['order_number']} - {o['status']} - ${o['total_amount']}"):
                st.write(f"**狀態:** {o['status']}")
                st.write(f"**日期:** {o.get('created_at', '-')}")
                st.write(f"**付款方式:** {o.get('payment_method', '-')}")
                st.write(f"**收貨地址:** {o.get('shipping_address', '-')}")
                st.write("**商品:**")
                for item in o.get('items', []):
                    st.write(f"  - {item.get('name')} x{item.get('quantity')} = ${item.get('price')}")
    else:
        st.info("尚無訂單")

# ============== 頁面：詢價 ==============
def page_inquiry():
    st.header("💬 " + t("inquiry"))
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    # 發詢價
    with st.form("inquiry_form"):
        product_id = st.number_input("商品ID", min_value=1)
        message = st.text_area("詢價訊息")
        if st.button("發送詢價", type="primary"):
            res = api_post("/api/inquiries", {
                "product_id": product_id,
                "buyer_id": st.session_state.user['id'],
                "message": message
            })
            if res and "error" not in res:
                st.success("詢價已發送！")
                st.rerun()
    
    st.divider()
    
    # 查看詢價
    result = api_get(f"/api/inquiries?buyer_id={st.session_state.user['id']}")
    if result and result.get('inquiries'):
        for i in result['inquiries']:
            st.write(f"📨 商品ID:{i['product_id']} - 狀態:{i['status']}")
            st.write(f"   {i['message']}")
            st.write("---")

# ============== 頁面：訊息 ==============
def page_messages():
    st.header("✉️ " + t("messages"))
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    # 發訊息
    with st.form("msg_form"):
        receiver_id = st.number_input("收件人ID", min_value=1)
        content = st.text_area("訊息內容")
        if st.button("發送", type="primary"):
            res = api_post("/api/messages", {
                "sender_id": st.session_state.user['id'],
                "receiver_id": receiver_id,
                "content": content
            })
            if res and "error" not in res:
                st.success("訊息已發送！")
                st.rerun()
    
    st.divider()
    
    # 查看訊息
    result = api_get(f"/api/messages?user_id={st.session_state.user['id']}")
    if result and result.get('messages'):
        for m in result['messages']:
            st.write(f"{'⬅️ 傳出' if m['sender_id'] == st.session_state.user['id'] else '➡️ 收到'}: {m['content']}")
            st.caption(m.get('created_at', ''))
            st.write("---")

# ============== 頁面：後台 ==============
def page_admin():
    st.header("🎛️ " + t("admin"))
    
    if not st.session_state.user:
        st.warning("請先登入")
        return
    
    tabs = st.tabs([t("product_mgmt"), t("add_product"), t("inventory"), t("finance")])
    
    # 商品管理
    with tabs[0]:
        st.subheader("📋 " + t("product_mgmt"))
        result = api_get("/api/products")
        if result and result.get('products'):
            for p in result['products']:
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                with c1: st.write(f"**{p['name']}**")
                with c2: st.write(f"庫存:{p.get('stock', 0)}")
                with c3: st.write(f"${p.get('price', 0)}")
                with c4:
                    if st.button("🗑️", key=f"del_{p['id']}"):
                        api_delete(f"/api/products/{p['id']}")
                        st.rerun()
    
    # 新增商品
    with tabs[1]:
        st.subheader("➕ " + t("add_product"))
        with st.form("new_product"):
            name = st.text_input("商品名稱 *")
            brand = st.selectbox("品牌 *", ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth", "其他"])
            category = st.selectbox("類型 *", ["Alto", "Tenor", "Soprano", "Baritone"])
            model = st.text_input("型號")
            year = st.number_input("年份", 1900, 2030, 2024)
            condition = st.selectbox("狀態", ["New", "Used"])
            price = st.number_input("價格", 0.0, 100000.0, 0.0)
            stock = st.number_input("庫存", 0, 10000, 0)
            desc = st.text_area("說明")
            files = st.file_uploader("圖片", type=['png','jpg','jpeg'], accept_multiple_files=True)
            
            if st.button("💾 建立", type="primary"):
                if not name:
                    st.error("請填寫名稱")
                else:
                    data = {
                        "name": name, "brand": brand, "category": category,
                        "model": model, "year": year, "condition": condition,
                        "price": price, "stock": stock, "description": desc
                    }
                    file_list = [("files", (f.name, f.getvalue(), f.type)) for f in files] if files else None
                    res = api_post("/api/products", data=data, files=file_list)
                    if res and "error" not in res:
                        st.success("✅ 建立成功！")
                        st.rerun()
    
    # 庫存
    with tabs[2]:
        st.subheader("📦 " + t("inventory"))
        result = api_get("/api/inventory")
        if result and result.get('inventory'):
            for inv in result['inventory']:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1: st.write(f"**{inv['product_id']}. {inv['name']}**")
                with c2: st.number_input("庫存", value=inv['stock'], key=f"stock_{inv['product_id']}")
                with c3:
                    if st.button("更新", key=f"upd_{inv['product_id']}"):
                        api_put(f"/api/inventory/{inv['product_id']}", {"stock": st.session_state.get(f"stock_{inv['product_id']}")})
                        st.success("更新成功")
    
    # 帳務
    with tabs[3]:
        st.subheader("💰 " + t("finance"))
        result = api_get("/api/finance/summary")
        if result:
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("總營收", f"${result.get('total_sales', 0)}")
            with c2: st.metric("總訂單", result.get('total_orders', 0))
            with c3: st.metric("待處理", result.get('pending_orders', 0))

# ============== 頁面：登入 ==============
def page_login():
    st.header("🔐 " + t("login"))
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("密碼", type="password")
        submitted = st.form_submit_button(t("login"), type="primary")
        
        if submitted:
            result = api_post("/api/auth/login", {"email": email, "password": password})
            if result and "error" not in result:
                st.session_state.user = result.get('user')
                st.success("登入成功！")
                st.rerun()
            else:
                st.error("登入失敗")
    
    st.divider()
    st.write("測試帳號：")
    st.code("Email: buyer@sax.com\n密碼: buyer123")

# ============== 主程式 ==============
def main():
    page = st.session_state.page
    
    if page == t("home"):
        page_home()
    elif page == t("products"):
        page_products()
    elif page == t("cart"):
        page_cart()
    elif page == t("orders"):
        page_orders()
    elif page == t("inquiry"):
        page_inquiry()
    elif page == t("messages"):
        page_messages()
    elif page == t("admin"):
        page_admin()
    elif page == t("login"):
        page_login()
    else:
        page_home()

if __name__ == "__main__":
    main()
