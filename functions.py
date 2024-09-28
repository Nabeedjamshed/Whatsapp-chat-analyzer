from urlextract import URLExtract
from wordcloud import WordCloud
import re
import pandas as pd
import emoji 
from collections import Counter

extract = URLExtract()

def fetch_details(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    msgs = df.shape[0]
    
    words = []
    for i in df['Message']:
        words.extend(re.findall(r'\w+', i))

    media = df[df['Message'] == '<Media omitted>\n'].shape[0]

    links = []
    for j in df['Message']:
        links.extend(extract.find_urls(j))

    return msgs, len(words), media, len(links)

def time_line(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline = df.groupby(['year', 'month'])['Message'].count().reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def date_line(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    dateline = df.groupby('Date')['Message'].count().reset_index()
    return dateline

def activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    active_month_df = df.groupby('month')['Message'].count().reset_index()
    month_list = active_month_df['month'].tolist()
    month_msg_list = active_month_df['Message'].tolist()

    active_day_df = df.groupby('day')['Message'].count().reset_index()
    day_list = active_day_df['day'].tolist()
    day_msg_list = active_day_df['Message'].tolist()

    if 'Time' in df.columns:
        df['hour'] = df['Time'].apply(lambda x: x.hour if x is not None else None)
        active_time_df = df.groupby('hour').size().reset_index(name='Message')
        active_time_df['hour'] = active_time_df['hour'].apply(lambda x: f'{x:02d}:00' if x is not None else 'Unknown')
    else:
        active_time_df = pd.DataFrame(columns=['hour', 'Message'])

    time_list = active_time_df['hour'].tolist()
    time_msg_list = active_time_df['Message'].tolist()

    return active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list, active_time_df, time_list, time_msg_list

def most_chat(df):
    x = df['User'].value_counts().head()
    percent = round((df['User'].value_counts() / df['User'].shape[0]) * 100, 2)
    return x, percent

def wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=' '))
    return df_wc

def most_used_emoji(df):
    user_emojis = {}
    for user in df['User'].unique():
        user_df = df[df['User'] == user]

        all_emojis = ' '.join(' '.join(c for c in msg if c in emoji.EMOJI_DATA) for msg in user_df['Message'])

        emoji_counts = Counter(all_emojis.split())

        if emoji_counts:
            most_common_emoji = emoji_counts.most_common(1)[0]
            user_emojis[user] = most_common_emoji
        else:
            user_emojis[user] = ("No emojis", 0)
    
    return user_emojis
