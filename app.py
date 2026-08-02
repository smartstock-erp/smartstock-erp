import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.express as px
from datetime import datetime
import time

# -----------------------------------------------------------------------------
# إعدادات الصفحة والأداء (التاسع والعاشر والثاني عشر)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Curex Medical ERP",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# التصميم المحدث بالكامل (سادسًا، سابعًا، ثامنًا) - نظام الألوان الحديث SaaS
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    :root {
        --primary: #2563eb;
        --secondary: #0ea5e9;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.75);
        --border-color: rgba(37, 99, 235, 0.25);
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Cairo', sans-serif;
        color: #f8fafc;
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #f8fafc !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    /* أنيميشن */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated-section {
        animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* الشريط العلوي الحديث Top Navigation */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(14, 165, 233, 0.2);
        padding: 15px 30px;
        border-radius: 18px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    /* الشريط الجانبي Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(25px);
        border-left: 1px solid rgba(37, 99, 235, 0.2);
        direction: rtl;
    }

    /* بطاقات KPI الكبيرة مع Gradient Border و Glass Effect */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 30px;
        position: relative;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border: 1px solid var(--border-color);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 20px;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0; left: 0; height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }

    .kpi-card:hover {
        transform: translateY(-6px);
        border-color: var(--secondary);
        box-shadow: 0 25px 50px rgba(14, 165, 233, 0.25);
    }

    .kpi-title {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        margin-bottom: 8px;
    }

    .kpi-number {
        font-size: 42px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #f8fafc 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .kpi-trend {
        font-size: 13px;
        font-weight: 700;
        color: var(--success);
        background: rgba(16, 185, 129, 0.15);
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
    }

    /* بطاقات المنتجات الاحترافية Product Card */
    .product-card-saas {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.35s ease;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .product-card-saas:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 20px 40px rgba(37, 99, 235, 0.25);
    }

    .product-img-placeholder {
        font-size: 50px;
        background: rgba(37, 99, 235, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(37, 99, 235, 0.2);
    }

    /* حقول الإدخال */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid rgba(37, 99, 235, 0.3) !important;
        font-weight: 600 !important;
    }

    /* الأزرار الاحترافية */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 0.75rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35) !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(14, 165, 233, 0.4) !important;
    }

    /* الجداول الاحترافية */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(37, 99, 235, 0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

# -----------------------------------------------------------------------------
# إدارة البيانات والتخزين المؤقت (الثاني عشر)
# -----------------------------------------------------------------------------
@st.cache_resource
def get_smtp_server():
    return "smtp.gmail.com"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_products = pd.read_excel(file_path, sheet_name="Products")
    df_trans = pd.read_excel(file_path, sheet_name="Transactions")
    df_inventory = pd.read_excel(file_path, sheet_name="Inventory Balance")
    return df_products, df_trans, df_inventory

def save_data(df_products, df_trans, df_inventory):
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df_products.to_excel(writer, sheet_name="Products", index=False)
        df_trans.to_excel(writer, sheet_name="Transactions", index=False)
        df_inventory.to_excel(writer, sheet_name="Inventory Balance", index=False)
    st.cache_data.clear()

def send_email_alert(subject, body):
    try:
        sender_email = st.secrets["EMAIL_USER"]
        sender_password = st.secrets["EMAIL_PASS"]
        receiver_email = st.secrets["RECEIVER_EMAIL"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(get_smtp_server(), 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"فشل إرسال الإيميل: {e}")

# تحميل البيانات الأولية
df_products, df_trans, df_inventory = load_data()

# -----------------------------------------------------------------------------
# تنسيق الرسوم البيانية (ثانيًا، تاسعًا)
# -----------------------------------------------------------------------------
def style_plot(fig, title_text):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", size=13, family="Cairo"),
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(color="#0ea5e9", size=18, family="Cairo")),
        legend=dict(font=dict(color="#f8fafc", size=12)),
        margin=dict(t=50, b=30, l=30, r=30)
    )
    return fig

