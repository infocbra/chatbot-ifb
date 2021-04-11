#-- coding: utf-8 --
#import telebot
#import time
#import urllib
#from urllib.request import urlopen
from bs4 import BeautifulSoup
from telebot import types #selecionando a lib types do telebot
import requests
import os.path
import csv
from datetime import datetime, timezone, timedelta

class Funcoes:

	def BuscaNoticia(URL, soup):
		#url = urlopen(URL)
		#soup = BeautifulSoup(url.read(), "html.parser")
		links = []
		for item in soup.select(".tileHeadline"):
			link = (URL + item.a.get('href'))
			links.append(link)
		#Busca a hora/data
		horario = []
		for item in soup.find_all('div', class_='span2 tileInfo'):
			horario.append(item.find_all('li'))
		for i in range(0, len(horario)):
			horario[i] = "{0} {1}".format(horario[i][2].get_text(), horario[i][3].get_text())
		#Busca a imagem da notícia
		imagem = []
		for item in soup.find_all('div', class_='tileItem'):
			if item.find_all('img'):
				imagem.append('https://www.ifb.edu.br' + item.find_all('img')[0].attrs['src'])
			else:
				imagem.append('')
		#Busca o ttítulo da notícia
		titulo = []
		for item in soup.select('.tileHeadline'):
			texto = item.get_text().strip()
			titulo.append(texto)
		#Busca a descrição da notícia
		descricao = []
		for item in soup.select('.description'):
			texto = item.get_text().strip()
			descricao.append(texto)
		#Busca o link da notícia
		link_noticia = []
		for item in soup.select('.tileHeadline'):
			link_noticia.append('https://www.ifb.edu.br' + item.a.get('href'))
		#estrutura em dic
		lista_noticia = []
		for i in range(len(link_noticia)):
			noticia = {
					'titulo' : titulo[i],
					'horario' : horario[i],
					'descricao' : descricao[i],
					'imagem' : imagem[i],
					'link' : links[i]
			}
			lista_noticia.append(noticia)
		return lista_noticia
	def BuscaPersonalizada(query):
		#print('passou busca')
		links = []
		descs = []
		titulos =[]
		query = query.replace(' ', '+')
		URL = "https://google.com/search?q={}".format(query)
		USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
		headers = {"user-agent" : USER_AGENT}
		resp = requests.get(URL, headers=headers)
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, "html.parser")
		results = []
		#print(soup)
		#print(soup.find_all('div', class_='rc'))
		for g in soup.find_all('div', class_='g'):
			anchors = g.find_all('a')
			if anchors:
				link = anchors[0]['href']
				title = g.find('h3').text
				#desc = g.select('.st').text
			links.append(link)
			titulos.append(title)

		for i in range(len(links)):
			item = {
					"titulo": titulos[i],
					"link": links[i]
					}
			results.append(item)
			#print(item)
		return results

	#botoes integrados
	def inl_keyboard():
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton('Portais do IFB', callback_data = 'portais'))
		markup.add(types.InlineKeyboardButton('Notícias dos Campi', callback_data = 'noticias'))
		markup.add(types.InlineKeyboardButton('Canais de notícias', callback_data = 'canais_noticias'))
		markup.add(types.InlineKeyboardButton('Busca Personalizada', callback_data = 'buscapersonalizada'))
		markup.add(types.InlineKeyboardButton('Processo Seletivo', callback_data = 'processoseletivo'))
		#markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', callback_data = 'formulario'))
		return(markup)

	def inl_portais():
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton('Portal IFB', url = 'https://www.ifb.edu.br'))
		markup.add(types.InlineKeyboardButton('Portal do Estudante', url = 'http://portaldoestudante.ifb.edu.br/seguranca/usuarios/entrar'))
		markup.add(types.InlineKeyboardButton('NEAD', url = 'https://nead.ifb.edu.br'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar2'))
		return(markup)

	def inl_botaobuscapersonalizada():
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton('Carregar mais resultados', callback_data = 'carregamais'))
		#markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
		markup.add(types.InlineKeyboardButton('Buscar novamente', callback_data = 'buscapersonalizada'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar'))
		return(markup)

	def inl_botaobuscapersonalizada2():
		markup = types.InlineKeyboardMarkup()
		#markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
		markup.add(types.InlineKeyboardButton('Buscar novamente', callback_data = 'buscapersonalizada'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar'))
		return(markup)

	def inl_voltar():
		markup = types.InlineKeyboardMarkup()
		#markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar'))
		return(markup)

	def inl_noticiascampus():
		markup = types.InlineKeyboardMarkup()
		markup.row_width = 2
		markup.add(types.InlineKeyboardButton('IFB Geral', callback_data = 'Reitoria'))
		markup.add(types.InlineKeyboardButton('Brasília', callback_data = 'CampusBrasília'),types.InlineKeyboardButton('Ceilândia', callback_data = 'CampusCeilândia'))
		markup.add(types.InlineKeyboardButton('Estrutural', callback_data = 'CampusEstrutural'),types.InlineKeyboardButton('Gama', callback_data = 'CampusGama'))
		markup.add(types.InlineKeyboardButton('Planaltina', callback_data = 'CampusPlanaltina'),types.InlineKeyboardButton('Recanto das Emas', callback_data = 'CampusRecanto'))
		markup.add(types.InlineKeyboardButton('Riacho Fundo', callback_data = 'CampusRiacho'),types.InlineKeyboardButton('Samambaia', callback_data = 'CampusSamambaia'))
		markup.add(types.InlineKeyboardButton('São Sebastião', callback_data = 'CampusSebastião'),types.InlineKeyboardButton('Taguatinga', callback_data = 'CampusTaguatinga'))
		return(markup)

	def inl_canaisnoticias():
		markup = types.InlineKeyboardMarkup()
		markup.row_width = 2
		markup.add(types.InlineKeyboardButton('IFB Geral', url = 'https://t.me/ifb_informa'))
		markup.add(types.InlineKeyboardButton('Brasília', url = 'https://t.me/ifb_cbra'),types.InlineKeyboardButton('Ceilândia', url = 'https://t.me/ifb_ccei'))
		markup.add(types.InlineKeyboardButton('Estrutural', url = 'https://t.me/ifb_cest'),types.InlineKeyboardButton('Gama', url = 'https://t.me/ifb_cgam'))
		markup.add(types.InlineKeyboardButton('Planaltina', url = 'https://t.me/ifb_cpla'),types.InlineKeyboardButton('Recanto das Emas', url = 'https://t.me/ifb_crem'))
		markup.add(types.InlineKeyboardButton('Riacho Fundo', url = 'https://t.me/ifb_crfi'),types.InlineKeyboardButton('Samambaia', url = 'https://t.me/ifb_csam'))
		markup.add(types.InlineKeyboardButton('São Sebastião', url = 'https://t.me/ifb_cssb'),types.InlineKeyboardButton('Taguatinga', url = 'https://t.me/ifb_ctag'))
		#markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar2'))
		return(markup)

	def inl_formulario():
		markup = types.InlineKeyboardMarkup()
		markup.row_width = 2
		markup.add(types.InlineKeyboardButton('Avaliar agora', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
		markup.add(types.InlineKeyboardButton('Menu Principal', callback_data = 'voltar'))
		return(markup)

	#salva atividade dos usuários em csv
	def registro_atividade(cid, message, fuso, usage_register, botao):
		registro_usabilidade = {
				'id': cid,
				'date': datetime.fromtimestamp(message.date).astimezone(fuso),
				'cod_action': botao
		}
		csv2_columns = ['id', 'date', 'cod_action']
		if os.path.exists(usage_register):
			with open(usage_register, 'r+',newline='') as csv2_file:
				reader = csv.DictReader(csv2_file)
				dados_existentes = [dado for dado in reader]

				writer = csv.DictWriter(csv2_file, fieldnames=csv2_columns)
				writer.writerow(registro_usabilidade)
		else:
			with open(usage_register, 'w', newline='') as csv2_file:
				writer = csv.DictWriter(csv2_file, fieldnames=csv2_columns)
				writer.writeheader()
				writer.writerow(registro_usabilidade)

	def registro_usuarios(cid, message, fuso, register, ja_registrado):
		registro_user = {
				'id': cid,
				'date': datetime.fromtimestamp(message.date).astimezone(fuso)
		}
		csv_columns = ['id', 'date']
		if os.path.exists(register):
			with open(register, 'r+',newline='') as csv_file:
				reader = csv.DictReader(csv_file)
				dados_existentes = [dado for dado in reader]

				writer = csv.DictWriter(csv_file, fieldnames=csv_columns)

				for dado in dados_existentes:
					ja_registrado.append(dado['id'])

				if (str(registro_user['id']) not in ja_registrado):
					writer.writerow(registro_user)
		else:
			with open(register, 'w', newline='') as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
				writer.writeheader()
				writer.writerow(registro_user)
'''def inl_keyboard():
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('🌐Portal IFB', callback_data = 'portais'))
	markup.add(types.InlineKeyboardButton('📣Notícias dos Campi', callback_data = 'noticias'))
	markup.add(types.InlineKeyboardButton('💬Busca Personalizada', callback_data = 'buscapersonalizada'))
	markup.add(types.InlineKeyboardButton('📝Processo Seletivo', callback_data = 'processoseletivo'))
	markup.add(types.InlineKeyboardButton('✅Clique aqui para avaliar essa ferramenta', callback_data = 'formulario'))
	return(markup)'''

#função para tratar erro de requisição de pagina web
'''def pegaPagina(url):
	try:
		resposta = urlopen(url)
		#conferir o codigo da resposta http para dar continuidade à função
		#retornar o codigo do erro
		soup = BeautifulSoup(resposta.read(), "html.parser")
		return soup
	except urllib.error.HTTPError as erro:
		print("Não foi possível atender a solicitação segue a descrição do erro:")
		print(str(erro))'''

#botão que não está sendo utilizado no momento
'''def inl_botaoprocessoseletivo():
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('✅Avalie esta ferramenta', url = 'https://forms.gle/22f6dxrE5VpiA4Pq5'))
	markup.add(types.InlineKeyboardButton('Carregar mais notícias sobre processos seletivos', callback_data = 'processoseletivo2'))
	markup.add(types.InlineKeyboardButton('Voltar', callback_data = 'voltar'))
	return(markup)'''
