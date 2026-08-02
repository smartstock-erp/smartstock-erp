import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.express as px
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="SmartStock ERP Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم UI حديث مع تباين عالي ووضوح تام للنصوص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111e38 50%, #1e3a8a 100%);
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        color: #ffffff;
    }

    /* تحسين النصوص العامة والعناوين لتكون واضحة تماماً */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ستايل الـ Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(11, 17, 32, 0.95) !important;
        backdrop-filter: blur(16px);
        border-left: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* كروت الـ Glassmorphism */
    .glass-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    /* بطاقات الإحصائيات */
    .metric-big-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }

    .metric-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 50px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
    }

    /* متجر المنتجات */
    .product-store-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }

    .product-store-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.25);
    }

    .badge-stock {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 700;
        margin-top: 12px;
    }
    .badge-good { background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid #10b981; }
    .badge-danger { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }

    /* حقول الإدخال بوضوح تام وتصحيح اللون الرمادي الباهت */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(11, 17, 32, 0.9) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        font-weight: 600 !important;
    }

    /* إصلاح تباين النصوص التوضيحية فوق الحقول لتعود واضحة تماماً */
    [data-testid="stForm"] label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: #38bdf8 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    /* تخصيص الأزرار */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 0.8rem 1.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
        width: 100% !important;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 12px 25px rgba(56, 189, 248, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

file_path = "SmartStock ERP Pro.xlsx"

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

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"فشل إرسال الإيميل: {e}")

def load_data():
    if not os.path.exists(file_path):
        st.error(f"⚠️ ملف الإكسيل غير موجود: {file_path}")
        st.stop()
    df_products = pd.read_excel(file_path, sheet_name="Products")
    df_trans = pd.read_excel(file_path, sheet_name="Transactions")
    df_inventory = pd.read_excel(file_path, sheet_name="Inventory Balance")
    return df_products, df_trans, df_inventory

df_products, df_trans, df_inventory = load_data()

