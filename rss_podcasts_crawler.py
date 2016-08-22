#coding: utf-8
#22/08/16
#Elias Soares
#http://eyed3.nicfit.net/api/eyed3.html
from bs4 import BeautifulSoup
import requests
import time
import subprocess
import eyed3

def get_soup(link):
	'''
	Explicação:
		Faz a conexão com as páginas passadas pelo link e retorna um objeto BeautifulSoup.
	'''
	i = 0
	while i < 100:
		time.sleep(1)
		try:
			resp = requests.get(link)
			sopa = BeautifulSoup(resp.content,"html.parser")
			return sopa
		except:
			print("Erro na conexão: " + link)
		i += 1
	return None

def download_episodes(podcast):
	diretory_name = podcast['title'].replace(' ','')
	#Mudando o diretório de download:
	diretory = ' -O ' + diretory_name + '/'

	for episode in podcast['episodes']:
		#Mudando o nome do arquivo que será baixado:
		file_name =  diretory + "'" + episode['name'] + "'"
		print(file_name)
		subprocess.call(['wget -c' + file_name +' ' + episode['link']], shell = True)

def get_podcast_information(rss_link):
	soup = get_soup(rss_link)
	if soup:
		podcast_name = soup.channel.title.text
		podcast = {'title' : podcast_name.replace('&#8211;','')	, 'episodes' : []}
		diretory_name = podcast_name.replace(' ','')
		subprocess.call(['rm -r ' + diretory_name], shell = True)
		subprocess.call(['mkdir ' + diretory_name], shell = True)

		#Para salvarmos os logs de erros:
		with open(diretory_name + '/logs.csv', u'w') as f:
			for epi in soup.channel.findAll('item'):
				try:
					episode_name = epi.title.text
					episode_link = epi.enclosure['url']
					podcast['episodes'].append({'name' : episode_name, 'link': episode_link})
				except TypeError:
					f.write("Erro: Sem link de Download\t" + epi.title.text + "\n")
		return podcast


podcast = get_podcast_information('http://www.portalcafebrasil.com.br/todos/podcasts/feed/')
if podcast : download_episodes(podcast)