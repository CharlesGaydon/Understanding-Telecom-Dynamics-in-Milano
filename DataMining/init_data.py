import pandas as pd
import glob
import re
from learning.model.predict import PredictionResult
def init_data(size):
    # merging multiple files into one pandaframe
    path = 'data'  # use your path
    allFiles = glob.glob(path + "/sms-call-internet-mi-*.txt-sample.csv")
    frame = pd.DataFrame()
    list_ = []
    i = 0
    for file_ in allFiles:
        if i == size:
            break
        i += 1
        df = pd.read_csv(file_,delimiter=',',index_col=None, header=0).sample(frac=.5)
        df['day'] = re.search(r'(\d+-\d+-\d+)',file_.split('/')[-1]).group(1)
        list_.append(df)
    frame = pd.concat(list_)
    frame.columns = ['Id', 'Square', 'Time', 'Country', 'SMSin', 'SMSout', 'Callin', 'Callout', 'Internet', 'day']
    # frame = overload(frame)

    return frame


def apply_overload(df):
    df = df.dropna()
    q = df['SMSin'].quantile(0.7)
    df['overload'] = df['SMSin'].apply(lambda x: x > q)
    return df


def overload(df):
    df = df.dropna()
    df_norm = df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']]

    df_norm = df_norm.astype(float)
    min_max_scaler = preprocessing.MinMaxScaler()
    df_norm = min_max_scaler.fit_transform(df_norm)
    df_norm = pd.DataFrame(df_norm)
    df_norm[5] = df_norm[0] + df_norm[1] + df_norm[2] + df_norm[3] + df_norm[4]
    df = df.reset_index()
    df.head()
    df = df.drop('index', axis=1)

    df['charge'] = df_norm[5]
    ind_overload = df['charge'].quantile(0.90)
    df_overload = df[df['charge'] > ind_overload]

    return df_overload

if __name__ == '__main__':
    df = init_data(10)
    print(df.head())
    print('#'*50)
    q = df['SMSin'].quantile(0.95)
    df['overload'] = df['SMSin'].apply(lambda x: x > q)
