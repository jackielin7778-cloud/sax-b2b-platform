"""
台灣薩克斯風B2B交易平台 - Streamlit 前端
"""
import streamlit as st
import requests
import os
from pathlib import Path

# ============== 語系配置 ==============
LANGUAGES = {
    "zh-TW": "繁體中文",
    "zh-CN": "简体中文", 
    "ja": "日本語",
    "ko": "한국어",
    "en": "English"
}

# IP對應語系
IP_LANGUAGE_MAP = {
    "TW": "zh-TW",
    "HK": "zh-TW",
    "MO": "zh-TW",
    "CN": "zh-CN",
    "JP": "ja",
    "KR": "ko"
}

# 翻譯字典
TRANSLATIONS = {
    "zh-TW": {
        "title": "台灣薩克斯風B2B交易平台",
        "home": "首頁",
        "products": "商品瀏览",
        "inquiry": "詢價系統",
        "orders": "訂單管理",
        "messages": "訊息",
        "login": "登入",
        "register": "註冊",
        "logout": "登出",
        "welcome": "歡迎來到",
        "tagline": "全球薩克斯風B2B交易首選平台",
        "hero_title": "專業薩克斯風B2B交易平台",
        "hero_subtitle": "連接全球製造商與經銷商",
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
        "welcome": "欢迎来到",
        "tagline": "全球萨克斯风B2B交易首选平台",
        "hero_title": "专业萨克斯风B2B交易平台",
        "hero_subtitle": "连接全球制造商与经销商",
        "featured_brands": "精选品牌",
        "product_categories": "商品分类",
        "search_placeholder": "搜索商品...",
        "contact": "联系我们",
        "about": "关于我们",
    },
    "ja": {
        "title": "台湾サックスB2B取引プラットフォーム",
        "home": "ホーム",
        "products": "商品一覧",
        "inquiry": "見積依頼",
        "orders": "注文管理",
        "messages": "メッセージ",
        "login": "ログイン",
        "register": "登録",
        "logout": "ログアウト",
        "welcome": "ようこそ",
        "tagline": "世界初のサックスB2B取引プラットフォーム",
        "hero_title": "プロフェッショナルサックスB2B取引プラットフォーム",
        "hero_subtitle": "世界の製造業者とディーラーをつなぐ",
        "featured_brands": "おすすめブランド",
        "product_categories": "商品カテゴリー",
        "search_placeholder": "商品を検索...",
        "contact": "お問い合わせ",
        "about": "会社概要",
    },
    "ko": {
        "title": "태국 색소폰 B2B 거래 플랫폼",
        "home": "홈",
        "products": "상품 보기",
        "inquiry": "견적 문의",
        "orders": "주문 관리",
        "messages": "메시지",
        "login": "로그인",
        "register": "회원가입",
        "logout": "로그아웃",
        "welcome": "오신 것을 환영합니다",
        "tagline": "세계 최초 색소폰 B2B 거래 플랫폼",
        "hero_title": "프로фессиональ 색소폰 B2B 거래 플랫폼",
        "hero_subtitle": "전 세계 제조업체와ディ러 연결",
        "featured_brands": "추천 브랜드",
        "product_categories": "상품 카테고리",
        "search_placeholder": "상품 검색...",
        "contact": "문의하기",
        "about": "회사 소개",
    },
    "en": {
        "title": "Taiwan Saxophone B2B Trading Platform",
        "home": "Home",
        "products": "Products",
        "inquiry": "Inquiry",
        "orders": "Orders",
        "messages": "Messages",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "welcome": "Welcome to",
        "tagline": "The Premier B2B Saxophone Trading Platform",
        "hero_title": "Professional Saxophone B2B Trading Platform",
        "hero_subtitle": "Connecting Global Manufacturers with Dealers",
        "featured_brands": "Featured Brands",
        "product_categories": "Product Categories",
        "search_placeholder": "Search products...",
        "contact": "Contact Us",
        "about": "About Us",
    }
}

# ============== 語系偵測 ==============
def get_client_ip():
    """取得客戶端IP"""
    try:
        # 嘗試從請求頭取得
        headers = {
            'User-Agent': 'Streamlit'
        }
        response = requests.get('https://api.ipify.org?format=json', headers=headers, timeout=5)
        return response.json().get('ip', '8.8.8.8')
    except:
        return '8.8.8.8'

def get_country_from_ip(ip):
    """從IP取得國碼"""
    try:
        # 使用免費的 ipapi
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        if response.status_code == 200:
            return response.json().get('country_code', 'US')
    except:
        pass
    return 'US'

def detect_language():
    """自動偵測語系"""
    # 檢查 session_state 是否有已儲存的偏好
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # 檢查 URL 參數
    params = st.query_params
    if 'lang' in params:
        lang = params['lang']
        if lang in LANGUAGES:
            st.session_state.language = lang
            return
    
    # 檢查 Cookie
    # 如果都沒有，則依 IP 偵測
    ip = get_client_ip()
    country = get_country_from_ip(ip)
    lang = IP_LANGUAGE_MAP.get(country, 'en')
    st.session_state.language = lang

