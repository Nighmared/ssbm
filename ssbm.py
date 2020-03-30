import requests
from sys import exit
import os


keys = []
saveName = ""


def main():
	global keys
	uName = input('Enter username or leave blank for own ssh keys: ')
	keys = loadKeys(uName)
	choice = 0;
	print('[SSH-Serverside PubKey Manager v0.1 by nighmared]')
	
	while(choice !='99'):
		if(choice == '1'):
			addKey()
		elif(choice == '2'):
			remKey()

		choice = prettymenu('''What would you like to do?
	(1) Add authorized keys
	(2) remove authorized keys
	(99) Exit
		''')



def loadKeys(username = ""):
	global keys
	global saveName
	saveName = username
	try:
		if(username==""):
			file = open(os.path.expanduser('~/.ssh/authorized_keys'),'r')
		else:
			try:
				file = open(os.path.expanduser(f'~/../{username}/.ssh/authorized_keys'),'r')
			except:
				print("must use sudo")
	except FileNotFoundError:
		createFile = input(f"the file was not found, should i create it at\n{os.path.expanduser(f'../{username}/.ssh/authorized_keys')}  ?  (y/n)")
		if(createFile == 'n'):
			print("abort..")
			exit()
		else:
			return keys

	for k in file:
		if(k not in keys):
			keys.append(k)
	file.close()
	return keys


def saveKeys():
	if(input("rly wanna===? ")=='n'):
		return
	if(saveName == ''):
		file = open(os.path.expanduser('~/.ssh/authorized_keys'),'w')
	else:
		file = open(os.path.expanduser(f'~/../{username}/.ssh/authorized_keys'),'w')
	for k in keys:
		file.write(k+"\n")
	file.close()

def prettymenu(text):
	return input(f'''\n\n\n\n\n\n{text}\n\n\n\n\n\n''')


def addKey():
	global keys
	choice = prettymenu('''How would you like to add keys?
	(1) Import from Github
	(2) Enter manually
	(3) Specify file
	(4) Go back
	(99) Exit''')

	while(choice not in ('1','2','3','4','99')):
		choice = prettymenu('''How would you like to add keys?
	(1) Import from Github
	(2) Enter manually
	(3) Specify file
	(4) Go back
	(99) Exit''')


	if(choice == '1'):
		key = getGithub()
	elif(choice == '2'):
		key = getManual()
	elif(choice == '3'):
		key = getFile()

	elif(choice=='4'):
		return
	elif(choice=='99'):
		exit()

	if(key == None):
		print("not ret yeady")
		return
	keys.append(key)
	saveKeys()
	return

def remKey():
	global keys
	if(len(keys) == 0):
		print("no key available :/")
		return

	print("The following keys are currently authorized, select one to remove:")
	for i in range(0,len(keys)):
		print(f"({i+1}) {keys[i]}")
	print("(99) go back to menu")
	keyNum = int(input("choose key: ")) -1
	if(keyNum == 98): return

	while(keyNum>=len(keys) or keyNum<0):
		print("invalid index...")
		for i in range(0,len(keys)):
			print(f"({i+1}) {keys[i]}")
		print("(99) go back to menu")
		keyNum = int(input("choose key: ")) -1
		if(keyNum == 98): return

	toRemKey = keys[keyNum]
	conf = input(f"The following key will be removed from authorized_keys: \n{toRemKey}\n continue? (y/n)")
	if(conf=='y'):
		if(toRemKey in keys):
			keys.remove(toRemKey)
			saveKeys()
			print("removed successfully")
			return
	print("aborted.. -> back to main")
	return



def getFile():
	print("WIP")
	return ""

def getManual():
	print("WIP")
	return ""

def getGithub():
	uName = input("Enter the name of the Github account whose keys you want to add (Leave empty to go back)\n")
	
	if(uName == ''): #given as go back option :)
		return(None)

	doAgain = False
	r = requests.get(f'https://github.com/{uName}.keys')

	if(r.status_code == 200):
		gitKeys = list(map(lambda x: x.strip(),str(r.text).split('\n')[:-1]))
		if(len(gitKeys)<1):
			doAgain = True

	while(r.status_code != 200 or doAgain):
		uName = input("Something wrent wrong (maybe a typo?) please try again: (Leave empty to go back)\n")
		if(uName == ''):
			return(None)

		r = requests.get(f'https://github.com/{uName}.keys')
		if(r.status_code == 200):
			gitKeys = list(map(lambda x: x.strip(),str(r.text).split('\n')[:-1]))
			if(len(gitKeys)>0):
				doAgain = False

	if(len(gitKeys) == 1):
		key = gitKeys[0]	

	elif(len(gitKeys)>1):
		print("Multiple keys were found, which one should i add?")
		for i in range(0,len(gitKeys)):
			print(f"({i+1}) {gitKeys[i]}")

		keyNum = int(input("choose key: ")) -1

		while(keyNum>=len(gitKeys) or keyNum<0):
			print("invalid index...")
			print("Multiple keys were found, which one should i add?")
			for i in range(0,len(gitKeys)):
				print(f"({i+1}) {gitKeys[i]}")
			keyNum = int(input("choose key: ")) -1

		key = gitKeys[keyNum]

	print("The following public key will be added to authorized_keys:")
	print(key)
	conf = input("continue? (y,n)\n")
	if(conf == 'y'):
		return key
	else:
		return None

main()


