"""
台灣薩克斯風B2B交易平台 - Streamlit 前端
包含前台展示 + 後台管理
"""
import streamlit as st
import requests
import os
from pathlib import Path

# ============== API 設定 ==============
API_BASE_URL = "https://sax-b2b-platform.zeabur.app"

# ============== 語系配置 ==============
LANGUAGES = {
    "zh-TW": "繁體中文",
    "zh-CN": "簡體中文", 
    "ja": "日本語",
    "ko": "한국어",
    "en": "English"
}

IP_LANGUAGE_MAP = {
    "TW": "zh-TW",
    "HK": "zh-TW",
    "MO": "zh-TW",
    "CN": "zh-CN",
    "JP": "ja",
    "KR": "ko"
}

TRANSLATIONS = {
    "zh-TW": {
        "title": "台灣薩克斯風B2B交易平台",
        "home": "首頁",
        "products": "商品瀏覽",
        "inquiry": "詢價系統",
        "orders": "訂單管理",
        "messages": "訊息",
        "login": "登入",
        "register": "註冊",
        "logout": "登出",
        "admin": "後台管理",
        "product_management": "商品管理",
        "add_product": "新增商品",
        "edit_product": "編輯商品",
        "delete_product": "刪除商品",
        "featured_brands": "精選品牌",
        "product_categories": "商品分類",
        "search_placeholder": "搜尋商品...",
        "contact": "聯絡我們",
        "about": "關於我們",
    },
    "zh-CN": {
        "title": "台湾萨克斯风B2B交易平台",
        "home": "首页",
        "products": "商品浏览",
        "inquiry": "询价系统",
        "orders": "订单管理",
        "messages": "消息",
        "login": "登录",
        "register": "注册",
        "logout": "退出",
        "admin": "后台管理",
        "product_management": "商品管理",
        "add_product": "新增商品",
        "edit_product": "编辑商品",
        "delete_product": "删除商品",
        "featured_brands": "精选品牌",
        "product_categories": "商品分类",
        "search_placeholder": "搜索商品...",
        "contact": "联系我们",
        "about": "关于我们",
    },
    "en": {
        "title": "Taiwan Saxophone B2B Platform",
        "home": "Home",
        "products": "Products",
        "inquiry": "Inquiry",
        "orders": "Orders",
        "messages": "Messages",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "admin": "Admin",
        "product_management": "Product Management",
        "add_product": "Add Product",
        "edit_product": "Edit Product",
        "delete_product": "Delete Product",
        "featured_brands": "Featured Brands",
        "product_categories": "Categories",
        "search_placeholder": "Search products...",
        "contact": "Contact",
        "about": "About",
    }
}

