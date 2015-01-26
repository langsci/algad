# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as etree
import re

def cmd(c,v, indent=0):
    return indent*u' '+u"\\%s{%s}"%(c,v) 

def getText(e,field,strtype):
    try:
	return e.find('%s/%s/Run'%(field,strtype)).text
    except AttributeError:
	return False
      

def label2latex(s):
    pass
    #return "\\hypertarget{%s}{}" % s

class LexEntry():
  
    def __init__(self,e):
	self.label = e.attrib['id']
	self.etymology = Etymology(e.find('../LexEtymology'))
	self.headword = Headword(e.find('LexEntry_HeadWord'))
	self.literalmeaning = getText(e,'LexEntry_LiteralMeaning','AStr')
	try:
	    self.pronunciations = [Pronunciation(p) for p in  e.find('LexEntry_Pronunciations').findall('LexPronunciation')]
	except AttributeError:
	    #print("no pronunciation for {}".format(e.attrib["id"]))
	    self.pronunciations = []
	try:
	    self.mlr = MimimalLexReferences(e.find('MimimalLexReferences'))
	except AttributeError:
	    self.mlr = False
	try:
	    self.vfebr = VariantFormEntryBackRefs(e.find('VariantFormEntryBackRefs'))
	except AttributeError:
	    self.vfebr = False
	self.pos = getText(e,'MoStemMsa','AStr')
	self.senses =  [Sense(s) for s in e.find('LexEntry_Senses').findall('LexSense')]
	self.plural = getText(e,'LexEntry_plural_form','AStr')
    
    def toLatex(self): 
	self.etymology.toLatex()
	self.headword.toLatex()
	if self.literalmeaning:
	    print cmd('literalmeaning',self.literalmeaning)
	#print label2latex(self.label)
	if len(self.pronunciations) == 0:
	    print '{\\fixpron}'
	for p in self.pronunciations:
	    p.toLatex()
	if self.mlr:
	    self.mlr.toLatex()
	if self.vfebr:
	    self.vfebr.toLatex()
	if self.plural:
	    print cmd("plural", self.plural)
	if self.pos:
	    print cmd("pos", self.pos)
	if len(self.senses)==1:
	    self.senses[0].toLatex()
	else:
	    for i,s in enumerate(self.senses):
		s.toLatex(number=i+1)

class Headword():
    def __init__(self,e):
	self.word = e.findall('.//Run')[0].text 
	try:
	    self.homograph = e.findall('.//Run')[1].text #better use attrib named style
	except IndexError:
	    self.homograph = False
      
    def toLatex(self):
	print "\\newentry"
	if self.homograph:
	    print "".join([cmd('homograph',self.homograph), cmd('headword',self.word)]).encode('utf-8') 
	else:
	    print cmd('headword',self.word).encode('utf-8') 

    
#class POS():
    #def __init__(self,p): 
	#try:
	    #self.pos = p.find('.//Run').text 
	#except AttributeError:
	    #self.pos = '{\\fixpos}'
	
    #def toLatex(self): 
	#print cmd('pos',self.pos, indent=1).encode('utf-8')
  
    
class Pronunciation():
    def __init__(self,p): 
	self.ipa = p.find('.//Run').text 
      
    def toLatex(self): 
	print cmd('ipa',self.ipa, indent=1).encode('utf-8')
    
class Sense():
    def __init__(self,s):
	self.definition = getText(s,'LexSense_Definition','AStr')
	self.examples = [Example(x) for x in s.findall('.//LexExampleSentence')]     
	self.references = [LexReflink(l) for l in (s.findall('.//LexReferenceLink'))]
	self.scientificname = getText(s,'LexSense_ScientificName','Str')
	self.usagetypes = [a.attrib['name'] for a in (s.findall('LexSense_UsageTypes/Link/Alt'))]
	try:
	    self.lsveferbs = [Veferbs(l) for l in (s.find('LexEntryRef_VariantEntryTypes'))]
	except TypeError:
	    self.lsveferbs = []
	self.lfg = getText(s,'LexSense_lexical_function_glosses','Str')
	self.synpos = getText(s,'MoMorphSynAnalysisLink_MLPartOfSpeech','AStr')
	self.lsgloss = getText(s,'LexSense_Gloss','AStr') 
    
    def toLatex(self,number=False):
	if number:
	    print cmd('sensenr',number,indent=1)
	if self.synpos:
	    print cmd('synpos',self.synpos,indent=2).encode('utf-8')
	if self.definition:
	    print cmd('definition',self.definition,indent=3).encode('utf-8')
	elif self.lsgloss:
	    print cmd('lsgloss',self.lsgloss,indent=3).encode('utf8')
	if len(self.examples) == 1:
	    self.examples[0].toLatex()
	else:
	    for i,example in enumerate(self.examples): 
		example.toLatex(number=i+1)
	for r in self.references:
	    r.toLatex()
	if self.scientificname:
	    print cmd('sciname',self.scientificname)
	for u in self.usagetypes:
	    print cmd('usage',u)
	for l in self.lsveferbs:
	    l.toLatex()
	#if self.synpos:
	    #print cmd('pos',self.synpos)
	#if self.lsgloss:
	    #print cmd('lsgloss',self.lsgloss)
	  
  
