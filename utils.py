#  Copyright (c) 2021. Luca Clissa
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# dictionary for column names of different categories
colnames = {
    'hospitalization': ['ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati', 'isolamento_domiciliare',
                        'totale_positivi', 'variazione_totale_positivi', 'nuovi_positivi', 'ingressi_terapia_intensiva',
                        'dimessi_guariti', 'deceduti', 'casi_da_sospetto_diagnostico', 'casi_da_screening',
                        'totale_casi'],
    'descriptive': ['stato', 'codice_regione', 'lat', 'long'],
    'cases': ['tamponi', 'casi_testati', 'totale_positivi_test_molecolare', 'totale_positivi_test_antigenico_rapido',
              'tamponi_test_molecolare', 'tamponi_test_antigenico_rapido'],
    'others': ['note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2']
}


def import_data(
        url="""https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv""",
        data_cols=['data'], index_cols=[0, 3]):
    """
    Read covid data from GitHub Protezione Civile
    :param url: file path or github url
    :param data_cols: list of columns containing date formats
    :param index_cols: list of columns to use as index
    :return: pandas dataframe
    """
    import pandas as pd
    return pd.read_csv(url, sep=',', parse_dates=data_cols, index_col=index_cols)


def is_business_day(date):
    """
    Distinguish between business days and holidays
    :param date: date or datetime
    :return: bool
    """
    import pandas as pd
    is_business = bool(len(pd.bdate_range(date, date)))
    holidays = ['01/01', '01/05', '02/06', '04/10', '15/08', '01/11', '08/12', '25/12', '26/12']  # manca Pasquetta
    if f"{date.day:02}/{date.month:02}" in holidays:
        is_business = False
    return is_business

def move_col_to_front(df, col): return df[[col] + [x for x in df.columns if x not in col]]  # list(set(df.columns).difference([col]))]


def format_prediction(setting, real_df, pred_df):
    cols = pred_df.summary_frame().columns
    out_df = pred_df.summary_frame()[cols.delete(1)]
    out_df.columns = ["fitted", "lower", "upper"]
    out_df = out_df.join(real_df[setting], how="left")
    out_df = move_col_to_front(out_df, setting)
    return out_df

