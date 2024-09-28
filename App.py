import streamlit as st
import processor
import functions
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
upload_file = st.sidebar.file_uploader("Choose file")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = processor.process(data)
    unique_users = df['User'].unique().tolist()

    if 'Group Notification' in unique_users:
        unique_users.remove('Group Notification')
    unique_users.sort()
    unique_users.insert(0, 'Overall')
    
    selected_user = st.sidebar.selectbox('Show Analysis for', unique_users)

    if st.sidebar.button('Analyze'):
        msgs, words, media, links = functions.fetch_details(selected_user, df)

        st.title("Overall Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Message')
            st.subheader(msgs)
        with col2:
            st.header('Total Words')
            st.subheader(words)
        with col3:
            st.header('Media Shared')
            st.subheader(media)
        with col4:
            st.header('Links Shared')
            st.subheader(links)

        timeline = functions.time_line(selected_user, df)
        print(timeline)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'], color='red')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        dateline = functions.date_line(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(dateline['Date'], dateline['Message'], color='#64137b')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)
        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list, active_time_df, time_list, time_msg_list = functions.activity(selected_user, df)
        print(active_month_df)
        print(month_list)
        print(month_msg_list)
        print(active_day_df)
        print(day_list)
        print(day_msg_list)
        print(active_time_df)
        print(time_list)
        print(time_msg_list)

        with col1:
            st.header('Most Active Months')
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'], active_month_df['Message'])
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green', label='Highest')
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header('Most Active Days')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['Message'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label='Highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        st.title('Most Active Time')
        if 'hour' in active_time_df.columns:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            bars = ax.bar(active_time_df['hour'], active_time_df['Message'], color='blue')

            time_labels = [f'{hour} AM' for hour in range(1, 12)] + ['12 AM'] + [f'{hour} PM' for hour in range(1, 12)] + ['12 PM']
            ax.set_xticks(range(1, 25)) 
            ax.set_xticklabels(time_labels, rotation=90)

            ax.set_xlim(0.5, 24.5) 

            st.pyplot(fig)

        if selected_user == 'Overall':
            st.title("Most Active Users")
            x, percent = functions.most_chat(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x, color='#3ef3e1')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        st.title("Most Used Emojis")
        user_emojis = functions.most_used_emoji(df)
        for user, (emoji, count) in user_emojis.items():
            st.write(f"{user}: {emoji} (Used {count} times)")
        
        df_wc = functions.wordcloud(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
