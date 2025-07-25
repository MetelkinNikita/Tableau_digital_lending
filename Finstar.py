import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt


fake = Faker()
np.random.seed(42)

n_users = 70000
users = np.arange(1, n_users + 1)

status_flow = ['started', 'submitted', 'verified', 'approved', 'funded']
alt_statuses = ['rejected', 'expired', 'cancelled']
transition_probs = {
    'started': 0.5,
    'submitted': 0.85,
    'verified': 0.6,
    'approved': 0.85,
    'funded': 0.5
}

events = []
for user_id in users:
    country = np.random.choice(['India', 'Vietnam', 'Mexico'], p=[0.54, 0.33, 0.13])
    channel = np.random.choice(['Facebook Ads', 'Google Ads', 'Organic', 'Referral'], p=[0.12, 0.33, 0.4, 0.15])

    if channel == 'Organic':
        n_sessions = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.05, 0.05])
        transition_probs = {
            'started': 0.8,
            'submitted': 0.85,
            'verified': 0.4,
            'approved': 0.85,
            'funded': 0.4
        }
    if channel == 'Facebook Ads':
        n_sessions = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        transition_probs = {
            'started': 0.5,
            'submitted': 0.85,
            'verified': 0.3,
            'approved': 0.85,
            'funded': 0.3
        }
    if channel == 'Google Ads':
        n_sessions = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.2, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1])
        transition_probs = {
            'started': 0.6,
            'submitted': 0.85,
            'verified': 0.3,
            'approved': 0.85,
            'funded': 0.4
        }
    if channel == 'Referral':
        n_sessions = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1])
        transition_probs = {
            'started': 0.8,
            'submitted': 0.85,
            'verified': 0.5,
            'approved': 0.85,
            'funded': 0.5
        }

    first_day = np.clip(np.random.normal(90, 40), a_min=0, a_max=180)
    #start = first_day + 1 if first_day + 1 < 180 else first_day
    session_days = np.random.randint(first_day + 1, first_day + 180, size=n_sessions - 1)
    session_days = np.sort(np.append(session_days, first_day))


    for session_num, session_day in enumerate(session_days, start=1):
        session_id = f"{user_id}_{session_num}"  # формируем session_id: userID_номерСессии
        base_time = pd.Timestamp('2024-01-01') + pd.to_timedelta(session_day, unit='D')
        device_id = fake.uuid4()

        events.append((user_id, session_id, 'visited', base_time, channel, country, device_id))

        current_time = base_time
        passed_flow = True
        for i, stage in enumerate(status_flow):
            prev_stage = status_flow[i - 1] if i > 0 else 'visited'
            if np.random.rand() < transition_probs[stage]:
                if stage == 'started':
                    current_time += pd.to_timedelta(np.random.lognormal(mean=1.7, sigma=0.4), unit='m')
                elif stage == 'submitted':
                    current_time += pd.to_timedelta(np.random.lognormal(mean=1.4, sigma=0.3), unit='m')
                elif stage == 'verified':
                    current_time += pd.to_timedelta(np.random.lognormal(mean=2, sigma=0.5), unit='m')
                elif stage == 'approved':
                    current_time += pd.to_timedelta(np.random.lognormal(mean=1, sigma=0.2), unit='m')
                else:
                    current_time += pd.to_timedelta(np.random.lognormal(mean=2.3, sigma=0.4), unit='m')
                events.append((user_id, session_id, stage, current_time, channel, country, device_id))
            else:
                if prev_stage == 'verified':
                    alt = np.random.choice(alt_statuses, p=[0.5, 0.3, 0.2])
                    current_time += pd.to_timedelta(np.random.randint(1, 30), unit='m')
                    events.append((user_id, session_id, alt, current_time, channel, country, device_id))
                passed_flow = False
                break

# Создаем DataFrame с новым столбцом session_id
df = pd.DataFrame(events, columns=['user_id', 'session_id', 'event', 'event_time', 'channel', 'country', 'device_id'])

# Добавляем credit_score и loan_amount только тем, кто хотя бы подал заявку
submitted_users = df[df['event'] == 'submitted']['user_id'].unique()
df['credit_score'] = df['user_id'].apply(lambda x: int(np.clip(np.random.normal(650, 50), 300, 850)) if x in submitted_users else None)
df['loan_amount'] = df['user_id'].apply(lambda x: np.random.randint(100, 1000) if x in submitted_users else None)

# Помечаем 2% пользователей как спам
spam_users = np.random.choice(df['user_id'].unique(), size=int(0.02 * n_users), replace=False)
df['is_spam'] = df['user_id'].isin(spam_users).astype(int)

# Считаем время до следующего события
df = df.sort_values(by=['user_id', 'event_time'])
df['time_to_next'] = df.groupby('session_id')['event_time'].shift(-1) - df['event_time']
df['time_to_next'] = df['time_to_next'].dt.total_seconds() / 60  # минуты

# Сохранение в CSV (если нужно)
df.to_csv("/Users/nikitametelkin/Desktop/digital_lending_events.csv", index=False)

# Пример вывода
#print(df.head(10))


#Analyze time to next stage
df_time = df[['user_id', 'session_id', 'event', 'event_time', 'channel', 'country']]
df_time = df_time.loc[(df_time['event'] != 'cancelled') & (df_time['event'] != 'rejected') & (df_time['event'] != 'expired')]
df_time = df_time.sort_values(by=['user_id', 'event_time'])
df_time['time_to_next'] = df_time.groupby('session_id')['event_time'].shift(-1) - df_time['event_time']
df_time['time_to_next'] = df_time['time_to_next'].dt.total_seconds() / 60  # минуты
df_time = df_time.dropna()
status = {'visited': 'visited -> started', 'started': 'started -> submitted', 'submitted': 'submitted -> verified', 'verified': 'verified -> approved', 'approved': 'approved -> funded'}
df_time['transition'] = df_time['event'].map(status)

# Сохранение в CSV (если нужно)
df_time.to_csv("/Users/nikitametelkin/Desktop/digital_lending_time.csv", index=False)


#Cohort analysis
df['event_time'] = pd.to_datetime(df['event_time']).dt.to_period('M')
df = df.merge(df.groupby('user_id')['event_time'].min().reset_index().rename(columns={'event_time': 'start_date'}), how='left', on='user_id')
df = df.loc[df['event'] == 'funded', ['user_id', 'event_time', 'start_date', 'country', 'channel']]
df = df.sort_values(['user_id', 'event_time'])
df['num'] = df.groupby('user_id').cumcount() + 1
# Сохранение в CSV (если нужно)
df.to_csv("/Users/nikitametelkin/Desktop/digital_lending_retention.csv", index=False)


retention = {}
for dt in df['start_date'].unique():
    retention[dt] = []
    for i in range(1, max(df['num'])+1):
        retention[dt].append(round(100 * len(df.loc[(df['start_date'] == dt) & (df['num'] == i)]) / len(df.loc[(df['start_date'] == dt) & (df['num'] == 1)]),2))


print(pd.DataFrame(retention))


# Результат: df

# # Построение графика
# plt.figure(figsize=(8, 5))
# bars = plt.bar(funnel_counts.index, funnel_counts.values, color='skyblue')
# plt.title('Loan Application Funnel')
# plt.xlabel('Stage')
# plt.ylabel('Number of Users')
# plt.grid(axis='y', linestyle='--', alpha=0.6)
#
# # Подписи на столбиках
# for bar in bars:
#     yval = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2, yval + 100, int(yval), ha='center', va='bottom')
#
# plt.tight_layout()
# plt.show()