import streamlit as st#مكتبة الرسوميات
import matplotlib.pyplot as plt#الرسوم البيانية

st.set_page_config(page_title="التحليل الجغرافي والزمني", page_icon="🗺️", layout="wide")
st.title("🗺️ التحليل الجغرافي والزمني لحركة السوق")

df_cleaned = st.session_state['data']

# فلتر المناطق خاص بهذه الصفحة
st.sidebar.header("خيارات التصفية الجغرافية")
regions = df_cleaned['Regionname'].unique() # جلب أسماء المناطق
selected_regions = st.sidebar.multiselect("اختر المنطقة", regions, default=regions)

df_filtered = df_cleaned[df_cleaned['Regionname'].isin(selected_regions)]

if df_filtered.empty:
    st.warning("يرجى اختيار منطقة واحدة على الأقل.")
else:
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("توزيع الأسعار حسب المنطقة")
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        regions_list = df_filtered['Regionname'].dropna().unique() # جلب أسماء المناطق
        price_data = [df_filtered[df_filtered['Regionname'] == r]['Price'] / 1000000 for r in regions_list]
        
        ax3.boxplot(price_data, tick_labels=regions_list, vert=False, patch_artist=True)
        ax3.set_xlabel('Price (Millions AUD)') #ليبل التحليل
        st.pyplot(fig3)#عرض التحليل بالموقع

    with col4:
        st.subheader("السعر مقابل المسافة والغرف")
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        scatter = ax4.scatter(df_filtered['Distance'], df_filtered['Price'] / 1000000,  #مخطط الفقاعات
                              c=df_filtered['Rooms'], cmap='viridis', alpha=0.5)
        ax4.set_xlabel('Distance from CBD (km)')
        ax4.set_ylabel('Price (Millions AUD)')
        fig4.colorbar(scatter, ax=ax4, label='Number of Rooms')
        st.pyplot(fig4)

    st.divider()
    
    st.subheader("📍 تمركز المبيعات: المسافة مقابل عدد الغرف")
    df_bubble = df_filtered.copy()
    df_bubble['Distance_Group'] = df_bubble['Distance'].round()
    sales_counts = df_bubble.groupby(['Distance_Group', 'Rooms']).size().reset_index(name='Sales_Count')
    
    fig6, ax6 = plt.subplots(figsize=(12, 5))
    bubble_plot = ax6.scatter(sales_counts['Distance_Group'], sales_counts['Rooms'], 
                          s=sales_counts['Sales_Count'] * 5, 
                          c=sales_counts['Sales_Count'], cmap='Reds', alpha=0.7, edgecolors='black')
    ax6.set_xlabel('Distance from CBD (km)')
    ax6.set_ylabel('Number of Rooms')
    fig6.colorbar(bubble_plot, ax=ax6, label='Number of Sales (Count)')
    st.pyplot(fig6)

    st.divider()

    st.subheader("📅 متوسط أسعار العقارات بمرور الزمن")
    monthly_price = df_filtered.groupby(df_filtered['Date'].dt.to_period('M'))['Price'].mean() / 1000000
    
    fig5, ax5 = plt.subplots(figsize=(15, 4))
    ax5.plot(monthly_price.index.astype(str), monthly_price.values, marker='o', linestyle='-', color='coral')
    ax5.set_xlabel('Date (Year-Month)')
    ax5.set_ylabel('Average Price (Millions AUD)')
    plt.xticks(rotation=45)
    st.pyplot(fig5)