import re
from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]
        
    #1. Fetch no of msg
    num_of_messages = df.shape[0]
    
    #2. fetch no of words
    words_list = []
    for msg in df['message']:
        words_list.extend(msg.split())
        
    #3. Media count
    count = 0
    pattern = r'<Media omitted>\n'
    for msg in df['message']:
        if re.search(pattern, msg):
            count +=1
    #4. fetch links
    links = []
    for msg in df['message']:
       found = extractor.find_urls(msg)
       if found :
           links.extend(found)
    
    #3. Return            
    return num_of_messages,len(words_list),count, len(links)
    
    
    

#most busiest user
def most_busy_users(df):
    #1. top 5 users
    x = df[df['user'] != 'group_notification']['user'].value_counts().head(5)
  
    
    #2. dataframe of users with percentage usage
    y = df[df['user'] != 'group_notification']['user'].value_counts()
    name = y.index
    counts = y.values
    message = counts
    percentage = [round(val/sum(counts) * 100,2) for val in counts]
    
    new_df = pd.DataFrame({
        'Name' : name,
        'Messages' : message,
        'Percentage': [str(p) + '%' for p in percentage]
    })
    
    return x , new_df
        


def create_wordcloud(selected_user, df):

    with open('Hinglish_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = set(line.strip() for line in f if line.strip())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y = []

        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stopwords)

    # Check whether the DataFrame is empty
    if temp.empty:
        return None

    text = temp['message'].str.cat(sep=" ").strip()

    # Check whether any text remains after stopword removal
    if not text:
        return None

    wc = WordCloud(
        width=500,
        height=500,
        background_color='white',
        font_path='C:/Windows/Fonts/Nirmala.ttc',
        regexp=r"[\w\u0900-\u097F']+",
        collocations=False
    )

    df_wc = wc.generate(text)

    return df_wc



def most_common_words(selected_user,df):
    #remove group_noti and media count
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    #open stopwords
    # with open('Hinglish_stopwords.txt','r') as f:
    #     stop_words = f.read().splitlines()
    
    with open('Hinglish_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = set(line.strip() for line in f if line.strip())
    
    # do check by excluding hinglish stopwords
    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    
   
    new_df = pd.DataFrame(Counter(words).most_common(50))
    # new_df = new_df.rename(columns={
    #     0 : 'Messages',
    #     1 : 'Frequency'
    # })
    return new_df.head(20)
  
def count_emoji(df):
    emojis = []
    for msg in df['message'].dropna():
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['Emoji', 'Count']
    )
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    timeline =df.groupby(['year','months_num','month']).count()['message'].reset_index()
    
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def active_day_in_week(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return  df['day_name'].value_counts()

def active_month_in_year(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()