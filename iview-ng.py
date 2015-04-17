#!/usr/bin/env python3

import iview.comm
import iview.fetch

promptText = 'iView $ '
running = True

iview.comm.get_config()
index = iview.comm.get_index()

shows = []
eps = []

def findShow(query):
	global shows
	shows = []
	for show in index:
		if show.get('title').find(query) > -1:
			#print('['+str(len(shows))+']', show.get('title'), len(show.get('items')), 'eps')
			print('['+str(len(shows))+']', show.get('title'))
			shows.append(show)

def findEp(showNum):
	global eps
	[eps, _] = iview.comm.get_series_items(shows[showNum].get('id'))
	print(shows[showNum].get('title') + ':')
	i=0
	for ep in eps:
		print('	','['+str(i)+']', '['+ep.get('rating', 'None')+']' , ep.get('title'))
		i+=1

def getEp(epNum):
	ep = eps[epNum]
	print(ep)
	episode = iview.comm.get_episode(ep.get('url'))
	iview.fetch.fetch_program(episode)

def makeIndex():
	global index
	index = iview.comm.get_index()

def main():
	while running:
		prompt(input(promptText))

def prompt(inp):
	global running, shows, eps
	command = inp.split()[0]
	args = inp.split()[1:]
	if command == 'exit':
		running = False
	elif command == 'find' or command == 'f':
		findShow(''.join(args))
	elif command == 'eps' or command == 'e':
		findEp(int(args[0]))
	elif command == 'help' or command == 'h':
		print('''
		Basic Usage:
			#Find a show by searching with the find command
			iView $ find <name of show>
			#The epesodes for a show can be listed using eps and the number in the []'s from the output of the last find command
			iView $ eps 0
			#Inside the second []'s is the rating (G, PG, M, etc.) if there is one
			#Get the show using get and the number in the []'s from the output of the last eps command
			iView $ get 1
		Basic Usage Example:
			iView $ find 7
			[0] 7.30 9 eps
			[1] That '70s Show 10 eps
			iView $ eps 0
			7.30:
				 [0] [None] 7.30 12/12/2014
				 [1] [None] 7.30 11/12/2014
				 [2] [None] 7.30 10/12/2014
				 [3] [None] 7.30 9/12/2014
				 --- extra entries have been removed ---
			iView $ get 1
		''')
	elif command == 'get' or command == 'g':
		getEp(int(args[0]))
	elif command == 'index':
		makeIndex()
	else:
		print('Um error')

if __name__ == "__main__":
	main()
