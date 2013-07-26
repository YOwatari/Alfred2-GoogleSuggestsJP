# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
import alp
import time
from types import StringType


_MAX_RESULTS = 9
_REQUEST_URL = u'http://google.com/complete/search'

def get_suggests_txt(q):
	query = {'hl':u'ja', 'ie':u'UTF-8', 'oe':'UTF-8','output':u'toolbar', 'q':q}
	r = alp.Request(_REQUEST_URL, payload=query)
	r.download()
	#alp.log("status: " + str(r.request.status_code))
	if r.request.status_code != 200:
		return
	return r.request.text
	"""
	proxy = {'http':u'http://proxy-west.uec.ac.jp:8080', 'https':u'https://proxy-west.uec.ac.jp:8080'}
	t = alp.requests.get(_REQUEST_URL, params=query, proxies=proxy)
	return t.text
	"""

def get_word_list(txt, maxresults):
	if txt is None:
		return
	response = ET.fromstring(txt.encode('utf-8'))

	results = []
	for r in response.iter('suggestion'):
		data = r.get('data')
		results.append(data)
		if type(data) is StringType:
			data = unicode(data)
	return results[:maxresults]

def get_filefilter(word_list):
	results = []
	i = 1
	for s in word_list:
		#alp.log((unicode(i)+ u' : ' + s).encode('utf-8'))
		elements = {
				'title':s,
				'subtitle':u'Search for \'%s\'' % s,
				'uid':unicode(i)+u'.'+unicode(int(time.time())),
				'arg':s,
				'valid':u'yes',
				'autocomplete':u'',
		}
		results.append(alp.Item(**elements))
		i += 1
	return results

def complete(query, maxresults=_MAX_RESULTS):
	#alp.log("query: " + str(query))
	#alp.log("maxresults: " + str(maxresults))
	txt = get_suggests_txt(query.decode('utf-8'))
	#alp.log("get xml: " + txt.encode('utf-8'))
	word_list = get_word_list(txt, maxresults)
	Items = get_filefilter(word_list)
	alp.feedback(Items)