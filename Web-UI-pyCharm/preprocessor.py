import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(am|pm)\s-\s'
    messages = re.split(pattern, data)[1:]
    pat = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    dates = (re.findall(pat, data))*2

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message-date type
    df['message_date'] = pd.to_datetime(df['message_date'])
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df.drop_duplicates(keep=False, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['perid'] = period

    return df






