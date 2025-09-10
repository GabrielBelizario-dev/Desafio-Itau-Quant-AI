import pywt
import numpy as np

# Assumindo 'data' é a sua série temporal de retornos
# Exemplo de dados sintéticos
np.random.seed(42)
data = np.random.randn(1024) * 0.01 + np.linspace(0, 0.05, 1024)

# Escolha da wavelet mãe e do nível de decomposição
wavelet = 'db4'
level = 4

# Realizar a decomposição DWT multinível
coeffs = pywt.wavedec(data, wavelet, level=level)

# Os coeficientes são retornados como uma lista:
cA4, cD4, cD3, cD2, cD1 = coeffs

# Para usar MODWT (SWT) (frequentemente preferível)
# A MODWT retorna uma lista de arrays, um para cada nível de detalhe e um para a aproximação final
modwt_coeffs = pywt.swt(data, wavelet, level=level)
# A ordem é para a MODWT

# Visualizar o número de coeficientes em cada nível para DWT
print("Comprimentos dos coeficientes DWT:")
for i, c in enumerate(coeffs):
    if i == 0:
        print(f"  cA{level}: {len(c)}")
    else:
        print(f"  cD{level - i + 1}: {len(c)}")
