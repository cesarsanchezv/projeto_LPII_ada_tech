import csv
import json
from tabulate import tabulate
from datetime import datetime

documento = 'str'
principal = 0
data = 0

def carregar_dados(documento):
  """Recebe uma string (documento) e retorna uma lista com tweets.

  Args:
    documento (str): path do dataset de tweets

  Returns:
    tabela (list): dataset de tweets com colunas data, conteúdo e assunto
  """
  while True:
    try:
      documento = input('Digite a rota do arquivo: ')
      arquivo = open(documento, encoding="utf8")
      planilha = csv.reader(
          arquivo,
          delimiter= ',',
          lineterminator='\n'
      )
      tabela = []
      for linha in planilha:
          tabela.append(linha)
      arquivo.close()
      break
    except:
      print('O documento especificado não existe.')
      continue
  limpar_dados(tabela)
  return tabela

def limpar_dados(tabela):
  """Recebe uma lista (tabela), elimina os cabeçalhos,  transforma as datas para objeto
  datetime e elimina os dados não necessários para o programa.

  Args:
    tabela (list): dataset de tweets com colunas date, url, username, content e subject
  
  Returns:
    tabela (list): dataset de tweets com colunas data, conteúdo e assunto
  """
  tabela.pop(0)
  for linha in tabela:
    linha[0] = f'{linha[0][8:10]}/{linha[0][5:7]}/{linha[0][0:4]}'
    data_str = linha[0]
    data_objeto = datetime.strptime(data_str, '%d/%m/%Y').date().strftime('%d-%m-%Y')
    linha[0] = data_objeto
    linha.pop(1)
    linha.pop(1)

def busca_por_data(data,tabela):
  """Recebe um input (data) e retorna uma tabela filtrada por data.

  Args:
    data (str): input de usuário com a data desejada para pesquisa
    tabela (list): dataset de tweets com colunas data, conteúdo e assunto

  Returns:
      busca_data (list): lista filtrada por data
  """
  while True:
    data = input('Digite a data no formato DD/MM/AAAA: ')
    try:
      data_reformulada = datetime.strptime(data, '%d/%m/%Y').date().strftime('%d-%m-%Y')
      data = data_reformulada
      busca_data = [linha for linha in tabela if data == linha[0]]
      print(tabulate(busca_data, headers=['Data','Conteúdo','Assunto']))
      break
    except:
      print('Data inválida, tente novamente')
      continue
  return busca_data

def busca_por_termo(termo,tabela):
  """Recebe um input (termo) e retorna uma tabela filtrada por conteúdo.

  Args:
    termo (str): input de usuário com o termo desejado para pesquisa
    tabela (list): dataset de tweets com colunas data, conteúdo e assunto

  Returns:
      busca_termo (list): lista filtrada por termo
  """
  termo = input('Digite o termo: ').lower()
  busca_termo = [linha for linha in tabela if termo in linha[1].lower()]
  print(tabulate(busca_termo, headers=['Data','Conteúdo','Assunto']))
  return busca_termo

def busca_por_assunto(assunto,tabela):
  """Recebe um input (assunto) e um dataset (tabela) e retorna uma lista filtrada por assunto

  Args:
      assunto (int): input de usuário indicando a opção desejada
      tabela (list): dataset de tweets com colunas data, conteúdo e assunto

  Returns:
      busca_assunto (list): lista filtrada por assunto
  """
  busca_assunto = []
  while True:
    try:
      assunto = int(input('Digite o número da opção escolhida:\n1. Copa do Mundo\n2. Eleições\n3. Ciência de Dados\n4. COVID-19\n5. Sair\nOpção: '))
      if assunto not in range(1,6):
        print('Opção inválida, tente novamente')
        continue
      elif assunto == 1:
        for linha in tabela:
          if linha[2] == 'copa do mundo':
            busca_assunto.append(linha)
        print(tabulate(busca_assunto, headers=['Data','Conteúdo','Assunto']))
        continue
      elif assunto == 2:
        for linha in tabela:
          if linha[2] == 'eleições':
            busca_assunto.append(linha)
        print(tabulate(busca_assunto, headers=['Data','Conteúdo','Assunto']))
        continue
      elif assunto == 3:
        for linha in tabela:
          if linha[2] == 'ciência de dados':
            busca_assunto.append(linha)
        print(tabulate(busca_assunto, headers=['Data','Conteúdo','Assunto']))
        continue
      elif assunto == 4:
        for linha in tabela:
          if linha[2] == 'covid-19':
            busca_assunto.append(linha)
        print(tabulate(busca_assunto, headers=['Data','Conteúdo','Assunto']))
        continue
      elif assunto == 5:
        break
    except:
      print('Opção inválida, tente novamente')
      continue
  return busca_assunto

def salvar_datos(busca_data,busca_termo,busca_assunto):
  """Recebe 3 listas (busca_data, busca_termo, busca_assunto), as soma e salva num arquivo
  em formato json.

  Args:
      busca_data (list): lista de tweets filtrada por data
      busca_termo (list): lista de tweets filtrada por termo
      busca_assunto (list): lista de tweets filtrada por assunto
  
  Returns:
      resultado.json (doc): documento em formato json com resultados de busca
  """
  dicionario_resultado = {}
  lista_resultado = busca_data + busca_termo + busca_assunto
  for linha in lista_resultado:
    linha[0] = str(linha[0])
  for i, elemento in enumerate(lista_resultado, 1):
    dicionario_interno = {
        'data':elemento[0],
        'conteudo':elemento[1],
        'assunto':elemento[2]
    }
    dicionario_resultado[i] = dicionario_interno
  ruta_archivo = 'resultado.json'
  with open(ruta_archivo, 'w') as arquivo:
    json.dump(dicionario_resultado, arquivo)
  print('Arquivo resultado.json salvo com sucesso.')

def menu(principal):
  """Recebe um int (principal) e aciona as funções de busca e salvamento de dados.

  Args:
      principal (int): input do usuário indicando a opção desejada
  """
  tabela = carregar_dados(documento)
  busca_data = []
  busca_termo = []
  busca_assunto = []
  termo = 'str'
  assunto = 0
  while True:
    principal = int(input('Boas vindas ao nosso sistema:\n1 - Buscar tweets por data\n2 - Buscar tweets por termo\n3 - Buscar tweets por assunto\n4 - Salvar resultado da busca\n5 - Sair\nOpção: '))
    if principal not in range(1,6):
      print('Opção inválida, tente novamente')
      continue
    elif principal == 1:
      busca_data = busca_por_data(data,tabela)
      busca_data = busca_data
    elif principal == 2:
      busca_termo = busca_por_termo(termo,tabela)
      busca_termo = busca_termo
    elif principal == 3:
      busca_assunto = busca_por_assunto(assunto,tabela)
      busca_assunto = busca_assunto
    elif principal == 4:
      salvar_datos(busca_data,busca_termo,busca_assunto)
    else:
      break

menu(principal)