#-- coding: utf-8 --
import telebot #importando a biblioteca pyTelegramBotAPI
import json
import urllib
from functions import Funcoes
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
from config_token import Token as t

API_TOKEN = t.token['chatbot'] #@ifb_informa_bot
bot = telebot.TeleBot(API_TOKEN) #token
f = Funcoes#intancia classe Funcoes
#arquivos csv para registro de atividade de usuários
register = 'register.csv'
usage_register = 'usage_register.csv'
ja_registrado = []
fuso = timezone(timedelta(hours = -3)) #setando o fuso horário dos registros
#--------------------------------------------   MENSAGENS INICIAIS ------------------------------------------------
#cria dicionário para carregar mais noticias
bot.last_message_sent = {}
#funcao para apagar menu
'''def getMensagem(cid, mensagem_anterior):
	#try:
	getattr(bot.message, "message_id",bot.last_message_sent[cid] - 4)'''
		
	#except:
	#	print('')
	
'''bot.last_message_sent[cid] = msg.message_id
mensagem_anterior = bot.last_message_sent[cid]
deletar(cid, mensagem_anterior)
'''

#mensagem inicio
@bot.message_handler(commands=['start','voltar','voltar2']) #recebo mensagem /start
def send_welcome(message):
	botao = 'start'
	cid = message.chat.id #pega o id da conversa    #concatenar id --> + str(cid) +
	msg = bot.send_message(cid, 'Selecione uma das funções abaixo:', reply_markup = f.inl_keyboard()) #mensagem enviada para o usuário
	bot.send_message(cid, '*Este chat segue em fase de melhoria*')
	#dicionário registro de novos usuários
	f.registro_usuarios(cid, message, fuso, register, ja_registrado)
	#f.registro_atividade(cid, message, fuso, usage_register, botao)
def send_voltar(message):
	botao = 'voltar'
	cid = message.chat.id #pega o id da conversa    #concatenar id --> + str(cid) +
	msg = bot.send_message(cid, 'Selecione uma das funções abaixo:', reply_markup = f.inl_keyboard()) #mensagem enviada para o usuário
	bot.send_message(cid, '*Este chat segue em fase de melhoria*')
	#dicionário registro de novos usuários
	f.registro_atividade(cid, message, fuso, usage_register, botao)
def send_voltar2(message):
	botao = 'voltar'
	cid = message.chat.id #pega o id da conversa    #concatenar id --> + str(cid) +
	#deleta menu anterior
	bot.last_message_sent[cid] = message.message_id
	mensagem_anterior = bot.last_message_sent[cid]
	bot.delete_message(cid, mensagem_anterior)

	msg = bot.send_message(cid, 'Selecione uma das funções abaixo:', reply_markup = f.inl_keyboard()) #mensagem enviada para o usuário
	#bot.send_message(cid, '*Este chat segue em fase de melhoria*')
	#dicionário registro de novos usuários
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão ajuda com funções
@bot.message_handler(commands=['ajuda'])#adicionar todas as funções
def send_help(message):
	botao = 'Ajuda'
	cid = message.chat.id
	msg_help = bot.send_message(cid,'Lembre-se das funções possíveis!\n/start = Recomeçar o bot.\n/portais = Receber link para portais do IFB.\n/noticias = Receber as três últimas notícias de algum campus.\n/buscapersonalizada = Buscar notícias do IFB por palavras-chave.\n/processoseletivo = Recebe as 4 últimas notícias a respeito dos processos seletivos do IFB.')
	f.registro_atividade(cid, message, fuso, usage_register, botao)
#--------------------------------------------OPÇÕES DOS BOTÕES------------------------------------------------
#OPÇÕES DE PORTAIS DO IFB
@bot.message_handler(commands=['portais'])
def send_portais(message):
	botao = 'menu_portais'
	cid = message.chat.id
	#deleta menu anterior
	bot.last_message_sent[cid] = message.message_id
	mensagem_anterior = bot.last_message_sent[cid]
	bot.delete_message(cid, mensagem_anterior)
	msg = bot.send_message(cid, 'Selecione o portal:', reply_markup = f.inl_portais())
'''def send_portais(message):
	botao = 'menu_portais'
	cid = message.chat.id
	msg = bot.send_message(cid,
	'''
