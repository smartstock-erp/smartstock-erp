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
# إعدادات الصفحة
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="متجر Curex للمستلزمات الطبية",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# الهوية البصرية والواجهة الطبية الاحترافية (ألوان متوازنة ومريحة للعين)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

    :root {
        --bg-main: #F1F5F9;
        --primary: #0284C7;
        --secondary: #0369A1;
        --medical-green: #16A34A;
        --warning: #D97706;
        --danger: #DC2626;
        --text-main: #0F172A;
        --card-bg: #FFFFFF;
        --border-color: #CBD5E1;
    }

    .stApp {
        background-color: var(--bg-main);
        font-family: 'Cairo', sans-serif;
        color: var(--text-main);
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: var(--text-main) !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated-section {
        animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Hero Section الطبي */
    .hero-section {
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
        border: 1px solid #7DD3FC;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 35px;
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* الشريط العلوي والنوافذ */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border-bottom: 2px solid #CBD5E1;
        padding: 15px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-left: 1px solid #CBD5E1;
        direction: rtl;
    }

    /* بطاقات KPI الكبيرة الاحترافية */
    .kpi-card-medical {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #CBD5E1;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .kpi-card-medical:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.15);
        border-color: var(--primary);
    }

    .kpi-title-large {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0369A1 !important;
        margin-bottom: 10px;
    }

    .kpi-number-large {
        font-size: 36px !important;
        font-weight: 900 !important;
        color: #0F172A;
    }

    /* بطاقات المنتجات الطبية */
    .product-medical-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    .product-medical-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.15);
    }

    .product-icon-box {
        font-size: 36px;
        color: #0284C7;
        background: #E0F2FE;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px auto;
    }

    /* النماذج وحقول الإدخال */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: var(--text-main) !important;
        border-radius: 10px !important;
        border: 1px solid #94A3B8 !important;
        font-weight: 600 !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2) !important;
    }

    /* الأزرار الحديثة */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 0.7rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4) !important;
    }

    /* الجداول الاحترافية */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #CBD5E1;
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

# -----------------------------------------------------------------------------
# دوال إدارة البيانات
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

df_products, df_trans, df_inventory = load_data()

# -----------------------------------------------------------------------------
# تنسيق الرسوم البيانية (Plotly)
# -----------------------------------------------------------------------------
def style_plot(fig, title_text):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0F172A", size=13, family="Cairo"),
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(color="#0369A1", size=18, family="Cairo")),
        legend=dict(font=dict(color="#0F172A", size=12)),
        margin=dict(t=50, b=30, l=30, r=30)
    )
    return fig

