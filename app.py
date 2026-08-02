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
    page_title="MedStock ERP Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة طبية متطورة مع تدرجات الأخضر الطبي والأزرق الهادئ ومحاذاة لليمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 20%, #061a18 0%, #0d2824 40%, #0f172a 100%);
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        color: #ffffff;
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, h5, h6, label, .stMarkdown p {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    /* الشريط الجانبي الطبي الفاخر */
    [data-testid="stSidebar"] {
        background: rgba(8, 26, 24, 0.95) !important;
        backdrop-filter: blur(25px);
        border-left: 1px solid rgba(52, 211, 153, 0.2);
        direction: rtl;
    }

    /* كروت الجلاس مورفيزم الطبية */
    .glass-card {
        background: linear-gradient(135deg, rgba(16, 42, 38, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(52, 211, 153, 0.25);
        border-radius: 28px;
        padding: 35px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        direction: rtl;
        text-align: right;
    }

    /* كروت الإحصائيات الطبية */
    .metric-big-card {
        background: linear-gradient(135deg, rgba(16, 42, 38, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 26px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        direction: rtl;
    }

    .metric-title {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #34d399 !important;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: 52px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #ffffff 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* كروت المنتجات الطبية */
    .product-store-card {
        background: rgba(16, 42, 38, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        padding: 26px;
        text-align: center;
        transition: all 0.35s ease;
        height: 100%;
        direction: rtl;
    }

    .product-store-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: #34d399;
        background: rgba(16, 42, 38, 0.8);
        box-shadow: 0 20px 40px rgba(52, 211, 153, 0.2);
    }

    .badge-stock {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 800;
        margin-top: 14px;
    }
    .badge-good { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.5); }
    .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.5); }

    /* حقول الإدخال */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(11, 27, 25, 0.85) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid rgba(52, 211, 153, 0.35) !important;
        font-weight: 600 !important;
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stForm"] label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: #34d399 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    /* الأزرار الطبية التفاعلية */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 0.85rem 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.4) !important;
        width: 100% !important;
        transition: all 0.35s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
        box-shadow: 0 15px 35px rgba(52, 211, 153, 0.5) !important;
        transform: translateY(-2px);
    }

    [data-testid="stDataFrame"] {
        direction: rtl;
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

with st.sidebar:
    st.markdown("""
        <div style="text-align: right; padding: 15px 0;">
            <h1 style="font-size: 26px; color: #34d399; margin-bottom: 0;">🩺 رعاية ميدكل</h1>
            <p style="font-size: 13px; color: #94a3b8; margin-top: 5px;">إدارة المستلزمات الطبية والأدوية</p>
        </div>
        <hr style="border-color: rgba(52,211,153,0.2);">
    """, unsafe_allow_html=True)
    
    current_time_str = datetime.now().strftime("%Y-%m-%d | %H:%M")
    st.markdown(f"<div style='text-align: center; font-size: 13px; color: #34d399; background: rgba(52,211,153,0.1); padding: 8px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(52,211,153,0.2);'>🕒 {current_time_str}</div>", unsafe_allow_html=True)
    
    app_mode = st.selectbox("اختر واجهة الاستخدام", ["متجر المستلزمات الطبية", "لوحة التحكم الرئيسية"])

if app_mode == "متجر المستلزمات الطبية":
    st.markdown("""
        <div class="glass-card" style="text-align: right; padding: 45px; margin-bottom: 35px;">
            <h1 style="font-size: 38px; color: #34d399; margin-bottom: 12px;">🩺 متجر المستلزمات الطبية والدوائية</h1>
            <p style="font-size: 18px; color: #cbd5e1;">تُشرّفنا زيارتُك، تصفّح المنتجات وأتمم طلبك بكل سهولة.</p>
        </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 ابحث عن مستلزم طبي أو دواء...", "")
    
    st.markdown("<h3 style='margin-top: 35px; margin-bottom: 25px; color: #34d399; text-align: right;'>المستلزمات الطبية المتاحة للطلب الفوري</h3>", unsafe_allow_html=True)
    
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
                        <div style="font-size: 45px; margin-bottom: 12px;">💊</div>
                        <h4 style="color: #ffffff; font-size: 19px; margin-bottom: 12px;">{item_name}</h4>
                        {stock_badge}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top: 25px; margin-bottom: 25px; color: #34d399; text-align: right;'>اطلب من هنا</h3>", unsafe_allow_html=True)
    
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
                            f"⚠️ تنبيه عاجل: نقص مخزون الصنف الطبي {c_name}",
                            f"عزيزي المالك،\n\nالمنتج الطبي ({c_name}) وصل رصيده الحالي إلى ({new_bal})، وهو أقل من حد الطلب.\nيرجى التوريد فوراً!"
                        )

                    st.success("🎉 تم تسجيل طلبك الطبي بنجاح، وسيتم التواصل معك للتسليم الشحن!")
                    st.balloons()
                except Exception as e:
                    st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى ملء البيانات الأساسية (الاسم، الهاتف، العنوان، المنتج).")

else:
    st.sidebar.markdown("---")
    admin_pass = st.sidebar.text_input("كلمة مرور الأدمن", type="password")
    
    if admin_pass == "lklklk900AR4":
        st.markdown("<h1 style='font-size: 38px; margin-bottom: 25px; color: #34d399; text-align: right;'>لوحة التحكم الإدارية الطبية</h1>", unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            prod_len = len(df_products)
            st.markdown(f"""
                <div class="metric-big-card">
                    <div class="metric-title">إجمالي المنتجات الطبية</div>
                    <div class="metric-value">{prod_len}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            trans_len = len(df_trans)
            st.markdown(f"""
                <div class="metric-big-card">
                    <div class="metric-title">إجمالي العمليات والطلبات</div>
                    <div class="metric-value">{trans_len}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)])
            st.markdown(f"""
                <div class="metric-big-card">
                    <div class="metric-title">منتجات تحتاج للتوريد</div>
                    <div class="metric-value">{reorder_count}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><h3 style='margin-bottom: 20px; color: #34d399; text-align: right;'>التحليلات والرسوم البيانية للمخزون</h3>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            if not df_inventory.empty and "Item Name" in df_inventory.columns and "Current Balance" in df_inventory.columns:
                fig_bar = px.bar(df_inventory, x="Item Name", y="Current Balance", title="توزيع رصيد المنتجات الطبية", template="plotly_dark")
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=12, family="Cairo"),
                    title_font=dict(color="#34d399", size=18, family="Cairo"),
                    xaxis=dict(tickfont=dict(color="white", size=11), tickangle=-45),
                    yaxis=dict(tickfont=dict(color="white"))
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with chart_col2:
            if not df_inventory.empty and "Item Name" in df_inventory.columns and "Current Balance" in df_inventory.columns:
                fig_pie = px.pie(df_inventory, names="Item Name", values="Current Balance", title="نسب توزيع المخزون الطبي", template="plotly_dark")
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=13, family="Cairo"),
                    title_font=dict(color="#34d399", size=18, family="Cairo"),
                    legend=dict(font=dict(color="white", size=12))
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(52,211,153,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("تفاصيل المخزون الطبي الحالي")
        st.dataframe(df_inventory, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(52,211,153,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("متابعة طلبات العملاء والعيادات الطبية")
        st.dataframe(df_trans, use_container_width=True)

        st.markdown("<hr style='border-color: rgba(52,211,153,0.2); margin: 35px 0;'>", unsafe_allow_html=True)
        st.subheader("إضافة صنف طبى جديد للمخزن")
        with st.form("add_product"):
            p_name = st.text_input("اسم المنتج أو الدواء الجديد")
            p_bal = st.number_input("الرصيد الابتدائي", min_value=0, value=10)
            p_reorder = st.number_input("حد الطلب (Reorder Point)", min_value=0, value=5)
            p_submit = st.form_submit_button("إضافة الصنف للمخزن")
            
            if p_submit and p_name:
                new_row = pd.DataFrame([{"Item Name": p_name, "Current Balance": p_bal, "Reorder Point": p_reorder}])
                df_inventory_updated = pd.concat([df_inventory, new_row], ignore_index=True)
                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df_inventory_updated.to_excel(writer, sheet_name="Inventory Balance", index=False)
                    df_trans.to_excel(writer, sheet_name="Transactions", index=False)
                    df_products.to_excel(writer, sheet_name="Products", index=False)
                st.success(f"✅ تم إضافة الصنف الطبي '{p_name}' بنجاح!")
                st.rerun()
    else:
        st.warning("🔒 من فضلك ادخل كلمة مرور الأدمن الصحيحة في القائمة الجانبية لعرض لوحة التحكم.")

st.markdown("""
    <hr style='border-color: rgba(52,211,153,0.2); margin-top: 60px;'>
    <div style='text-align: center; color: #94a3b8; font-size: 14px; padding-bottom: 25px;'>
        رعاية ميدكل لنظم الإدارة الطبية &copy; 2026 | جميع الحقوق محفوظة
    </div>
""", unsafe_allow_html=True)
