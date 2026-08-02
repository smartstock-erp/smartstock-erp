import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="SmartStock ERP Pro", page_icon="📊", layout="wide")

file_path = "SmartStock ERP Pro.xlsx"

# --- دالة إرسال الإيميلات ---
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

# --- تحميل البيانات ---
def load_data():
    if not os.path.exists(file_path):
        st.error(f"⚠️ ملف الإكسيل غير موجود: {file_path}")
        st.stop()
    df_products = pd.read_excel(file_path, sheet_name="Products")
    df_trans = pd.read_excel(file_path, sheet_name="Transactions")
    df_inventory = pd.read_excel(file_path, sheet_name="Inventory Balance")
    return df_products, df_trans, df_inventory

df_products, df_trans, df_inventory = load_data()

# --- واجهة النظام والصلاحيات ---
st.sidebar.title("🔐 لوحة التحكم وصلاحيات النظام")
app_mode = st.sidebar.selectbox("اختر الشاشة", ["🛒 متجر العرض والطلب (للعملاء)", "⚙️ لوحة تحكم المالك (Admin)"])

if app_mode == "🛒 متجر العرض والطلب (للعملاء)":
    st.title("🛍️ متجر SmartStock للمنتجات")
    st.markdown("---")
    st.subheader("📋 قائمة المنتجات المتاحة للطلب")
    
    if not df_inventory.empty:
        st.dataframe(df_inventory[["Item Name", "Current Balance"]], use_container_width=True)
    
    st.markdown("---")
    st.subheader("📝 نموذج طلب شراء جديد")
    with st.form("customer_order"):
        c_name = st.selectbox("اختر المنتج المطلوب", df_inventory["Item Name"].tolist() if "Item Name" in df_inventory.columns else [])
        c_qty = st.number_input("الكمية المطلوبة", min_value=1, value=1)
        c_buyer = st.text_input("اسمك الكريم / رقم الهاتـف")
        
        submit_order = st.form_submit_button("إرسال طلب الشراء")
        if submit_order:
            if c_buyer and c_name:
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
                        
                        new_t = pd.DataFrame([{
                            "Item Name": c_name, "Transaction Type": "بيع (خصم عبر المتجر)",
                            "Quantity": c_qty, "Notes": f"عميل: {c_buyer}",
                            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        }])
                        df_trans_updated = pd.concat([df_trans, new_t], ignore_index=True)
                        df_trans_updated.to_excel(writer, sheet_name="Transactions", index=False)
                        df_products.to_excel(writer, sheet_name="Products", index=False)

                    # فحص حد الطلب لإرسال إيميل تنبيه لو المخزون قل
                    reorder_val = df_inventory.loc[idx[0], "Reorder Point"]
                    if new_bal <= int(str(reorder_val).replace("Reorder", "").strip() or 0):
                        send_email_alert(
                            f"⚠️ تنبيه عاجل: نقص مخزون الصنف {c_name}",
                            f"عزيزي المالك،\n\nالمنتج ({c_name}) وصل رصيده الحالي إلى ({new_bal})، وهو أقل من حد الطلب.\nيرجى التوريد فوراً!"
                        )

                    st.success("🎉 تم تسجيل طلبك بنجاح وسيتم التواصل معك!")
                    st.balloons()
                except Exception as e:
                    st.error(f"خطأ أثناء تسجيل الطلب: {e}")
            else:
                st.warning("⚠️ يرجى كتابة اسمك وإدخال البيانات كاملة.")

else:
    # شاشة الأدمن السرية
    st.sidebar.markdown("---")
    admin_pass = st.sidebar.text_input("كلمة مرور الأدمن", type="password")
    
    if admin_pass == "1234":  # تقدر تغير الباسورد براحتك هنا
        st.title("📊 لوحة تحكم التخطيط والتنبؤ الذكي (Admin Dashboard)")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📦 إجمالي المنتجات", value=len(df_products))
        with col2:
            st.metric(label="🔄 إجمالي العمليات", value=len(df_trans))
        with col3:
            reorder_count = len(df_inventory[df_inventory["Reorder Point"].astype(str).str.contains("Reorder|🚨", na=False)])
            st.metric(label="🚨 منتجات تحتاج للطلب", value=reorder_count)

        st.subheader("📋 تفاصيل المخزون الكاملة")
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