def set_language(lang):
    """設定語系"""
    if lang in LANGUAGES:
        st.session_state.language = lang
        st.query_params['lang'] = lang
        st.rerun()

def t(key):
    """翻譯函數"""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

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
    /* 奢華金色主題 */
    :root {
        --primary-gold: #D4AF37;
        --secondary-gold: #C5A028;
        --dark-steel: #2C3E50;
        --warm-copper: #B87333;
        --ivory: #FAF9F6;
        --light-gray: #F5F5F5;
    }
    
    /* 導航欄 */
    .stRadio > div {
        flex-direction: row !important;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background-color: #D4AF37 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
    }
    
    /* 標題樣式 */
    h1, h2, h3 {
        color: #2C3E50 !important;
    }
    
    /* Hero 區塊 */
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
    
    /* 品牌卡片 */
    .brand-card {
        background: white;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s;
    }
    
    .brand-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* 語系選單 */
    .language-selector {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# ============== 導航欄 ==============
def render_navbar():
    """渲染導航欄"""
    lang = st.session_state.get('language', 'en')
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown(f"### 🎷 {t('title')}")
    
    with col2:
        if st.button(t('home'), use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    with col3:
        if st.button(t('products'), use_container_width=True):
            st.session_state.page = 'products'
            st.rerun()
    
    with col4:
        if st.button(t('inquiry'), use_container_width=True):
            st.session_state.page = 'inquiry'
            st.rerun()
    
    with col5:
        if st.button(t('login'), use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

# ============== 側邊欄 ==============
def render_sidebar():
    """渲染側邊欄"""
    with st.sidebar:
        st.header("🎷 Menu")
        
        # 語系選擇
        st.subheader("🌐 Language / 語言")
        current_lang = st.session_state.get('language', 'en')
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
        
        # 搜尋
        st.subheader(t('search_placeholder'))
        search_query = st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed")
        
        st.divider()
        
        # 商品分類
        st.subheader(t('product_categories'))
        categories = ["Alto Saxophone", "Tenor Saxophone", "Soprano Saxophone", "Baritone Saxophone"]
        for cat in categories:
            st.write(f"• {cat}")
        
        st.divider()
        
        # 精選品牌
        st.subheader(t('featured_brands'))
        brands = ["Selmer", "Yamaha", "Yanagisawa", "Keilwerth"]
        for brand in brands:
            st.write(f"• {brand}")

# ============== 首頁 ==============
def render_home():
    """渲染首頁"""
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t('hero_title')}</h1>
        <p class="hero-subtitle">{t('hero_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 搜尋列
    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
    with search_col1:
        st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed")
    with search_col2:
        st.button("🔍 搜尋", use_container_width=True)
    
    st.markdown("---")
    
    # 精選品牌
    st.header(f"✨ {t('featured_brands')}")
    brand_col1, brand_col2, brand_col3, brand_col4 = st.columns(4)
    
    brands = [
        ("Selmer", "法國經典", "#D4AF37"),
        ("Yamaha", "日本精工", "#2C3E50"),
        ("Yanagisawa", "日本專業", "#B87333"),
        ("Keilwerth", "德國工藝", "#34495E")
    ]
    
    for i, (brand, desc, color) in enumerate(brands):
        with [brand_col1, brand_col2, brand_col3, brand_col4][i]:
            st.markdown(f"""
            <div class="brand-card">
                <h3 style="color: {color}">{brand}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 商品分類
    st.header(f"📦 {t('product_categories')}")
    cat_col1, cat_col2, cat_col3, cat_col4 = st.columns(4)
    
    categories = [
        ("Alto", "次中音", "🎷"),
        ("Tenor", "高音", "🎷"),
        ("Soprano", "超高音", "🎷"),
        ("Baritone", "上低音", "🎷")
    ]
    
    for i, (name, desc, icon) in enumerate(categories):
        with [cat_col1, cat_col2, cat_col3, cat_col4][i]:
            st.info(f"{icon} **{name}**\n\n{desc}")

# ============== 主程式 ==============
def main():
    # 初始化
    detect_language()
    set_page_config()
    local_css()
    
    # 初始化 session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # 渲染導航
    render_navbar()
    
    # 渲染側邊欄
    render_sidebar()
    
    # 根據頁面狀態渲染內容
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'products':
        st.header(t('products'))
        st.info("商品列表頁面開發中...")
    elif st.session_state.page == 'inquiry':
        st.header(t('inquiry'))
        st.info("詢價系統開發中...")
    elif st.session_state.page == 'login':
        st.header(t('login'))
        st.info("登入/註冊頁面開發中...")
    else:
        render_home()

if __name__ == "__main__":
    main()