'''Link para acessar o Portal do IFB:
https://www.ifb.edu.br

Conheça também:
Portal do Estudante:
http://portaldoestudante.ifb.edu.br/seguranca/usuarios/entrar
Educação à Distância:
https://nead.ifb.edu.br'''''',
parse_mode = "markdown",reply_markup=f.inl_voltar())
#msg_portais = bot.send_message(cid,'Escolha o portal desejado', reply_markup = f.inl_portais()) #opções que devem aparecer
f.registro_atividade(cid, message, fuso, usage_register, botao)'''

#OPÇÕES DE CAMPUS PARA NOTÍCIAS
@bot.message_handler(commands=['noticias'])
def send_noticias(message):
	botao = 'menu_noticias_campus'
	cid = message.chat.id
	msg_botoesnoticias = bot.send_message(cid, 'Clique no campus desejado', reply_markup = f.inl_noticiascampus()) #opções que devem aparecer
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#CANAIS DE NOTICIAS DO IFB NO TELEGRAM
@bot.message_handler(commands=['canais_noticias'])
def send_canais(message):
	botao = 'menu_canais_noticias'
	cid = message.chat.id
	bot.last_message_sent[cid] = message.message_id
	mensagem_anterior = bot.last_message_sent[cid]
	bot.delete_message(cid, mensagem_anterior)
	
	msg_botoesnoticias = bot.send_message(cid, '*Clique no canal desejado*', reply_markup = f.inl_canaisnoticias(), parse_mode = "markdown") #opções que devem aparecer
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#REALIZA BUSCA POR PALAVRAS CHAVES
@bot.message_handler(commands=['buscapersonalizada','carregamais'])
def send_mensagembusca(message):
	cid = message.chat.id
	msg_palavrabusca = bot.send_message(cid, 'Digite as palavras-chave para buscar: \n(ex.: calendário acadêmico 2020)')
	bot.register_next_step_handler(message, send_buscapersonalizada)

