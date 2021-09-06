#importa bibliotecas relevantes
import numpy as np
from scipy.stats import expon
import matplotlib.pyplot as plt
import pandas as pd

#define as funções a serem utilizadas no método de Monte Carlo
def theta_n(n, initial_int = 1, end_int = 5, mesh = 100):
    '''Acha o valor \theta que minimiza média(log(f(\theta,x))), onde x vem de uma normal truncada positiva. 
    Note que o parâmetro mesh controla a qualidade da aproximação, sendo maior o mesh, melhor a aproximação.
    No mesh padrão, o erro esperado é de 0.04.
    
    Retorna o valor de \theta que maximiza a média(log(f(\theta,x))) e a distribuição normal padrão truncada gerada'''
    mean_log_pdf = [];
    scales = np.linspace(initial_int, end_int ,mesh) #valores de 1/\theta a serem testados
    truncated_normal = abs(np.random.normal(loc=0.0, scale=1.0, size=n)) #gera a função normal truncada em postivos a ser usada
    for scale in scales:
        mean_log_pdf.append(np.mean(expon.logpdf(truncated_normal, loc=0, scale=1/scale))) #aplica os valores gerados na 
        #distribuição normal truncada positiva como inputs de uma pdf da distribuição exponencial de parâmetro 1/scale
    return [scales[np.argmax(mean_log_pdf)], truncated_normal]

def BoAsquared(truncated_normal, theta):
    '''Retorna o valor do estimador desenvolvido no exercício 3.1 em função da normal truncada geradora dos dados
    e de um valor \theta selecionado.'''
    return theta**2-2*np.mean(truncated_normal)*theta**3+np.mean(truncated_normal**2)*theta**4

def wald(n, theta0, initial_int = 1, end_int =2, mesh = 100, emp = False):
    '''Retorna o teste de Wald desenvolvido para testar theta = theta0, dada uma amostra de n observações iid
    da normal truncada postiva. Se empírico é False, usamos o valor téorico do minimizador'''
    [theta, truncated_normal] = theta_n(n, initial_int, end_int, mesh)
    if emp == False:
        denominator = BoAsquared(truncated_normal, minimizer)
    else:
        denominator = BoAsquared(truncated_normal, theta)
    
    return n*(theta-theta0)**2/denominator

#começamos o método de Monte Carlo gerando valores estatísticos para \hat{theta}_n. Como notado no documento principal, a
#princípio, poderíamos 'pular' esse passo, pois sabemos que o minimizador da distância possui valor teórico de
#\theta_*=\sqrt(pi/2), mas fazer esse processo é útil não só para ver que, de fato, \hat{theta}_n converge para \theta_*,
#mas também para podermos generalizar o processo quando g não é uma função conhecida o que, de fato, é a maior utilidade
#desse método

theta_n_means = []
theta_n_stdvs = []
for n in [10, 50, 100, 200, 500]:
    thetas = []
    for i in range(5000):
        thetas.append(theta_n(n)[0])
    theta_n_means.append(np.mean(thetas))
    theta_n_stdvs.append(np.std(thetas))
    
#faz um gráfico comparando os valores médios empíricos de \theta_n e o valor teórico esperado para \theta_* (\sqrt(pi/2)).
#note que, de fato, os valores estão prócximos do valor teórico e quanto maior n, melhor a proximidade, assim como demonstrado
#no Problema 2.1
fig = plt.figure()
ax = plt.axes()
ax.errorbar([10,50,100,200,500],theta_n_means,theta_n_stdvs, fmt='o')
ax.plot(range(1,520), np.sqrt(np.pi/2)*np.ones(520-1), '--r') 
ax.legend([r'Valor teórico para $\theta_*$'])
ax.grid(color='k', linestyle='-', linewidth=0.1)
ax.set_xlim([1, 513])
plt.show()

#agora, para avaliar os erros tipo I e II do teste vamos usar dois métodos
#no primeiro, avaliamos o teste de Wald desenvolvido usando o valor teórico de \theta_* de \sqrt(pi/2)
#porém, como calcular o valor de \theta_* exige ter conhecimento prévio de da distribuição geradora de dados, vamos também
#desenvolver um método completamente baseado em valores empíricos de \theta_*, calculado a partir de médias de \hat{theta}_n
#como no exemplo anterior

