# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as etree
import re

def cmd(c,v, indent=0):
  return indent*u' '+u"\\%s{%s}"%(c,v) 

def label2latex(s):
  return "\\hypertarget{%s}{}" % s

class LexEntry():
  
  def __init__(self,e):
    self.headword = Headword(e.find('LexEntry_HeadWord'))
    self.label = e.attrib['id']
    try:
      self.pronunciations = [Pronunciation(p) for p in  e.find('LexEntry_Pronunciations').findall('LexPronunciation')]
    except AttributeError:
      #print("no pronunciation for {}".format(e.attrib["id"]))
      self.pronunciations = []
    self.pos = POS(e.find('MoStemMsa'))
    self.senses =  [Sense(s) for s in e.find('LexEntry_Senses').findall('LexSense')]
  
  def toLatex(self): 
    self.headword.toLatex()
    print label2latex(self.label)
    if len(self.pronunciations) == 0:
      print '{\\fixpron}'
    for p in self.pronunciations:
      p.toLatex()
    self.pos.toLatex()
    if len(self.senses)==1:
      self.senses[0].toLatex()
    else:
      for i,s in enumerate(self.senses):
	s.toLatex(number=i+1)

class Headword():
  def __init__(self,e):
    self.word = e.findall('.//Run')[0].text 
    try:
      self.homograph = e.findall('.//Run')[1].text 
    except IndexError:
      self.homograph = False
  
  def toLatex(self):
    print "\\newentry"
    if self.homograph:
      print "".join([cmd('homograph',self.homograph), cmd('headword',self.word)]).encode('utf-8') 
    else:
      print cmd('headword',self.word).encode('utf-8') 

    
class POS():
  def __init__(self,p): 
    try:
      self.pos = p.find('.//Run').text 
    except AttributeError:
      self.pos = '{\\fixpos}'
    
    
  def toLatex(self): 
    print cmd('pos',self.pos, indent=1).encode('utf-8')
  
    
class Pronunciation():
  def __init__(self,p): 
    self.ipa = p.find('.//Run').text 
    
  def toLatex(self): 
    print cmd('ipa',self.ipa, indent=1).encode('utf-8')
  
class Sense():
  def __init__(self,s):
    try:
      self.synpos = s.find('.//MoMorphSynAnalysisLink_MLPartOfSpeech').find('.//Run').text 
    except AttributeError:	
      #print("no pos for {}".format(s.attrib["id"]))
      self.synpos = '{\\fixpos}'
    try:
      self.definition = s.find('.//LexSense_Definition').find('.//Run').text 
    except AttributeError:
      #print("no definition for {}".format(s.attrib["id"]))      
      self.definition = '{\\fixdef}'
    self.examples = [Example(x) for x in s.findall('.//LexExampleSentence')] 
  
  def toLatex(self,number=False):
    if number:
      print cmd('sensenr',number,indent=1)
    print cmd('synpos',self.synpos,indent=2).encode('utf-8')
    print cmd('definition',self.definition,indent=3).encode('utf-8')
    if len(self.examples) == 1:
      self.examples[0].toLatex()
    else:
      for i,example in enumerate(self.examples): 
	example.toLatex(number=i+1)
	
  
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
      




  

fn = sys.argv[1]
tree = etree.parse(fn)
root = tree.getroot()

lexentries = []

for entry in root.findall('LexEntry'):
  lexentries.append(LexEntry(entry))
   

for le in lexentries:
  print "%"+30*"-"
  le.toLatex()

<CmTranslation_Translation>                                                                                                                                                         
<ExportedDictionary>                                                                                                                                                                
<LexEntry_Etymology>                                                                                                                                                                
<LexEntry_HeadWord>                                                                                                                                                                 
<LexEntry_LiteralMeaning>                                                                                                                                                           
<LexEntry_Pronunciations>                                                                                                                                                           
<LexEntryRefLink_OwningEntry>                                                                                                                                                       
<LexEntryRef_VariantEntryTypes>                                                                                                                                                     
<LexEntry_Senses>
<LexEtymology>
<LexEtymology_Form>
<LexEtymology_Gloss>
<LexEtymology_Source>
<LexExampleSentence_Example>
<LexExampleSentence_Translations>
<LexPronunciation_Form>
<LexReferenceLink>
<LexReferenceLink_Type>
<LexReference_Targets>
<LexSense_Definition>
<LexSense_Examples>
<LexSense_Gloss>
<LexSense_LexSenseReferences>
<LexSense_ScientificName>
<LexSense_UsageTypes>
<LexSense_VariantFormEntryBackRefs>
<Link>
<MoMorphSynAnalysisLink_MLPartOfSpeech>
<MoStemMsa_MLPartOfSpeech>
<Str>

  