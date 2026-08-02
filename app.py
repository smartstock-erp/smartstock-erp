import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# إعدادات الصفحة
st.set_page_config(page_title="SmartStock", page_icon="🛍️", layout="wide")

# تصميم الديزاين المودرن الفخم (Modern UI & Animations)
st.markdown("""
    <style>
    /* خلفية عامة مريحة للعين وبسيطة */
    .main {
        background-color: #f1f5f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* العناوين بستايل راقي وجذاب */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* كروت النماذج بشكل عصري مع تأثير Hover ناعم */
    div.stForm {
        background: #ffffff;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease;
    }
    
    div.stForm:hover {
        transform: translateY(-2px);
    }
    
    /* أزرار عصرية بتدرجات ألوان فخمة */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
        transform: scale(1.01);
    }
    
    /* تنسيق الكروت الإحصائية (Metrics) */
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
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

# القائمة الجانبية بالاسم المطلوب
st.sidebar.title("🔐 لوحة التحكم")
app_mode = st.sidebar.selectbox("اختر الشاشة", ["SmartStock", "⚙️ لوحة التحكم"])

if app_mode == "SmartStock":
    st.title("🛍️ SmartStock")
    st.markdown("مرحباً بك! تصفح المنتجات وأتمم طلبك بكل راحة واحترافية.")
    st.markdown("---")
    
    st.subheader("📋 قائمة المنتجات المتاحة للطلب")
    if not df_inventory.empty:
        st.dataframe(df_inventory[["Item Name", "Current Balance"]], use_container_width=True)
    
    st.markdown("---")
    st.subheader("📝 املأ بياناتك")
    
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
        st.title("📊 لوحة تحكم التخطيط والتنبؤ الذكي (Admin Dashboard)")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📦 إجمالي المنتجات", value=len(df_products))
        with col2:
            st.metric(label="🔄 إجمالي العمليات والطلبات", value=len(df_trans))
        with col3:
            reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)])
            st.metric(label="🚨 منتجات تحتاج للطلب", value=reorder_count)

        st.subheader("🔔 لوحة متابعة طلبات العملاء والعمليات (Live Orders)")
        st.dataframe(df_trans, use_container_width=True)

        st.markdown("---")
        st.subheader("📦 تفاصيل المخزون الحالي")
        st.dataframe(df_inventory, use_container_width=True)

        st.markdown("---")
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