# ============== API 函數 ==============
def get_api(url, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}{url}", params=params, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def post_api(url, data=None, files=None):
    try:
        if files:
            response = requests.post(f"{API_BASE_URL}{url}", data=data, files=files, timeout=30)
        else:
            response = requests.post(f"{API_BASE_URL}{url}", json=data, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return {"error": str(e)}

def put_api(url, data=None):
    try:
        response = requests.put(f"{API_BASE_URL}{url}", json=data, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def delete_api(url):
    try:
        response = requests.delete(f"{API_BASE_URL}{url}", timeout=10)
        return response.status_code == 200
    except:
        return False

# ============== 語系偵測 ==============
def detect_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'zh-TW'
    
    params = st.query_params
    if 'lang' in params:
        lang = params['lang']
        if lang in LANGUAGES:
            st.session_state.language = lang

def set_language(lang):
    if lang in LANGUAGES:
        st.session_state.language = lang
        st.query_params['lang'] = lang

def t(key):
    lang = st.session_state.get('language', 'zh-TW')
    return TRANSLATIONS.get(lang, TRANSLATIONS['zh-TW']).get(key, key)

# ============== 頁面配置 ==============
def set_page_config():
    st.set_page_config(
        page_title="台灣薩克斯風B2B交易平台",
        page_icon="🎷",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ============== 自訂CSS ==============
def local_css():
    st.markdown("""
    <style>
    :root {
        --primary-gold: #D4AF37;
        --secondary-gold: #C5A028;
        --dark-steel: #2C3E50;
        --warm-copper: #B87333;
    }
    .stButton > button {
        background-color: #D4AF37 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #2C3E50 !important;
    }
    .hero-section {
        background: linear-gradient(135deg, #2C3E50 0%, #1a252f 100%);
        padding: 60px 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-title {
        color: #D4AF37 !important;
        font-size: 48px !important;
        font-weight: bold !important;
    }
    .hero-subtitle {
        color: white !important;
        font-size: 20px !important;
    }
    .brand-card {
        background: white;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ============== 前台頁面 ==============
def render_home():
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">🎷 專業薩克斯風B2B交易平台</h1>
        <p class="hero-subtitle">連接全球製造商與經銷商</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 搜尋
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed")
    with col2:
        st.button("🔍 搜尋", use_container_width=True)
    
    st.markdown("---")
    
    # 品牌
    st.header("✨ " + t('featured_brands'))
    brands = [
        ("Selmer", "法國經典"),
        ("Yamaha", "日本精工"),
        ("Yanagisawa", "日本專業"),
        ("Keilwerth", "德國工藝")
    ]
    cols = st.columns(4)
    for i, (brand, desc) in enumerate(brands):
        with cols[i]:
            st.markdown(f"""
            <div class="brand-card">
                <h3 style="color: #D4AF37">{brand}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 分類
    st.header("📦 " + t('product_categories'))
    categories = [
        ("Alto", "中音薩克斯風", "🎷"),
        ("Tenor", "次中音薩克斯風", "🎷"),
        ("Soprano", "高音薩克斯風", "🎷"),
        ("Baritone", "上低音薩克斯風", "🎷")
    ]
    cols = st.columns(4)
    for i, (name, desc, icon) in enumerate(categories):
        with cols[i]:
            st.info(f"{icon} **{name}**\n\n{desc}")

def render_products():
    st.header(t('products'))
    
    # 取得分類
    cats = get_api("/api/categories")
    
    # 篩選
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("類型", ["全部"] + (cats.get('categories', []) if cats else []))
    with col2:
        brand_filter = st.selectbox("品牌", ["全部"] + (cats.get('brands', []) if cats else []))
    with col3:
        status_filter = st.selectbox("狀態", ["active", "inactive"])
    
    # 取得商品
    params = {}
    if category_filter != "全部":
        params['category'] = category_filter
    if brand_filter != "全部":
        params['brand'] = brand_filter
    params['status'] = status_filter
    
    result = get_api("/api/products", params)
    
    if result and result.get('products'):
        for product in result['products']:
            with st.expander(f"{product['name']} - ${product.get('price', 'N/A')}"):
                st.write(f"**品牌:** {product['brand']}")
                st.write(f"**類型:** {product['category']}")
                st.write(f"**型號:** {product.get('model', 'N/A')}")
                st.write(f"**年份:** {product.get('year', 'N/A')}")
                st.write(f"**狀態:** {product['condition']}")
                st.write(f"**說明:** {product.get('description', 'N/A')}")
                if product.get('images'):
                    st.image(product['images'][0], width=200)
    else:
        st.info("尚無商品，請至後台新增")

# ============== 後台頁面 ==============
def render_admin():
    st.header("🎛️ " + t('admin'))
    
    # 後台選單
    admin_menu = st.radio(
        "請選擇功能",
        [t('product_management'), t('add_product')],
        horizontal=True
    )
    
    if admin_menu == t('product_management'):
        render_product_list()
    elif admin_menu == t('add_product'):
        render_product_form()

def render_product_list():
    st.subheader("📋 " + t('product_management'))
    
    # 取得商品
    result = get_api("/api/products?status=active")
    
    if result and result.get('products'):
        for product in result['products']:
            with st.expander(f"🔹 {product['name']} (ID: {product['id']})"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**品牌:** {product['brand']}")
                    st.write(f"**類型:** {product['category']}")
                    st.write(f"**型號:** {product.get('model', '-')}")
                
                with col2:
                    st.write(f"**年份:** {product.get('year', '-')}")
                    st.write(f"**狀態:** {product['condition']}")
                    st.write(f"**價格:** ${product.get('price', '-')}")
                
                with col3:
                    if st.button(f"🗑️ 刪除", key=f"del_{product['id']}", type="primary"):
                        if delete_api(f"/api/products/{product['id']}"):
                            st.success("刪除成功！")
                            st.rerun()
                        else:
                            st.error("刪除失敗")
    else:
        st.info("尚無商品，請先新增")

def render_product_form():
    st.subheader("➕ " + t('add_product'))
    
    with st.form("product_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("商品名稱 *", placeholder="例如: Mark VI Tenor")
            brand = st.selectbox("品牌 *", ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth", "其他"])
            category = st.selectbox("類型 *", ["Alto", "Tenor", "Soprano", "Baritone"])
            model = st.text_input("型號", placeholder="例如: YAS-62")
        
        with col2:
            year = st.number_input("製造年份", min_value=1900, max_value=2030, step=1)
            condition = st.selectbox("商品狀態", ["New", "Used"])
            price = st.number_input("價格 (USD)", min_value=0.0, step=100.0)
            material = st.text_input("材質", placeholder="例如: Brass")
        
        description = st.text_area("商品說明", height=3)
        
        # 圖片上傳
        st.write("📷 商品圖片")
        uploaded_files = st.file_uploader(
            "選擇圖片（可多選）",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            accept_multiple_files=True
        )
        
        # 預覽圖片
        if uploaded_files:
            st.write("預覽：")
            cols = st.columns(min(len(uploaded_files), 4))
            for i, f in enumerate(uploaded_files):
                with cols[i % 4]:
                    st.image(f, width=100)
        
        submit = st.form_submit_button("💾 建立商品", type="primary")
        
        if submit:
            if not name or not brand or not category:
                st.error("請填寫必填欄位（名稱、品牌、類型）")
            else:
                # 準備資料
                data = {
                    "name": name,
                    "brand": brand,
                    "category": category,
                    "model": model,
                    "year": year if year else None,
                    "condition": condition,
                    "price": price if price else None,
                    "material": material,
                    "description": description
                }
                
                # 準備檔案
                files = []
                if uploaded_files:
                    for f in uploaded_files:
                        files.append(("files", (f.name, f.getvalue(), f.type)))
                
                # 發送請求
                result = post_api("/api/products", data=data, files=files if files else None)
                
                if result and "error" not in result:
                    st.success("✅ 商品建立成功！")
                    st.rerun()
                else:
                    st.error(f"❌ 建立失敗: {result.get('error', '未知錯誤')}")

# ============== 側邊欄 ==============
def render_sidebar():
    with st.sidebar:
        st.header("🎷 Menu")
        
        # 語系
        st.subheader("🌐 語言")
        current_lang = st.session_state.get('language', 'zh-TW')
        selected_lang = st.radio(
            "選擇語言",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            index=list(LANGUAGES.keys()).index(current_lang),
            label_visibility="collapsed"
        )
        if selected_lang != current_lang:
            set_language(selected_lang)
        
        st.divider()
        
        # 導航
        st.subheader("📍 導航")
        page = st.radio(
            "頁面",
            [t('home'), t('products'), t('admin')],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # API 測試
        st.subheader("🔌 API 狀態")
        if st.button("測試連線"):
            result = get_api("/health")
            if result:
                st.success(f"✅ 連線成功\n\n{result}")
            else:
                st.error("❌ 連線失敗")

# ============== 主程式 ==============
def main():
    detect_language()
    set_page_config()
    local_css()
    
    # 初始化
    if 'page' not in st.session_state:
        st.session_state.page = t('home')
    
    # 渲染
    render_sidebar()
    
    # 根據選擇渲染
    page = st.session_state.get('page', t('home'))
    
    # 從 radio 取得當前頁面（因為每次render都會重新創建）
    # 使用 query_params 或 session_state 來記住
    with st.sidebar:
        page_choice = st.radio(
            "導航",
            [t('home'), t('products'), t('admin')],
            index=[t('home'), t('products'), t('admin')].index(st.session_state.page) if st.session_state.page in [t('home'), t('products'), t('admin')] else 0,
            label_visibility="collapsed",
            key="page_radio"
        )
        st.session_state.page = page_choice
    
    if st.session_state.page == t('home'):
        render_home()
    elif st.session_state.page == t('products'):
        render_products()
    elif st.session_state.page == t('admin'):
        render_admin()
    else:
        render_home()

if __name__ == "__main__":
    main()
