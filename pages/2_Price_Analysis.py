import streamlit as st#مكتبة الرسوميات
import matplotlib.pyplot as plt#الرسوم البيانية

# 1. إعدادات الصفحة
st.set_page_config(page_title="تحليل الأسعار والأنواع", page_icon="📈", layout="wide")
st.title("📈 تحليل الأسعار وأنواع العقارات")

df_cleaned = st.session_state['data']

# فلتر نوع العقار خاص بهذه الصفحة
st.sidebar.header("خيارات التصفية")
types = df_cleaned['Type'].unique()# استخراج أنواع العقارات بدون تكرار

selected_types = st.sidebar.multiselect("اختر نوع العقار", types, default=types) # إنشاء قائمة اختيار جانبية للمستخدم

df_filtered = df_cleaned[df_cleaned['Type'].isin(selected_types)]# تصفية البيانات بحيث تطابق اختيار المستخدم فقط

if df_filtered.empty:# إذا كانت نتيجة التصفية فارغة
    st.warning("يرجى اختيار نوع عقار واحد على الأقل.")
else:
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("توزيع أسعار العقارات")
        fig1, ax1 = plt.subplots(figsize=(8, 5)) # إنشاء لوحة رسم بأبعاد 8x5
        ax1.hist(df_filtered['Price'] / 1000000, bins=50, color='skyblue', edgecolor='black')#الهستوغرام البياني )   رسم مدرج تكراري للأسعار (مقسمة على مليون لتسهيل القراءة) بـ 50 
        ax1.set_xlabel('Price (Millions AUD)')
        ax1.set_ylabel('Frequency')
        st.pyplot(fig1) # أمر Streamlit لعرض الرسمة في الموقع

    with right_column:
        st.subheader("حجم المبيعات حسب نوع العقار")
        type_counts = df_filtered['Type'].value_counts() # حساب عدد المبيعات لكل نوع عقار
        fig2, ax2 = plt.subplots(figsize=(8, 5)) 
        ax2.bar(type_counts.index, type_counts.values, color=['#ff9999', '#66b3ff', '#99ff99'], edgecolor='black') # رسم المخطط الشريطي، المحور الأفقي للأنواع (index) والعمودي للعدد 
        ax2.set_xlabel('Property Type (h=House, u=Unit, t=Townhouse)')
        ax2.set_ylabel('Count')
        st.pyplot(fig2)