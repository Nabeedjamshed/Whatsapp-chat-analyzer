import re
import pandas as pd
import emoji

def process(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'
    messages = re.split(pattern, data)[1:] #to convert data into meaningfull list
    dates = re.findall(pattern, data)
    
    date = []
    time = []
    for i in dates:
        date.append(i.split(", ")[0])
        time.append(i.split(", ")[1].split(' - ')[0])  

    df = pd.DataFrame({'User_msg': messages, 'Date': date, 'Time': time})
    user = []
    msg = []
    emojis = []  
    for i in df['User_msg']:
        user_and_msg = re.split(r"([\w\W]+?):\s", i)
        if len(user_and_msg) > 2:
            user.append(user_and_msg[1])
            msg.append(user_and_msg[2])
        else:
            user.append("Group Notification")
            msg.append(user_and_msg[0] if len(user_and_msg) > 0 else "")
        msg_emojis = ' '.join(c for c in msg if c in emoji.EMOJI_DATA)
        emojis.append(msg_emojis)
    df['User'] = user
    df['Message'] = msg
    df['Emojis'] = emojis
    df.drop(columns=['User_msg'], inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day_name()

    def convert_time(t):
        for fmt in ('%I:%M %p', '%H:%M'):
            try:
                return pd.to_datetime(t, format=fmt).time()
            except ValueError:
                continue
        return None 

    df['Time'] = df['Time'].apply(convert_time)

    return df
print(process('12/2/23, 7:06 PM - NABEED JAMSHED: Assalam u alaikum bhai'))