def send_buscapersonalizada(message):
	botao = 'menu_busca_personalizada'
	cid = message.chat.id
	f.registro_atividade(cid, message, fuso, usage_register, botao)
	mensagem_busca = message.text
	msg_busca = {
		'cid' : cid,
		'text' : message.text
	}
	msg = message.message_id
	bot.last_message_sent[msg] = message.text
	query = mensagem_busca + " site:ifb.edu.br" #input da busca personalizada
	lista_noticia = f.BuscaPersonalizada(query)
	#print(lista_noticia)
	try:
		msg_buscapersonalizada = bot.send_message(cid, "Aqui estão os resultados da sua busca: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_noticia[i].values()):
				resultado.append(conteudo)
			mensagem = "*{0}* \n\n{1}\n".format(resultado[0],resultado[1])
			if i == 2:
				try:
					bot.send_message(cid, mensagem, parse_mode = "markdown", reply_markup = f.inl_botaobuscapersonalizada())
				except:
					bot.send_message(cid,'Não foi possível carregar este resultado', reply_markup = f.inl_botaobuscapersonalizada())
			else:
				try:
					bot.send_message(cid, mensagem, parse_mode = "markdown")
				except:
					bot.send_message(cid,'Não foi possível carregar este resultado')
	except:bot.send_message(cid,'Não há resultados para essa busca.', reply_markup = f.inl_botaobuscapersonalizada2())
	message = mensagem_busca

def send_buscapersonalizada2(msg, message, x, y):
	botao = 'busca_personalizada_carrega_mais'
	cid = msg.chat.id
	mensagem_busca = message
	query = mensagem_busca + " site:ifb.edu.br" #input da busca personalizada
	lista_noticia = f.BuscaPersonalizada(query)
	msg_buscapersonalizada = bot.send_message(cid, "Aqui estão mais 3 resultados da sua busca: ")
	for i in range(x, y):
		resultado = []
		for conteudo in (lista_noticia[i].values()):
			resultado.append(conteudo)
		mensagem = "*{0}* \n\n{1}\n".format(resultado[0],resultado[1])
		if i == 5:
			try:
				bot.send_message(cid, mensagem, parse_mode = "markdown", reply_markup = f.inl_botaobuscapersonalizada2())
			except:
				bot.send_message(cid,'Não foi possível carregar este resultado', reply_markup = f.inl_botaobuscapersonalizada2())
		else:
			try:
				bot.send_message(cid, mensagem, parse_mode = "markdown")
			except:
				bot.send_message(cid,'Não foi possível carregar este resultado')
	f.registro_atividade(cid, msg, fuso, usage_register, botao)

@bot.message_handler(commands=['formulario'])
def send_formulario(message):
	botao = 'botao_avaliacao'
	cid = message.chat.id
	msg = bot.send_message(cid, 'Selecione uma das opções:', reply_markup = f.inl_formulario())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#--------------------------------------------BOTÕES LINK PORTAIS------------------------------------------

#--------------------------------------------FUNÇÕES NOTICIAS----------------------------------------------
#botão reitoria
@bot.message_handler(commands=['Reitoria'])
def send_noticiareitoria(message):
	botao = 'noticias_reitoria'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/reitori"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiareitoria = bot.send_message(cid, "Aqui estão as 3 últimas notícias destaque do IFB: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias destaques do IFB acesse o canal @ifb_informa. ', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão brasília
@bot.message_handler(commands=['CampusBrasília'])
def send_noticiabrasilia(message):
	botao = 'noticias_brasilia'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/brasilia/noticiasbrasilia"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiabrasilia = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Brasília: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Brasília acesse o canal @ifb_cbra', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão ceilândia
@bot.message_handler(commands=['CampusCeilândia'])
def send_noticiaceilandia(message):
	botao = 'noticias_ceilandia'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/campus-ceilandia/noticiasceilandia"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiaceilandia = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Ceilândia: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Ceilândia acesse o canal @ifb_ccei', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
			bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão estrutural
@bot.message_handler(commands=['CampusEstrutural'])
def send_noticiaestrutural(message):
	botao = 'noticias_estrutural'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/campus-estrutural"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiaestrutural = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Estrutural: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Estrutural acesse o canal @ifb_cest', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)
#botão gama
@bot.message_handler(commands=['CampusGama'])
def send_noticiagama(message):
	botao = 'noticias_gama'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/gama/noticiasgama"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiagama = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Gama: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Gama acesse o canal @ifb_cgam', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão planaltina
@bot.message_handler(commands=['CampusPlanaltina'])
def send_noticiaplanaltina(message):
	botao = 'noticias_planaltina'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/planaltina/noticiasplanaltina"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiaplanaltina = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Planaltina: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Planaltina acesse o canal @ifb_cpla', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão recanto das emas
@bot.message_handler(commands=['CampusRecanto'])
def send_noticiarecanto(message):
	botao = 'noticias_recanto'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/recantodasemas"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiarecanto = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Recanto das Emas: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Recanto das Emas acesse o canal @ifb_crem', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)
#botão riacho fundo
@bot.message_handler(commands=['CampusRiacho'])
def send_noticiariacho(message):
	botao = 'noticas_riacho'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/riachofundo/noticiasriachofundo"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiariacho = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Riacho Fundo: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Riacho Fundo acesse o canal @ifb_crfi', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão samambaia
@bot.message_handler(commands=['CampusSamambaia'])
def send_noticiasamambaia(message):
	botao = 'noticias_samambaia'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/samambaia/noticiassamambaia"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiasamambaia = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Samambaia: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Samambaia acesse o canal @ifb_csam', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão são sebastião
@bot.message_handler(commands=['CampusSebastião'])
def send_noticiasebastiao(message):
	botao = 'noticias_sebastiao'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/saosebastiao/noticiassaosebastiao"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiasebastiao = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus São Sebastião: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus São Sebastião acesse o canal @ifb_cssb', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão taguatinga
@bot.message_handler(commands=['CampusTaguatinga'])
def send_noticiataguatinga(message):
	botao = 'noticias_taguatinga'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/taguatinga/noticiastaguatinga"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiataguatinga = bot.send_message(cid, "Aqui estão as 3 últimas notícias do Campus Taguatinga: ")
		for i in range(0, 3):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			if resultado[3] == '':
				bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
			else:
				bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
		bot.send_message(cid,'Para acompanhar as notícias do campus Taguatinga acesse o canal @ifb_ctag', reply_markup = f.inl_voltar())
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)