#calcula o valor de \alpha como a quantidade de erros (rejeições de H0 se \theta_0 = \theta_*) em níveis de 10%, 5% e 1%
#note que os valores de quantis da distribuição \chi^2(1) para esses níveis são 2.706, 3.841 e 5.024, respectivamente
minimizer = np.sqrt(np.pi/2)

means_wald_theo_alpha = []
stdvs_wald_theo_alpha = []
for n in [10, 50, 100, 200, 500]:
    mean_n = []
    stdv_n = []
    for error in [2.706, 3.841, 5.024]:
        rejected_H0 = []
        for i in range(5000):
            if wald(n, minimizer)>error:
                 rejected_H0.append(1)
            else:
                rejected_H0.append(0)
        mean_n.append(np.mean(rejected_H0))
        stdv_n.append(np.std(rejected_H0))
    means_wald_theo_alpha.append(mean_n)
    stdvs_wald_theo_alpha.append(stdv_n)

#salva a probabilidade de erro tipo I calculada como dataframe em pandas usando o valor teórico de \theta_* e mostra
print('\n\n\nMédia de Probabilidade de Erro Tipo I com Minimizador Teórico')
mean_theo_alpha = pd.DataFrame(means_wald_theo_alpha,columns=['10%', '5%', '1%'])
mean_theo_alpha['Tamanho do Dataset'] = [10, 50,100,200,500]
mean_theo_alpha.set_index('Tamanho do Dataset', inplace=True)
print(mean_theo_alpha)

print('\n\n\nDesvio Padrão de Probabilidade de Erro Tipo I com Minimizador Teórico')
stdv_theo_alpha = pd.DataFrame(stdvs_wald_theo_alpha,columns=['10%', '5%', '1%'])
stdv_theo_alpha['Tamanho do Dataset'] = [10, 50,100,200,500]
stdv_theo_alpha.set_index('Tamanho do Dataset', inplace=True)
print(stdv_theo_alpha)

#calcula o a probabilidade de erros tipo ii como a quantidade de erros (aceitação de H0 se \theta_0 \neq \theta_*) 
#(em particular, estamos assumindo \theta_0 = 1.1*\theta_*) em níveis de 10%, 5% e 1% 
#note que os valores de quantis da distribuição \chi^2(1) para esses níveis são 2.706, 3.841 e 5.024, respectivamente
means_wald_theo_ii = []
stdvs_wald_theo_ii = []
for n in [10, 50, 100, 200, 500]:
    mean_n = []
    stdv_n = []
    for error in [2.706, 3.841, 5.024]:
        accepted_H0 = []
        for i in range(5000):
            if wald(n, 1.1*minimizer)<=error:
                 accepted_H0.append(1)
            else:
                accepted_H0.append(0)
        mean_n.append(np.mean(accepted_H0))
        stdv_n.append(np.std(accepted_H0))
    means_wald_theo_ii.append(mean_n)
    stdvs_wald_theo_ii.append(stdv_n)
    
#salva a probabilidade de erro tipo II calculada como dataframe em pandas usando o valor teórico de \theta_* e mostra
print('\n\n\nMédia de Probabilidade de Erro Tipo II com Minimizador Teórico')
mean_theo_ii = pd.DataFrame(means_wald_theo_ii,columns=['10%', '5%', '1%'])
mean_theo_ii['Tamanho do Dataset'] = [10, 50,100,200,500]
mean_theo_ii.set_index('Tamanho do Dataset', inplace=True)
print(mean_theo_ii)

print('\n\n\nDesvio Padrão de Probabilidade de Erro Tipo II com Minimizador Teórico')
stdv_theo_ii = pd.DataFrame(stdvs_wald_theo_ii,columns=['10%', '5%', '1%'])
stdv_theo_ii['Tamanho do Dataset'] = [10, 50,100,200,500]
stdv_theo_ii.set_index('Tamanho do Dataset', inplace=True)
print(stdv_theo_ii)

