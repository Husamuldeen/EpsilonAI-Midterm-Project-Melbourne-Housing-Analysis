import streamlit as st#مكتبة الرسوميات

st.set_page_config(page_title="الملخص العام", page_icon="📊", layout="wide")
st.title("📊 ملخص السوق العقاري وإحصائيات عامة")

# استدعاء البيانات من الجلسة
df_cleaned = st.session_state['data'] # جلب البيانات المنظفة من الجلسة

col1, col2, col3, col4 = st.columns(4)#تحديد الاعمدة
col1.metric("إجمالي العقارات المعروضة", f"{len(df_cleaned):,}")#اضافة صف عنوان العمود وصف المعلومة
col2.metric("متوسط السعر", f"${df_cleaned['Price'].mean():,.0f}")
col3.metric("أعلى سعر", f"${df_cleaned['Price'].max():,.0f}")
col4.metric("أقل سعر", f"${df_cleaned['Price'].min():,.0f}")

st.divider()
st.header("📋 استعراض عينة من البيانات")
st.dataframe(df_cleaned.head(100)) #عرض اول 100 نتيجة