#botão PROCESSO SELETIVO
@bot.message_handler(commands=['processoseletivo'])
def send_noticiaprocessoseletivo(message):
	botao = 'menu_processo_seletivo'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/estude-no-ifb/noticias"
	try:
		url = urlopen(URL)
		soup = BeautifulSoup(url.read(), "html.parser")
		lista_link = f.BuscaNoticia(URL, soup)
		msg_noticiaprocessoseletivo = bot.send_message(cid, "Aqui estão as 4 últimas notícias sobre Processos Seletivos do IFB: ")
		for i in range(0, 4):
			resultado = []
			for conteudo in (lista_link[i].values()):
				resultado.append(conteudo)
			mensagem = "*{0}* \n [.]({1}).\n {2}\n".format(resultado[0],resultado[3],resultado[4])
			if i == 3:
				if resultado[3] == '':
					bot.send_message(cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown",reply_markup = f.inl_voltar())
				else:
					bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown",reply_markup = f.inl_voltar())
			else:
				if resultado[3] == '':
					bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
				else:
					bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
		bot.send_message(cid,"Não foi possível atender a solicitação, segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)



#Gerenciador de comandos dos botões
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	if call.data == 'portais':
		send_portais(call.message)
	elif call.data == 'noticias':
		send_noticias(call.message)
	elif call.data == 'canais_noticias':
		send_canais(call.message)
	elif call.data == 'buscapersonalizada':
		send_mensagembusca(call.message)
	elif call.data == 'carregamais':
		cid = call.message.chat.id
		msg = call.message.message_id
		print(bot.last_message_sent[msg - 4])
		send_buscapersonalizada2(call.message,bot.last_message_sent[msg - 4], 3, 6)
	elif call.data == 'start':
		send_welcome(call.message)
	elif call.data == 'voltar':
		send_voltar(call.message)
	elif call.data == 'voltar2':
		send_voltar2(call.message)
	elif call.data == 'Reitoria':
		send_noticiareitoria(call.message)
	elif call.data == 'CampusBrasília':
		send_noticiabrasilia(call.message)
	elif call.data == 'CampusCeilândia':
		send_noticiaceilandia(call.message)
	elif call.data == 'CampusEstrutural':
		send_noticiaestrutural(call.message)
	elif call.data == 'CampusGama':
		send_noticiagama(call.message)
	elif call.data == 'CampusPlanaltina':
		send_noticiaplanaltina(call.message)
	elif call.data == 'CampusRecanto':
		send_noticiarecanto(call.message)
	elif call.data == 'CampusRiacho':
		send_noticiariacho(call.message)
	elif call.data == 'CampusSamambaia':
		send_noticiasamambaia(call.message)
	elif call.data == 'CampusSebastião':
		send_noticiasebastiao(call.message)
	elif call.data == 'CampusTaguatinga':
		send_noticiataguatinga(call.message)
	elif call.data == 'processoseletivo':
		send_noticiaprocessoseletivo(call.message)
	elif call.data == 'processoseletivo2':
		send_noticiaprocessoseletivo2(call.message)
	elif call.data == 'formulario':
		send_formulario(call.message)
	elif call.data == 'avaliacao':
		send_botao_avaliacao(call.message)

bot.polling() #escuta usuário

'''@bot.message_handler(commands=['processoseletivo2'])
def send_noticiaprocessoseletivo2(message):
	botao = 'Mais resultados Proc. Seletivo'
	cid = message.chat.id
	URL = "https://www.ifb.edu.br/estude-no-ifb/noticias"
	try:
			url = urlopen(URL)
			soup = BeautifulSoup(url.read(), "html.parser")
			lista_link = f.BuscaNoticia(URL, soup)
			msg_noticiaprocessoseletivo = bot.send_message(cid, "Aqui estão mais 4 notícias sobre Processos Seletivos do IFB: ")
			for i in range(4, 8):
					resultado = []
					for conteudo in (lista_link[i].values()):
							resultado.append(conteudo)
					mensagem = "*{0}* \n [.]({1}).\n {2}\n".format(resultado[0],resultado[3],resultado[4])
					if i == 3:
							if resultado[3] == '':
									bot.send_message(cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown",reply_markup = f.inl_voltar())
							else:
									bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown",reply_markup = f.inl_voltar())
					else:
							if resultado[3] == '':
									bot.send_message (cid,"*{0}*\n\n{1}\n".format(resultado[0],resultado[4]), parse_mode = "markdown")
							else:
									bot.send_photo(cid,resultado[3],"*{0}*\n{1}\n".format(resultado[0],resultado[4]),parse_mode = "markdown")
	except (urllib.error.HTTPError, urllib.error.URLError) as erro:
			bot.send_message(cid,"Não foi possível atender a solicitação segue a descrição do erro:\n" + str(erro), reply_markup= f.inl_voltar())
	f.registro_atividade(cid, message, fuso, usage_register, botao)'''