def draw_charts(df_inventory, df_trans):
    st.markdown("<br><h3 style='margin-bottom: 25px; color: #0ea5e9; text-align: right;'>📊 التحليلات والتقارير الاحترافية</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_trans.empty and "Date" in df_trans.columns and "Quantity" in df_trans.columns:
            fig_line = px.line(df_trans, x="Date", y="Quantity", color="Item Name" if "Item Name" in df_trans.columns else None, template="plotly_dark", markers=True)
            st.plotly_chart(style_plot(fig_line, "حركة المستلزمات اليومية (Line Chart)"), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لرسم الخط البياني للحركات.")

    with col2:
        if not df_inventory.empty:
            fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", template="plotly_dark", color="Current Balance", color_continuous_scale="Blues")
            st.plotly_chart(style_plot(fig_bar, "مستوى المخزون الحالي (Bar Chart)"), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if not df_inventory.empty:
            fig_pie = px.pie(df_inventory, names="Item Name", values="Current Balance", template="plotly_dark", hole=0.3)
            st.plotly_chart(style_plot(fig_pie, "توزيع المخزون النسبي (Pie Chart)"), use_container_width=True)

    with col4:
        if not df_inventory.empty:
            sold_col = "Total Sold" if "Total Sold" in df_inventory.columns else "Current Balance"
            fig_donut = px.pie(df_inventory, names="Item Name", values=sold_col, template="plotly_dark", hole=0.6)
            st.plotly_chart(style_plot(fig_donut, "حصة مبيعات المنتجات (Donut Chart)"), use_container_width=True)

    # عرض أكثر المنتجات مبيعًا وأقلها بالمخزون
    c_best, c_least = st.columns(2)
    with c_best:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 20px; color: #10b981; font-weight: 800; margin-bottom: 10px;">⭐ أكثر المنتجات مبيعًا</div>
                <p style="font-size: 24px; font-weight: 900;">الأعلى طلباً في النظام</p>
            </div>
        """, unsafe_allow_html=True)
        if not df_inventory.empty:
            top_prod = df_inventory.sort_values(by="Current Balance", ascending=False).iloc[0]["Item Name"]
            st.success(f"المنتج الأبرز: **{top_prod}**")

    with c_least:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 20px; color: #ef4444; font-weight: 800; margin-bottom: 10px;">⚠️ أقل المنتجات بالمخزون</div>
                <p style="font-size: 24px; font-weight: 900;">تتطلب إعادة توريد عاجل</p>
            </div>
        """, unsafe_allow_html=True)
        if not df_inventory.empty:
            low_prod = df_inventory.sort_values(by="Current Balance", ascending=True).iloc[0]["Item Name"]
            st.error(f"المنتج الأقل: **{low_prod}**")

# -----------------------------------------------------------------------------
# لوحة التحكم الرئيسية (أولًا، تاسعًا)
# -----------------------------------------------------------------------------
def create_dashboard():
    st.markdown("""
        <div class="animated-section">
            <h1 style="font-size: 38px; margin-bottom: 10px; color: #0ea5e9;"> لوحة التحكم الرئيسية - SaaS Dashboard</h1>
            <p style="color: #94a3b8; font-size: 16px; margin-bottom: 30px;">نظرة شاملة ومحدثة على كافة مؤشرات الأداء الحيوية لمتجر Curex الطبي.</p>
        </div>
    """, unsafe_allow_html=True)

    # الصف الأول: 4 بطاقات KPI كبيرة الحجم (34px)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 28px; margin-bottom: 10px;">📦</div>
                <div class="kpi-title">المنتجات</div>
                <div class="kpi-number">{len(df_products)}</div>
                <span class="kpi-trend">+12% هذا الشهر</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 28px; margin-bottom: 10px;">🔄</div>
                <div class="kpi-title">العمليات</div>
                <div class="kpi-number">{len(df_trans)}</div>
                <span class="kpi-trend">+8% نشط</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)]) if not df_inventory.empty else 0
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 28px; margin-bottom: 10px;">⚠️</div>
                <div class="kpi-title">التنبيهات</div>
                <div class="kpi-number">{reorder_count}</div>
                <span class="kpi-trend" style="color: #f59e0b; background: rgba(245, 158, 11, 0.15);">تحتاج توريد</span>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        total_stock = df_inventory["Current Balance"].sum() if not df_inventory.empty and "Current Balance" in df_inventory.columns else 0
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 28px; margin-bottom: 10px;">📊</div>
                <div class="kpi-title">إجمالي الرصيد</div>
                <div class="kpi-number">{total_stock}</div>
                <span class="kpi-trend">+5% مستقر</span>
            </div>
        """, unsafe_allow_html=True)

    # الرسوم البيانية
    draw_charts(df_inventory, df_trans)

    # الجداول الاحترافية (ثامنًا)
    st.markdown("<hr style='border-color: rgba(37,99,235,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("📋 سجل المخزون الطبي الحالي")
    search_inv = st.text_input("بحث سريع في المخزون...", key="search_inv_db")
    filtered_df_inv = df_inventory.copy()
    if search_inv and not df_inventory.empty:
        filtered_df_inv = df_inventory[df_inventory["Item Name"].astype(str).str.contains(search_inv, case=False, na=False)]
    st.dataframe(filtered_df_inv, use_container_width=True)

    st.markdown("<hr style='border-color: rgba(37,99,235,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("📝 سجل العمليات والطلبات")
    st.dataframe(df_trans, use_container_width=True)

# -----------------------------------------------------------------------------
# صفحة المتجر الاحترافية (ثالثًا، تاسعًا)
# -----------------------------------------------------------------------------
def create_store():
    st.markdown("""
        <div class="animated-section" style="background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.95)); border-radius: 24px; padding: 40px; border: 1px solid rgba(14,165,233,0.2); margin-bottom: 35px;">
            <h1 style="font-size: 38px; color: #0ea5e9; margin-bottom: 10px;">💊 متجر Curex للمستلزمات الطبية والدوائية</h1>
            <p style="font-size: 16px; color: #cbd5e1;">تصفح المنتجات الطبية المتاحة، وقم بإتمام طلباتك بكل سهولة وأمان عبر النظام.</p>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 35px; margin-bottom: 25px; color: #0ea5e9;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            
            stock_badge = f'<span style="background: rgba(16,185,129,0.2); color: #10b981; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">متوفر: {current_bal}</span>' if current_bal > 5 else f'<span style="background: rgba(239,68,68,0.2); color: #ef4444; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-card-saas">
                        <div class="product-img-placeholder">🩺</div>
                        <h4 style="color: #f8fafc; font-size: 18px; margin-bottom: 15px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 25px; margin-bottom: 25px; color: #0ea5e9;'>إتمام طلب جديد</h3>", unsafe_allow_html=True)
    
    with st.form("customer_order_full"):
        c_name = st.selectbox("اختر المستلزم الطبي المطلوب", df_inventory["Item Name"].tolist() if "Item Name" in df_inventory.columns else [])
        c_qty = st.number_input("الكمية المطلوبة", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            c_buyer = st.text_input("اسمك الكريم / اسم المؤسسة الطبية")
            c_phone = st.text_input("رقم الهاتـف / الجوال")
        with col2:
            c_email = st.text_input("البريد الإلكتروني")
            c_payment = st.selectbox("طريقة الدفع", ["الدفع عند الاستلام (Cash)", "تحويل بنكي", "بطاقة ائتمان"])
            
        c_address = st.text_area("عنوان التوصيل أو اسم العيادة/المستشفى بالتفصيل")
        
        submit_order = st.form_submit_button("تأكيد وإرسال الطلب الطبي")
        if submit_order:
            if c_buyer and c_phone and c_address and c_name:
                with st.spinner("جاري معالجة وإرسال الطلب..."):
                    time.sleep(1)
                    try:
                        idx = df_inventory[df_inventory["Item Name"] == c_name].index
                        if not idx.empty:
                            current_bal = df_inventory.loc[idx[0], "Current Balance"]
                            new_bal = max(0, current_bal - c_qty)
                            df_inventory.loc[idx[0], "Current Balance"] = new_bal
                            
                            if "Total Sold" in df_inventory.columns:
                                df_inventory.loc[idx[0], "Total Sold"] += c_qty
                            else:
                                df_inventory.loc[idx[0], "Total Sold"] = c_qty

                        order_notes = f"الاسم: {c_buyer} | الهاتف: {c_phone} | الإيميل: {c_email} | الدفع: {c_payment} | العنوان: {c_address}"
                        new_t = pd.DataFrame([{
                            "Item Name": c_name, "Transaction Type": "طلب عميل جديد",
                            "Quantity": c_qty, "Notes": order_notes,
                            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        }])
                        df_trans_updated = pd.concat([df_trans, new_t], ignore_index=True)
                        
                        save_data(df_products, df_trans_updated, df_inventory)

                        reorder_val = df_inventory.loc[idx[0], "Reorder Point"]
                        if new_bal <= int(str(reorder_val).replace("Reorder", "").strip() or 0):
                            send_email_alert(
                                f"⚠️ تنبيه عاجل: نقص مخزون الصنف الطبي {c_name}",
                                f"عزيزي المالك،\n\nالمنتج الطبي ({c_name}) في براند Curex وصل رصيده الحالي إلى ({new_bal})، وهو أقل من حد الطلب.\nيرجى التوريد فوراً!"
                            )

                        st.success("🎉 تم تسجيل طلبك الطبي بنجاح لدى Curex، وسيتم التواصل معك للتسليم والشحن!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى ملء البيانات الأساسية (الاسم، الهاتف، العنوان، المنتج).")

# -----------------------------------------------------------------------------
# الشريط العلوي الحديث Top Navigation (رابعًا)
# -----------------------------------------------------------------------------
current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="top-nav animated-section">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 26px;">💊</span>
            <span style="font-size: 20px; font-weight: 800; color: #0ea5e9;">Curex Medical ERP</span>
        </div>
        <div style="font-size: 14px; color: #94a3b8; background: rgba(14,165,233,0.1); padding: 6px 15px; border-radius: 20px; border: 1px solid rgba(14,165,233,0.2);">
            🕒 الوقت الحالي: {current_time_str}
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: #10b981; font-weight: 700; font-size: 13px;">🟢 متصل وجاهز</span>
            <span style="background: rgba(37,99,235,0.2); padding: 8px 12px; border-radius: 50%; font-size: 16px;">👤</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# الشريط الجانبي Sidebar (خامساً)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;" class="animated-section">
            <div style="font-size: 55px; margin-bottom: 10px;">🩺</div>
            <h1 style="font-size: 28px; color: #0ea5e9; margin-bottom: 0; font-weight: 900;">Curex SaaS</h1>
            <p style="font-size: 13px; color: #94a3b8; margin-top: 5px;">إدارة المستلزمات الطبية الذكية</p>
        </div>
        <hr style="border-color: rgba(37,99,235,0.2); margin-bottom: 25px;">
    """, unsafe_allow_html=True)
    
    app_mode = st.selectbox("🎯 اختر واجهة الاستخدام", [
        "متجر Curex الطبي", 
        "لوحة التحكم الرئيسية"
    ])
    
    st.markdown("---")
    admin_pass = st.text_input("🔒 كلمة مرور الأدمن", type="password")

# -----------------------------------------------------------------------------
# التوجيه بين الصفحات بناءً على اختيار المستخدم
# -----------------------------------------------------------------------------
if app_mode == "متجر Curex الطبي":
    create_store()
else:
    if admin_pass == "lklklk900AR4":
        create_dashboard()
        
        # قسم إضافة صنف طبي جديد للإدارة
        st.markdown("<hr style='border-color: rgba(37,99,235,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("➕ إضافة صنف طبى جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج أو الدواء الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للمخزن")
            
            if p_submit and p_name:
                new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder, "Total Sold": 0}])
                df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                save_data(df_products, df_trans, df_inventory_updated)
                st.success(f"✅ تم إضافة الصنف الطبي '{p_name}' بنجاح!")
                st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة مرور الأدمن الصحيحة في القائمة الجانبية لعرض لوحة التحكم الكاملة.")

# -----------------------------------------------------------------------------
# الفوتر الاحترافي Footer (عاشرًا)
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style='border-color: rgba(37,99,235,0.2); margin-top: 60px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #94a3b8; font-size: 14px; padding-bottom: 30px;' class='animated-section'>
        <div>
            <strong style="color: #0ea5e9;">Curex Medical ERP</strong> - الإصدار 3.0 الاحترافي
        </div>
        <div>
            &copy; 2026 جميع الحقوق محفوظة
        </div>
        <div style="display: flex; gap: 15px;">
            <span>🌐 Web</span>
            <span>📱 App</span>
            <span>✉️ Support</span>
        </div>
    </div>
""", unsafe_allow_html=True)
