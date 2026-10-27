import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


font_path = 'C:/Windows/Fonts/Nirmala.ttc' 
font_manager.fontManager.addfont(font_path)
font_manager.fontManager.addfont('C:/Windows/Fonts/seguiemj.ttf')   # Segoe UI Emoji
plt.rcParams['font.family'] = ['Nirmala UI', 'Segoe UI Emoji']

st.sidebar.title('Watsapp Chat Analyzer')


#upload file
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data=data)
    # st.dataframe(df)
    
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    #button to show analysis
    if st.sidebar.button("Show Analysis"):
        
        #stats area
        num_of_messages,num_of_words,media_count,num_of_url = helper.fetch_stats(df=df, selected_user=selected_user)
        st.title("Top Stastics")
        col1,col2,col3,col4 = st.columns(4)
        
       

        with col1:
            st.metric("Total Messages", num_of_messages)

        with col2:
            st.metric("Total Words", num_of_words)

        with col3:
            st.metric("Media Messages", media_count)

        with col4:
            st.metric("Total URLs", num_of_url)
                
        
        st.divider()
        
        #1.Monthly  Timeline
        st.header("Monthly Timeine")
        timeline = helper.monthly_timeline(selected_user,df)
        
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(timeline['time'], timeline['message'], color='#4C6EF5', linewidth=2.5)
        ax.fill_between(timeline['time'], timeline['message'], color='#4C6EF5', alpha=0.15)

        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlabel('Time', fontweight='bold')
        ax.set_ylabel('Messages', fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        st.pyplot(fig)
    
    
        # Daily Timeline
        st.divider()
        st.header('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#4C6EF5', linewidth=2.5)
        ax.fill_between(daily_timeline['only_date'], daily_timeline['message'], color='#4C6EF5', alpha=0.15)
        
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Messages', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        st.pyplot(fig)
        
        
        #activity map
        st.divider()
        st.header("Activity Map")
        monthly_map = helper.active_month_in_year(selected_user,df)
        day_map = helper.active_day_in_week(selected_user,df)
        col1,col2 = st.columns(2)
        
        with col1:
            colors = plt.cm.rainbow(np.linspace(0, 1, len(day_map)))
            fig,ax = plt.subplots()
            ax.bar(day_map.index,day_map.values, color = colors)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            
        with col2:
            colors = plt.cm.rainbow(np.linspace(0, 1, len(monthly_map)))
            fig,ax = plt.subplots()
            ax.bar(monthly_map.index,monthly_map.values, color = colors)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            
        
        #2. finding the busiest user in the group
        st.divider()
        if selected_user == 'Overall':
            st.header('Most Busy Users')
            col1,col2 = st.columns(2)
            x,new_df = helper.most_busy_users(df)
            
            with col1:
                fig, ax = plt.subplots(figsize = (6,5))
                colors = plt.cm.rainbow(np.linspace(0, 1, len(x)))
                ax.bar(x.index, x.values, color=colors)

                plt.xticks(rotation='vertical')
                ax.set_xlabel('Users', fontweight='bold', fontsize=20)
                ax.set_ylabel('Num_of_messages', fontweight='bold', fontsize=20)

                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
                
                
    st.divider()
    #3. wordcloud
    wc_img = helper.create_wordcloud(selected_user,df)
    st.header("Word Cloud")
    fig,ax = plt.subplots()
    ax.imshow(wc_img)
    st.pyplot(fig)
    
    
    #4. most common words
    top_words = helper.most_common_words(selected_user,df)
    st.divider()
    st.header("Top Common Words")
    fig, ax = plt.subplots()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(top_words)))
    ax.bar(top_words[0],top_words[1], color = colors)
    
    plt.xticks(rotation='vertical')
    ax.set_xlabel('words', fontweight='bold', fontsize=10)
    ax.set_ylabel('Frequency', fontweight='bold', fontsize=10)
    st.pyplot(fig)
    
    
    #5. Emojis Count
    st.divider()
    st.header("Emojis Used")
    col1,col2 = st.columns(2)
    emojis_df = helper.count_emoji(df)
   
    
    with col1:
       st.dataframe(emojis_df,height=207, use_container_width=True)
        
    with col2:
        top_emojis = emojis_df.head(10)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(top_emojis)))

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.pie(
            top_emojis['Count'],
            labels=top_emojis['Emoji'],
            colors=colors,
            autopct=lambda p: f'{p:.1f}%' if p > 3 else '',   # hides tiny labels
            startangle=90,
            pctdistance=0.8,
            textprops={'fontsize': 14}
        )
        ax.axis('equal')                      # keeps the pie circular
        fig.tight_layout()
        st.pyplot(fig)