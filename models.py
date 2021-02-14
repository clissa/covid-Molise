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

# Ignore harmless warnings
import warnings

warnings.filterwarnings("ignore")

pred_dict = {}
text = ''

settings = ["DEGENZA ORDINARIA COVID", "TERAPIA INTENSIVA COVID",
            "DEGENZA MED GENERALE NO COVID", "DEGENZA MED SPECIALISTICA NO COVID"]


#             , "DEGENZA CHIR GENERALE NO COVID", "DEGENZA CHIR SPECIALISTICA NO COVID"]

def gridsearch_SARIMAX(data, setting, exogenous, start_training, end_training, d=1, D=1, m=7, out_of_sample_size=7,
                       seasonal=True, trend='ct', scoring='mae', stepwise=True, method='nm'):
    # TODO: implement saving mechanism to store best configuration
    from pmdarima import auto_arima
    import warnings
    warnings.filterwarnings("ignore")
    data = data.loc[start_training:end_training].copy()
    gridsearch_fit = auto_arima(data[setting], exogenous=data[exogenous],
                                #                                 start_p=2, start_q=0,
                                #                                 max_p=7, max_q=4,
                                d=d, D=D,
                                m=m, seasonal=seasonal, trend=trend,
                                trace=False, out_of_sample_size=out_of_sample_size,
                                scoring=scoring, method=method,
                                error_action='ignore',  # we don't want to know if an order does not work
                                suppress_warnings=True,  # we don't want convergence warnings
                                stepwise=True)
    text = f"Best parameters for {setting}:\nSARIMAX({gridsearch_fit.order})({gridsearch_fit.seasonal_order}) with " \
           f"{gridsearch_fit.trend} trend"
    print(text)

    return gridsearch_fit.order, gridsearch_fit.seasonal_order, gridsearch_fit.trend


def SARIMAX(data, setting, exogenous, start_training, end_training, end_prediction, order, seasonal_order, trend,
            time_varying_regression=False):
    import statsmodels.api as sm

    # subset data
    data = data.loc[start_training:end_training].copy()
    # Construct the model
    model = sm.tsa.SARIMAX(data[setting], exogenous=data[exogenous],
                           trend=trend,
                           order=order,
                           seasonal_order=seasonal_order,
                           time_varying_regression=time_varying_regression)

    # Estimate the parameters
    model = model.fit()
    # Here we construct a more complete results object.
    forecast = model.get_forecast(end_prediction)
    # format_prediction(setting, data, forecast)
    return forecast, model
