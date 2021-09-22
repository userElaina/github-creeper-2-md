import os
import json
import requests
from urllib.parse import unquote_to_bytes,quote_from_bytes

def bencode(x:all)->bytes:
	if isinstance(x,(bytes,bytearray,memoryview,)):
		x=bytes(x)
	else:
		x=str(x).encode(encoding='utf8')
	return x

def urlencode(s:all)->str:
	return quote_from_bytes(bencode(s))

false=False
true=True
null='None'

_port=0
_count=0
def gt(u):
	global _port,_count
	print(_count)
	_count+=1
	return requests.get(u,proxies={
		'http':'http://127.0.0.1:'+str(_port),
		'https':'http://127.0.0.1:'+str(_port)
	}).content

def creep_repos(name:str='userElaina'):
	l_u=list()
	l_archive=list()
	l_fork=list()
	l_star=list()

	u='https://api.github.com/users/'+name+'/repos?sort=updated&pre_page=100&page='
	for page in range(1,2333):
		res=gt(u+str(page))
		l=eval(res.decode('utf8'))
		if not l:
			break
		for i in l:
			if i['fork']:
				l_fork.append(i)
			elif i['archived']:
				l_archive.append(i)
			else:
				l_u.append(i)

	u='https://api.github.com/users/'+name+'/starred?sort=updated&pre_page=100&page='
	for page in range(1,2333):
		res=gt(u+str(page))
		l=eval(res.decode('utf8'))
		if not l:
			break
		l_star+=l
	
	p=os.path.join(os.path.dirname(__file__),name+'-repo.md')
	open(p,'wb')
	f=open(p,'ab')

	f.write('### To Do\n\n'.encode('utf8'))
	for i in l_u:
		s='['+i['name']+']('+i['html_url']+'): '+i['description']+'\n'
		f.write(s.encode('utf8'))

	f.write('\n### Archived\n\n'.encode('utf8'))
	for i in l_archive:
		s='['+i['name']+']('+i['html_url']+'): '+i['description']+'\n'
		f.write(s.encode('utf8'))

	f.write('\n### Fork\n\n'.encode('utf8'))
	for i in l_fork:
		s='['+i['name']+']('+i['html_url']+'): '+i['description']+'\n'
		f.write(s.encode('utf8'))

	f.write('\n### Star\n\n'.encode('utf8'))
	for i in l_star:
		s='['+i['full_name']+']('+i['html_url']+'): '+i['description']+'\n'
		f.write(s.encode('utf8'))

	return len(l_u),len(l_archive),len(l_fork)

def creep_following(name:str='userElaina'):
	l_follow=list()

	u='https://api.github.com/users/'+name+'/following?sort=updated&pre_page=100&page='
	for page in range(1,2333):
		res=gt(u+str(page))
		l=eval(res.decode('utf8'))
		if not l:
			break
		for i in l:
			res=gt(i['url'])
			try:
				l_follow.append(json.loads(res))
			except:
				print(res)
				exit(0)

	p=os.path.join(os.path.dirname(__file__),name+'-follow.md')
	open(p,'wb')
	f=open(p,'ab')

	for i in l_follow:
		for j in ['name','login','bio','blog','company','location','twitter_username','email']:
			if j in i:
				if i[j] in (None,'None',0,False,'False'):
					i[j]=None
			else:
				i[j]=None
		s='[![avatar_url]('+i['avatar_url']+')]('+i['html_url']+')\n'
		s+='\n#### '+str(i['name'])+' ('+str(i['login'])+')\n'
		s+=str(i['bio'])+'\n'
		if i['blog']:
			s+='blog: '+i['blog']+'\n'
		if i['company']:
			s+='company: '+i['company']+'\n'
		if i['location']:
			s+='[![](https://img.shields.io/badge/Location-'+urlencode(i['location'])+'-4285f4?style=flat-square&logo=google-maps)](https://en.wikipedia.org/wiki/'+urlencode(i['location'])+') '
		if i['twitter_username']:
			s+='[![](https://img.shields.io/badge/Twitter-'+i['twitter_username']+'-1da1f2?style=flat-square&logo=twitter)](https://twitter.com/'+i['twitter_username']+')'
		if i['location'] or i['twitter_username']:
			s+='\n'
		if i['email']:
			_x,_y=i['email'].lower().split('@')
			if _y in ('protonmail.com','pm.me'):
				w=('ProtonMail',_x,'8b89cc','protonmail','https://pm.me/')
			elif _y=='gmail.com':
				w=('Gmail',_x,'ea4335','gmail','https://gmail.com/')
			else:
				w=(_y,_x,'005ff9','mail.ru','https://gmail.com/')

			s+='[![](https://img.shields.io/badge/%s-%s-%s?style=flat-square&logo=%s)](%s) '%w
			s+=i['email']+'\n'
		s+='\n\n'
		f.write(s.encode('utf8'))

	return len(l_follow),

_port=23301
print(creep_repos())
_port=23303
print(creep_following())
