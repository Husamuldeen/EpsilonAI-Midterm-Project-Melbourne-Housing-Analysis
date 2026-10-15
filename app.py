import streamlit as st#مكتبة الرسوميات
import pandas as pd#مكتبة الداتافريم والتنظيف

# 1. إعدادات الصفحة الرئيسية
st.set_page_config(page_title="Melbourne Housing Dashboard", page_icon="🏘️", layout="wide")#عنوان مال الصفحة
st.title("🏘️ لوحة تحكم السوق العقاري في ملبورن")# النص الاول
st.markdown("مرحباً بك! يعرض هذا التطبيق نتائج التحليل الاستكشافي لبيانات أسعار العقارات. يرجى التنقل بين الصفحات من القائمة الجانبية اليسرى.")# الشرح

# 2. تحميل وتنظيف البيانات (باستخدام التخزين المؤقت لتسريع الموقع)
@st.cache_data#حفظ البيانات بالكاش مموري بدال الااستدعاء المباشر للداتا
def load_data():
    df = pd.read_csv('MELBOURNE_HOUSE_PRICES_LESS.csv') #ننقل البيانات بمتغير
    df_clean = df.drop_duplicates() #نحذف المكرر
    df_clean = df_clean.dropna(subset=['Price', 'Regionname'])# اذا كان السعر، المنطقة غير موجود نحذف الصف
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], dayfirst=True)#تحويل التاريخ لصيغة التاريخ
    return df_clean.reset_index(drop=True)#يعيد ترتيب العنوان بسبب الحذف

if 'data' not in st.session_state:# التحقق مما إذا كانت البيانات غير محفوظة في الجلسة
    st.session_state['data'] = load_data()# استدعاء الدالة

st.success("تم تحميل البيانات وتنظيفها بنجاح! جاهزون للتحليل.")