class Example():
    def __init__(self,x):
	self.vernacular = False
	try:
	    self.vernacular = x.find('.//LexExampleSentence_Example').find('.//Run').text 
	    self.translations = [Translation(t) for t in x.findall('.//CmTranslation_Translation')]
	except AttributeError:
	    pass
      
    def toLatex(self,number=False):
	if self.vernacular:
	    if number:
		print cmd('exnr',number,indent=5)
	    modvernacular = self.hyphenate(self.vernacular)
	    print cmd('vernacular',self.vernacular,indent=6).encode('utf-8')
	    print cmd('modvernacular',modvernacular,indent=6).encode('utf-8')
	    for t in self.translations: 
		t.toLatex()
	  
    def hyphenate(self,s):
	return re.sub(u"(?<![$ ])([bcdfghjkḱlĺmḿnńǹŋpṕrŕsśtvwxyz])",r"\\-\1",s)  

class Translation():
    def __init__(self,x):
	self.string = x.find('.//Run').text 
    
    def toLatex(self):
	print cmd('trs',self.string,indent=6).encode('utf-8')
	

class Etymology ():
      def __init__(self,e):
	self.form = getText(e,'LexEtymology_Form','AStr')
	self.gloss = getText(e,'LexEtymology_Gloss','AStr')
	self.source = getText(e,'LexEtymology_Source','AUni')
  
      def toLatex(self):
	  if self.form or self.gloss or self.source:
	      print cmd('etymology','',indent=6).encode('utf-8')
	  if self.form:
	      print cmd('etymologyform',self.form,indent=8).encode('utf-8')
	  if self.gloss:
	      print cmd('etymologygloss',self.gloss,indent=8).encode('utf-8')
	  if self.source:
	      print cmd('etymologysrc',self.source,indent=8).encode('utf-8')
	  

class MimimalLexReferences():
      def __init__(self,e):
	  self.lexreflinks = [LexReflink(lrl) for lrl in e.findall('LexReferenceLink')]
	  
      def toLatex(self):
	  for l in lexreflinks:
	      l.toLatex()
	
class LexReflink():
    def __init__(self,e):
	  self.type_ = e.find('LexReferenceLink_Type/Link/Alt').attrib.get('abbr')
	  self.targets = [(l.attrib['target'],l.find('Alt').attrib.get('sense')) for l in e.findall('LexReference_Targets/Link')]  

    def toLatex(self):
	  print cmd('type',self.type_)
	  for t in self.targets:
	    out = "\hyperref[%s]{%s}{}"%t
	  print out.encode('utf8')

class VariantFormEntryBackRefs ():
      def __init__(self,e):
	  self.lexentryreflinks = [LexEntryReflink(lerl) for lerl in e.findall('LexEntryRefLink')]
      
      def toLatex(self):
	  for l in self.lexentryreflinks:
	      l.toLatex()
	
	
class LexEntryReflink():
    def __init__(self,e):
	  self.target = e.find('LexEntryRefLink_OwningEntry/Link').attrib['target']
	  self.alt = e.find('LexEntryRefLink_OwningEntry/Link/Alt').attrib['entry']
	  self.vet = e.find('LexEntryRefLink_VariantEntryTypes/Link/Alt').attrib['revabbr']
	  
    def toLatex(self):
	  print "%s\hyperref{%s}{%s}"%(self.vet,self.target,self.alt)
	
	 

#===================

fn = sys.argv[1]
tree = etree.parse(fn)
root = tree.getroot()

lexentries = []

for entry in root.findall('LexEntry'):
  lexentries.append(LexEntry(entry))
   

for le in lexentries:
  print "%"+30*"-"
  le.toLatex()

  