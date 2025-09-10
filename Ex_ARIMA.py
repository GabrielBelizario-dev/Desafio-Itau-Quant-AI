from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np


# Assumindo cA4 da secção anterior
# 1. Testar a estacionariedade com o teste ADF
adf_result = adfuller(cA4)
print(f'ADF Statistic: {adf_result}')
print(f'p-value: {adf_result[1]}')
# Se p-value > 0.05, a série provavelmente não é estacionária e precisa de diferenciação.
# Vamos assumir que uma diferenciação é necessária (d=1)
cA4_diff = np.diff(cA4)

# 2. Identificar p e q com gráficos ACF e PACF
fig, axes = plt.subplots(1, 2, figsize=(16, 4))
plot_acf(cA4_diff, ax=axes)
plot_pacf(cA4_diff, ax=axes[1])
plt.show()
# A análise visual dos gráficos sugere ordens para p e q.
# Por exemplo, se o PACF corta após o lag 1 e o ACF decai lentamente, um modelo AR(1) (p=1, q=0) pode ser apropriado.

# 3. Ajustar o modelo ARIMA
# Vamos assumir ordens p=1, d=1, q=1 como exemplo
model_arima = ARIMA(cA4, order=(1, 1, 1))
model_fit = model_arima.fit()
print(model_fit.summary())

# 4. Gerar previsões fora da amostra
# Prever os próximos 10 passos
forecast_steps = 10
forecast = model_fit.forecast(steps=forecast_steps)
print("\nPrevisão dos Coeficientes de Aproximação:")
print(forecast)