# شريط جانبى
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="font-size: 26px; color: #38bdf8; margin-bottom: 0;">🛍️ SmartStock</h1>
            <p style="font-size: 13px; color: #cbd5e1;">إدارة المخزون ونقاط البيع الذكية</p>
        </div>
        <hr style="border-color: rgba(255,255,255,0.15);">
    """, unsafe_allow_html=True)
    
    current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
    st.markdown(f"<div style='text-align: center; font-size: 13px; color: #38bdf8; margin-bottom: 15px;'>🕒 {current_time_str}</div>", unsafe_allow_html=True)
    
    app_mode = st.selectbox("اختر الشاشة الرئيسية", ["SmartStock", "⚙️ لوحة التحكم"])

if app_mode == "SmartStock":
    st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px; margin-bottom: 30px;">
            <h1 style="font-size: 36px; color: #38bdf8; margin-bottom: 10px;">🛍️ متجر SmartStock الرقمي</h1>
            <p style="font-size: 17px; color: #e2e8f0;">تُشرّفنا زيارتُك، تصفّح المنتجات المتاحة وأتمم طلبك بكل سهولة ويسر.</p>
        </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 ابحث عن منتج بالمخزون...", "")
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px; color: #38bdf8;'>📋 المنتجات المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
    if not df_inventory.empty:
        filtered_inv = df_inventory.copy()
        if search_query:
            filtered_inv = filtered_inv[filtered_inv["Item Name"].astype(str).str.contains(search_query, case=False, na=False)]
        
        cols = st.columns(3)
        for idx, row in filtered_inv.iterrows():
            item_name = row.get("Item Name", "منتج بدون اسم")
            current_bal = row.get("Current Balance", 0)
            
            if current_bal > 5:
                stock_badge = f'<span class="badge-stock badge-good">متوفر: {current_bal}</span>'
            else:
                stock_badge = f'<span class="badge-stock badge-danger">قارب على النفاد: {current_bal}</span>'
                
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="product-store-card">
                        <div style="font-size: 40px; margin-bottom: 10px;">📦</div>
                        <h4 style="color: #ffffff; font-size: 18px; margin-bottom: 10px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 20px; margin-bottom: 20px; color: #38bdf8;'>📝 نموذج تقديم الطلب</h3>", unsafe_allow_html=True)
    
    with st.form("customer_order_full"):
        c_name = st.selectbox("اختر المنتج المطلوب", df_inventory["Item Name"].tolist() if "Item Name" in df_inventory.columns else [])
        c_qty = st.number_input("الكمية المطلوبة", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            c_buyer = st.text_input("اسمك الكريم")
            c_phone = st.text_input("رقم الهاتـف / الجوال")
        with col2:
            c_email = st.text_input("البريد الإلكتروني")
            c_payment = st.selectbox("طريقة الدفع", ["الدفع عند الاستلام (Cash)", "تحويل بنكي / إنستاباي", "بطاقة ائتمان"])
            
        c_address = st.text_area("عنوان التوصيل بالتفصيل (المدينة، الشارع، رقم العمارة)")
        
        submit_order = st.form_submit_button("🚀 تأكيد وإرسال الطلب الآن")
        if submit_order:
            if c_buyer and c_phone and c_address and c_name:
                try:
                    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        idx = df_inventory[df_inventory["Item Name"] == c_name].index
                        if not idx.empty:
                            current_bal = df_inventory.loc[idx[0], "Current Balance"]
                            new_bal = max(0, current_bal - c_qty)
                            df_inventory.loc[idx[0], "Current Balance"] = new_bal
                            if "Total Sold" in df_inventory.columns:
                                df_inventory.loc[idx[0], "Total Sold"] += c_qty

                        df_inventory.to_excel(writer, sheet_name="Inventory Balance", index=False)
                        
                        order_notes = f"الاسم: {c_buyer} | الهاتف: {c_phone} | الإيميل: {c_email} | الدفع: {c_payment} | العنوان: {c_address}"
                        new_t = pd.DataFrame([{
                            "Item Name": c_name, "Transaction Type": "طلب عميل جديد",
                            "Quantity": c_qty, "Notes": order_notes,
                            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        }])
                        df_trans_updated = pd.concat([df_trans, new_t], ignore_index=True)
                        df_trans_updated.to_excel(writer, sheet_name="Transactions", index=False)
                        df_products.to_excel(writer, sheet_name="Products", index=False)

                    reorder_val = df_inventory.loc[idx[0], "Reorder Point"]
                    if new_bal <= int(str(reorder_val).replace("Reorder", "").strip() or 0):
                        send_email_alert(
                            f"⚠️ تنبيه عاجل: نقص مخزون الصنف {c_name}",
                            f"عزيزي المالك،\n\nالمنتج ({c_name}) وصل رصيده الحالي إلى ({new_bal})، وهو أقل من حد الطلب.\nيرجى التوريد فوراً!"
                        )

                    st.success("🎉 تم تسجيل طلبك بنجاح، وسيتم التواصل معك لتأكيد الشحن!")
                    st.balloons()
                except Exception as e:
                    st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى ملء البيانات الأساسية (الاسم، الهاتف، العنوان، المنتج).")

else:
    st.sidebar.markdown("---")
    admin_pass = st.sidebar.text_input("كلمة مرور الأدمن", type="password")
    
    if admin_pass == "lklklk900AR4":
        st.markdown("<h1 style='font-size: 38px; margin-bottom: 25px; color: #38bdf8;'>📊 لوحة التحكم الرئيسية (Admin Dashboard)</h1>", unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            prod_len = len(df_products)
            st.markdown(f"""
                <div class="metric-big-card">
                    <div style="font-size: 35px; margin-bottom: 10px;">📦</div>
                    <div class="metric-title">إجمالي المنتجات</div>
                    <div class="metric-value">{prod_len}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            trans_len = len(df_trans)
            st.markdown(f"""
                <div class="metric-big-card">
                    <div style="font-size: 35px; margin-bottom: 10px;">🔄</div>
                    <div class="metric-title">إجمالي العمليات والطلبات</div>
                    <div class="metric-value">{trans_len}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)])
            st.markdown(f"""
                <div class="metric-big-card">
                    <div style="font-size: 35px; margin-bottom: 10px;">🚨</div>
                    <div class="metric-title">منتجات تحتاج للطلب</div>
                    <div class="metric-value">{reorder_count}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><h3 style='margin-bottom: 15px; color: #38bdf8;'>📈 الرسوم البيانية والتحليلات المتقدمة</h3>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            if not df_inventory.empty and "Item Name" in df_inventory.columns and "Current Balance" in df_inventory.columns:
                fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", title="توزيع الرصيد الحالي للمنتجات", template="plotly_dark")
                # تم ضبط لون العناوين والمحاور لتكون بيضاء وواضحة جداً
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=14, family="Cairo"),
                    title_font=dict(color="#38bdf8", size=18, family="Cairo"),
                    xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
                    yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with chart_col2:
            if not df_inventory.empty and "Item Name" in df_inventory.columns and "Current Balance" in df_inventory.columns:
                fig_pie = px.pie(df_inventory, names="Item Name", values="Current Balance", title="حصة المخزون من الأصناف", template="plotly_dark")
                # تم ضبط لون العناوين والليجند لتكون واضحة
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=13, family="Cairo"),
                    title_font=dict(color="#38bdf8", size=18, family="Cairo"),
                    legend=dict(font=dict(color="white", size=12))
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.15); margin: 30px 0;'>", unsafe_allow_html=True)
        st.subheader("📦 تفاصيل المخزون الحالي")
        st.dataframe(df_inventory, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.15); margin: 30px 0;'>", unsafe_allow_html=True)
        st.subheader("لوحة متابعة طلبات العملاء والعمليات (Live Orders)")
        st.dataframe(df_trans, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.15); margin: 30px 0;'>", unsafe_allow_html=True)
        st.subheader("➕ إضافة صنف جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للملف")
            
            if p_submit and p_name:
                new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder}])
                df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df_inventory_updated.to_excel(writer, sheet_name="Inventory Balance", index=False)
                    df_trans.to_excel(writer, sheet_name="Transactions", index=False)
                    df_products.to_excel(writer, sheet_name="Products", index=False)
                st.success(f"✅ تم إضافة المنتج '{p_name}' بنجاح!")
                st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة مرور الأدمن الصحيحة في القائمة الجانبية لعرض لوحة التحكم.")

st.markdown("""
    <hr style='border-color: rgba(255,255,255,0.15); margin-top: 50px;'>
    <div style='text-align: center; color: #94a3b8; font-size: 14px; padding-bottom: 20px;'>
        SmartStock ERP Pro &copy; 2026 | جميع الحقوق محفوظة | تصميم UI/UX فائق الاحترافية
    </div>
""", unsafe_allow_html=True)
