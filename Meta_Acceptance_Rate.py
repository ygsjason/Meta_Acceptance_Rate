# Import your libraries
import pandas as pd
# import datetime as dt

# Sort the df in ascending order and Convert date column to date only
df1 = fb_friend_requests.sort_values(['user_id_sender', 'date']).drop_duplicates()
df1['dt'] = df1.date.dt.date
df1

# Groupby id_sender, id_receiver to drop users who didn't receive "accepted", 
#df2 = df1[(df1.action == 'sent') | (df1.action == 'accepted')]
df1_1 = df1.groupby(['user_id_sender', 'user_id_receiver'])['action'].count().reset_index(name = 'n_action').query('n_action == 1')

df1_2 = df1[~df1.user_id_sender.isin(df1_1.user_id_sender)]

# Count n of acpt by date (action contains both sent and accepted for an individual sender)
df2 = df1_2.query('action == "sent"').groupby('dt')['user_id_sender'].count().reset_index(name = 'n_acpt')

# Count n of total actions == sent by date
df3 = df1.query('action == "sent"').groupby('dt')['action'].count().reset_index(name = 'n_sent')

# Join df2 and df3 by dt, then calculate acceptance rate
df4 = pd.merge(df3, df2, how = 'outer', on = 'dt').assign(acpt_rate =  lambda df: df.n_acpt / df.n_sent)