def draw_charts(df_inventory, df_trans):
    st.markdown("<br><h3 style='margin-bottom: 25px; color: #0369A1;'>📊 التحليلات والتقارير الطبية</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_trans.empty and "Date" in df_trans.columns and "Quantity" in df_trans.columns:
            fig_line = px.line(df_trans, x="Date", y="Quantity", color="Item Name" if "Item Name" in df_trans.columns else None, template="plotly_white", markers=True)
            st.plotly_chart(style_plot(fig_line, "حركة المستلزمات اليومية (Line Chart)"), use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لرسم الخط البياني للحركات.")

    with col2:
        if not df_inventory.empty:
            fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", template="plotly_white", color="Current Balance", color_continuous_scale="Blues")
            st.plotly_chart(style_plot(fig_bar, "مستوى المخزون الحالي (Bar Chart)"), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if not df_inventory.empty:
            fig_pie = px.pie(df_inventory, names="Item Name", values="Current Balance", template="plotly_white", hole=0.3)
            st.plotly_chart(style_plot(fig_pie, "توزيع المخزون النسبي (Pie Chart)"), use_container_width=True)

    with col4:
        if not df_inventory.empty:
            sold_col = "Total Sold" if "Total Sold" in df_inventory.columns else "Current Balance"
            fig_donut = px.pie(df_inventory, names="Item Name", values=sold_col, template="plotly_white", hole=0.6)
            st.plotly_chart(style_plot(fig_donut, "حصة مبيعات المنتجات (Donut Chart)"), use_container_width=True)

    c_best, c_least = st.columns(2)
    with c_best:
        st.markdown("""
            <div class="kpi-card-medical">
                <div style="font-size: 18px; color: #16A34A; font-weight: 800; margin-bottom: 8px;"><i class="bi bi-award-fill"></i> أكثر المنتجات مبيعًا</div>
                <p style="font-size: 18px; font-weight: 700; color: #0F172A;">الأعلى طلباً في المنظومة الطبية</p>
            </div>
        """, unsafe_allow_html=True)
        if not df_inventory.empty:
            top_prod = df_inventory.sort_values(by="Current Balance", ascending=False).iloc[0]["Item Name"]
            st.success(f"المنتج الأبرز: **{top_prod}**")

    with c_least:
        st.markdown("""
            <div class="kpi-card-medical">
                <div style="font-size: 18px; color: #DC2626; font-weight: 800; margin-bottom: 8px;"><i class="bi bi-exclamation-triangle-fill"></i> أقل المنتجات بالمخزون</div>
                <p style="font-size: 18px; font-weight: 700; color: #0F172A;">تتطلب إعادة توريد عاجل</p>
            </div>
        """, unsafe_allow_html=True)
        if not df_inventory.empty:
            low_prod = df_inventory.sort_values(by="Current Balance", ascending=True).iloc[0]["Item Name"]
            st.error(f"المنتج الأقل: **{low_prod}**")

# -----------------------------------------------------------------------------
# لوحة التحكم الرئيسية (Dashboard)
# -----------------------------------------------------------------------------
def create_dashboard():
    st.markdown("""
        <div class="animated-section">
            <h1 style="font-size: 32px; margin-bottom: 10px; color: #0369A1;"><i class="bi bi-speedometer2"></i> لوحة التحكم الإدارية</h1>
            <p style="color: #475569; font-size: 15px; margin-bottom: 25px;">متابعة شاملة لحالة المخزون، العمليات، والمؤشرات الحيوية للمتجر الطبي.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 28px; color: #0284C7; margin-bottom: 8px;"><i class="bi bi-box-seam"></i></div>
                <div class="kpi-title-large">📦 إجمالي المنتجات</div>
                <div class="kpi-number-large">{len(df_products)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 28px; color: #16A34A; margin-bottom: 8px;"><i class="bi bi-arrow-repeat"></i></div>
                <div class="kpi-title-large">🔄 إجمالي العمليات والطلبات</div>
                <div class="kpi-number-large">{len(df_trans)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)]) if not df_inventory.empty else 0
        st.markdown(f"""
            <div class="kpi-card-medical">
                <div style="font-size: 28px; color: #DC2626; margin-bottom: 8px;"><i class="bi bi-exclamation-octagon"></i></div>
                <div class="kpi-title-large">🚨 منتجات تحتاج للطلب</div>
                <div class="kpi-number-large">{reorder_count}</div>
            </div>
        """, unsafe_allow_html=True)

    draw_charts(df_inventory, df_trans)

    st.markdown("<hr style='border-color: #CBD5E1; margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("📋 تفاصيل المخزون الطبي الحالي")
    search_inv = st.text_input("بحث سريع في المخزون...", key="search_inv_db")
    filtered_df_inv = df_inventory.copy()
    if search_inv and not df_inventory.empty:
        filtered_df_inv = df_inventory[df_inventory["Item Name"].astype(str).str.contains(search_inv, case=False, na=False)]
    st.dataframe(filtered_df_inv, use_container_width=True)

    st.markdown("<hr style='border-color: #CBD5E1; margin: 35px 0;'>", unsafe_allow_html=True)
    st.subheader("📝 سجل الطلبات والعمليات")
    st.dataframe(df_trans, use_container_width=True)

# -----------------------------------------------------------------------------
# صفحة المتجر الاحترافية
# -----------------------------------------------------------------------------
def create_store():
    st.markdown("""
        <div class="hero-section animated-section">
            <div>
                <h1 style="font-size: 32px; color: #0369A1; margin-bottom: 10px;"><i class="bi bi-hospital"></i> متجر Curex للمستلزمات الطبية</h1>
                <p style="font-size: 15px; color: #334155; max-width: 600px;">نوفر أحدث الأجهزة والمستلزمات الطبية والدوائية بأعلى معايير الجودة والنظافة لتلبية احتياجات القطاع الصحي.</p>
            </div>
            <div style="font-size: 60px;">🩺</div>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px; color: #0369A1;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            
            stock_badge = f'<span style="background: #DCFCE7; color: #16A34A; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-check-circle"></i> متوفر: {current_bal}</span>' if current_bal > 5 else f'<span style="background: #FEE2E2; color: #DC2626; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 12px;"><i class="bi bi-exclamation-circle"></i> قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-medical-card">
                        <div class="product-icon-box"><i class="bi bi-capsule"></i></div>
                        <h4 style="color: #0F172A; font-size: 17px; margin-bottom: 15px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 20px; margin-bottom: 20px; color: #0369A1;'>نموذج طلب مستلزم طبي</h3>", unsafe_allow_html=True)
    
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
                with st.spinner("جاري معالجة وإرسال الطلب الطبي..."):
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
                                f"عزيزي المالك،\n\nالمنتج الطبي ({c_name}) في متجر Curex وصل رصيده الحالي إلى ({new_bal})، وهو أقل من حد الطلب.\nيرجى التوريد فوراً!"
                            )

                        st.success("🎉 تم تسجيل طلبك الطبي بنجاح لدى Curex، وسيتم التواصل معك للتسليم والشحن!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى ملء البيانات الأساسية (الاسم، الهاتف، العنوان، المنتج).")

# -----------------------------------------------------------------------------
# الشريط العلوي وتجربة المستخدم
# -----------------------------------------------------------------------------
current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="top-nav animated-section">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 22px; color: #0284C7;"><i class="bi bi-heart-pulse-fill"></i></span>
            <span style="font-size: 17px; font-weight: 800; color: #0369A1;">Curex Medical ERP</span>
        </div>
        <div style="font-size: 13px; color: #0369A1; background: #E0F2FE; padding: 5px 12px; border-radius: 20px; border: 1px solid #7DD3FC;">
            <i class="bi bi-clock"></i> الوقت الحالي: {current_time_str}
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: #16A34A; font-weight: 700; font-size: 13px;"><i class="bi bi-check-circle-fill"></i> متصل وجاهز</span>
            <span style="background: #E2E8F0; color: #0F172A; padding: 6px 10px; border-radius: 50%; font-size: 14px;"><i class="bi bi-person-fill"></i></span>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# الشريط الجانبي (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 15px 0;" class="animated-section">
            <div style="font-size: 40px; color: #0284C7; margin-bottom: 6px;"><i class="bi bi-plus-square-fill"></i></div>
            <h1 style="font-size: 22px; color: #0369A1; margin-bottom: 0; font-weight: 900;">Curex Medical</h1>
            <p style="font-size: 12px; color: #475569; margin-top: 4px;">متجر المستلزمات الطبية</p>
        </div>
        <hr style="border-color: #CBD5E1; margin-bottom: 15px;">
    """, unsafe_allow_html=True)
    
    app_mode = st.selectbox("🎯 اختر واجهة الاستخدام", [
        "متجر Curex الطبي", 
        "لوحة التحكم الرئيسية"
    ])
    
    st.markdown("---")
    admin_pass = st.text_input("🔒 كلمة مرور الأدمن", type="password")

# -----------------------------------------------------------------------------
# التنقل بين واجهات النظام
# -----------------------------------------------------------------------------
if app_mode == "متجر Curex الطبي":
    create_store()
else:
    if admin_pass == "lklklk900AR4":
        create_dashboard()
        
        st.markdown("<hr style='border-color: #CBD5E1; margin: 35px 0;'>", unsafe_allow_html=True)
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
# الفوتر الاحترافي (Footer)
# -----------------------------------------------------------------------------
st.markdown("""
    <hr style='border-color: #CBD5E1; margin-top: 50px;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #475569; font-size: 13px; padding-bottom: 25px;' class='animated-section'>
        <div>
            <strong style="color: #0369A1;">Curex Medical ERP</strong> - نظام إدارة المستلزمات الطبية المتطور
        </div>
        <div>
            &copy; 2026 جميع الحقوق محفوظة
        </div>
        <div style="display: flex; gap: 20px;">
            <span><i class="bi bi-globe"></i> الموقع الرسمي</span>
            <span><i class="bi bi-shield-check"></i> الأمان الطبي</span>
            <span><i class="bi bi-headset"></i> الدعم الفني</span>
        </div>
    </div>
""", unsafe_allow_html=True)