#agora calculamos os erros tipo I e II, só que utilizando o minimizador empírico como \theta_*, calculado em theta_n_means

#novamente, calcula o valor de \alpha como a quantidade de erros (rejeições de H0 se \theta_0 = \theta_*) 
#em níveis de 10%, 5% e 1%
#note que os valores de quantis da distribuição \chi^2(1) para esses níveis são 2.706, 3.841 e 5.024, respectivamente
sizes = [10, 50, 100, 200, 500]

means_wald_emp_alpha = []
stdvs_wald_emp_alpha = []
for n in range(len(sizes)):
    mean_n = []
    stdv_n = []
    for error in [2.706, 3.841, 5.024]:
        rejected_H0 = []
        for i in range(5000):
            if wald(sizes[n], theta_n_means[n], emp = True)>error:
                 rejected_H0.append(1)
            else:
                rejected_H0.append(0)
        mean_n.append(np.mean(rejected_H0))
        stdv_n.append(np.std(rejected_H0))
    means_wald_emp_alpha.append(mean_n)
    stdvs_wald_emp_alpha.append(stdv_n)

#salva a probabilidade de erro tipo I calculada como dataframe em pandas usando o valor teórico de \theta_* e mostra
print('\n\n\nMédia de Probabilidade de Erro Tipo I com Minimizador Empírico')
mean_emp_alpha = pd.DataFrame(means_wald_emp_alpha,columns=['10%', '5%', '1%'])
mean_emp_alpha['Tamanho do Dataset'] = [10, 50,100,200,500]
mean_emp_alpha.set_index('Tamanho do Dataset', inplace=True)
print(mean_emp_alpha)

print('\n\n\nDesvio Padrão de Probabilidade de Erro Tipo I com Minimizador Empírico')
stdv_emp_alpha = pd.DataFrame(stdvs_wald_emp_alpha,columns=['10%', '5%', '1%'])
stdv_emp_alpha['Tamanho do Dataset'] = [10, 50,100,200,500]
stdv_emp_alpha.set_index('Tamanho do Dataset', inplace=True)
print(stdv_emp_alpha)

#calcula o a probabilidade de erros tipo ii como a quantidade de erros (aceitação de H0 se \theta_0 \neq \theta_*) 
#(em particular, estamos assumindo \theta_0 = 1.1*\theta_*) em níveis de 10%, 5% e 1% 
#note que os valores de quantis da distribuição \chi^2(1) para esses níveis são 2.706, 3.841 e 5.024, respectivamente
means_wald_emp_ii = []
stdvs_wald_emp_ii = []
for n in range(len(sizes)):
    mean_n = []
    stdv_n = []
    for error in [2.706, 3.841, 5.024]:
        accepted_H0 = []
        for i in range(5000):
            if wald(sizes[n], 1.1*theta_n_means[n], emp = True)<=error:
                 accepted_H0.append(1)
            else:
                accepted_H0.append(0)
        mean_n.append(np.mean(accepted_H0))
        stdv_n.append(np.std(accepted_H0))
    means_wald_emp_ii.append(mean_n)
    stdvs_wald_emp_ii.append(stdv_n)
    
#salva a probabilidade de erro tipo II calculada como dataframe em pandas usando o valor teórico de \theta_* e mostra
print('\n\n\nMédia de Probabilidade de Erro Tipo II com Minimizador Empírico')
mean_emp_ii = pd.DataFrame(means_wald_emp_ii,columns=['10%', '5%', '1%'])
mean_emp_ii['Tamanho do Dataset'] = [10, 50,100,200,500]
mean_emp_ii.set_index('Tamanho do Dataset', inplace=True)
print(mean_emp_ii)

print('\n\n\nDesvio Padrão de Probabilidade de Erro Tipo II com Minimizador Empírico')
stdv_emp_ii = pd.DataFrame(stdvs_wald_emp_ii,columns=['10%', '5%', '1%'])
stdv_emp_ii['Tamanho do Dataset'] = [10, 50,100,200,500]
stdv_emp_ii.set_index('Tamanho do Dataset', inplace=True)
print(stdv_emp_ii)