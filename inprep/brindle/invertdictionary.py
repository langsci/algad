# -*- coding: utf-8 -*-

import re

class Entry():
  def __init__(self,a):
    for l in a:
      if 'definition' in l or 'gloss' in l:
	self.english = l
	continue
      if r'\headword' in l:
	try:
	  self.vernaculars.append(l)
	except AttributeError:
	  self.vernaculars = [l]
	continue            
      if l.strip().startswith(r'\synpos') or l.strip().startswith(r'\pos'):
	try:
	  self.poss.append(l)
	except AttributeError:
	  self.poss = [l]
      	continue
       
d = {}

entries = open('chapters/dictionary.tex').read().decode('utf8').split('%------------------------------')
#print len(entries)
for e in entries[1:]:
  #print e
  a = e.split('\n')[1:]
  x = Entry(a)
  #print a
  try:
    d[x.english].append(x)
  except KeyError:
    d[x.english] = [x]
  except AttributeError: 
    s =  "%% error in %s"% u''.join(a)
    print s.encode('utf8')
    
for k in sorted(d.keys()):
  print '%'+30*'-'
  print '\\newentry'
  print k.encode('utf8')
  out = []
  for e in d[k]:
    try:
      out.append(''.join([''.join(l)
      for l in zip(e.vernaculars,e.poss)]))      
    except AttributeError:
      print "%%insufficient information for %s".encode('utf8') % k
  print ';\n'.join(out).encode('utf8')      
  