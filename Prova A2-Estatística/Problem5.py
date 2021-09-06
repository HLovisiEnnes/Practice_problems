#importa as bibliotecas relevantes
import numpy as np
from scipy.stats import expon
import matplotlib.pyplot as plt
from scipy.stats import gamma
import random

#define as funções a serem utilizadas no método de Monte Carlo
def bootstrap(data, B):
    '''Gera B amostras de bootstrap de um dataset'''
    bootstrap_data = [random.choices(data, k=len(data)) for i in range(B)]
    return bootstrap_data

def theta_n(initial_int = 0.1, end_int = 2, mesh = 100, n = 5000):
    '''Gera uma amostragem bootstrap de tamanho n
    para dados de uma distribuição gama com \alpha =1.1 e \beta =0.5. Utiliza esse método
    bootstrap para maximizar a média média(log(f(\theta,x))), achando o \hat{\theta}_n que o faz melhor para cada 
    amostra bootstrap.
    Depois tira a média desses \hat{\theta}_n para as distintas estimações bootstrap, retonando também a amostra de bootstap
    
    Note que o parâmetro mesh controla a qualidade da aproximação, sendo maior o mesh, melhor a aproximação.
    No mesh padrão, o erro esperado é de, aproximadamente, 0.02.'''
    gamma_dis = gamma.rvs(1.1, scale=1/0.5, size=30) #gera a distribuição gama, note que \beta = 1/scale
    bootstrap_data = bootstrap(gamma_dis, B = n) #gera os dados em bootsrap
    
    scales = np.linspace(initial_int, end_int ,mesh) #valores de 1/\theta a serem testados para cada distribuição bootstrap
    maximizer_per_b = [] #para cada amostra de bootstrap, acha o valor de 1/\theta que maximiza a média(log(f(\theta,x)))
    for b in bootstrap_data:
        mean_log_pdf_b = [];
        for scale in scales:
            mean_log_pdf_b.append(np.mean(expon.logpdf(b, loc=0, scale=1/scale)))
        maximizer_per_b.append(scales[np.argmax(mean_log_pdf_b)])
    return [np.mean(maximizer_per_b), np.std(maximizer_per_b), gamma_dis]

def BoAsquared(mean_dist, mean_dist_squared, theta):
    '''Retorna o valor do estimador desenvolvido no exercício 3.1.'''
    return theta**2-2*mean_dist*theta**3+mean_dist_squared*theta**4

def wald(theta0, gamma_dis, theta, initial_int = 0.1, end_int =1, mesh = 50):
    '''Retorna o teste de Wald desenvolvido para testar se f=g, dada uma amostra de 30 observações iid
    de uma distribuição gama.'''
    mean_dist =  np.mean(gamma_dis)
    mean_dist_squared =  np.mean(gamma_dis**2)
    
    denominator = BoAsquared(mean_dist, mean_dist_squared, theta)*(2*mean_dist/theta**2+1)**2
    return len(gamma_dis)*(mean_dist_squared-2*mean_dist/theta+theta-theta0)**2/denominator

#starts by generating a fixed gamma_distribution and a theta_n to minimize it
[theta, theta_stdv ,gamma_dis] = theta_n()
print('Valor encontrado para o minimizador: ',theta, '+/-', theta_stdv)
#agora fazemos uma lista com as predições dos testes de Wald
wald_value = []
for theta_0 in np.linspace(0.1,10,500):
    wald_value.append(wald(theta_0, gamma_dis = gamma_dis, theta = theta))
    
#fazemos então um gráfico para diferentes valores de \theta_0 e note que rejeitamos os que possuem valores maior que 3.84 (linha vermelha)
fig = plt.figure()
ax = plt.axes()
plt.plot(np.linspace(0.1,10,500), 3.84*np.ones(500), '--r')
ax.legend([r'Valor crítico de rejieção em 3.84'])
ax.plot(np.linspace(0.1,10,500),wald_value)
ax.grid(color='k', linestyle='-', linewidth=0.1)
ax.set_xlim([0.15, 9.95])
plt.show()

#vamos retornar o mínimo e máximo do intervalo de probabilidade 1-\alpha
elements_in_region = []
for index in range(len(wald_value)):
    if wald_value[index]<=3.84:
        elements_in_region.append(np.linspace(0.1,10,500)[index])
print('(',min(elements_in_region),',',max(elements_in_region),')')