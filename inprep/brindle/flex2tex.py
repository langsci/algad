import sys
import xml.etree.ElementTree as etree

def cmd(c,v):
  return u"\\%s{%s}"%(c,v) 

class LexEntry():
  
  def __init__(self,e):
    self.headword = Headword(e.find('LexEntry_HeadWord'))
    try:
      self.pronunciations = [Pronunciation(p) for p in  e.find('LexEntry_Pronunciations').findall('LexPronunciation')]
    except AttributeError:
      print("no pronunciation for {}".format(e.attrib["id"]))
      self.pronunciations = []
    self.senses =  e.find('LexEntry_Senses').findall('LexSense')
  
  def toLatex(self): 
    self.headword.toLatex()
    for p in self.pronunciations:
      p.toLatex()
    #for s in self.senses:
      #s.toLatex()

class Headword():
  def __init__(self,e):
    self.word = e.findall('.//Run')[0].text 
    try:
      self.homograph = e.findall('.//Run')[1].text 
    except IndexError:
      self.homograph = False
  
  def toLatex(self):
    if self.homograph:
      print cmd('homograph',self.homograph)
    print cmd('headword',self.word).encode('utf-8') 
    
class Pronunciation():
  def __init__(self,p): 
    self.ipa = p.find('.//Run').text 
    
  def toLatex(self): 
    print cmd('ipa',self.ipa).encode('utf-8')
  
class Sense():
  def __init__(self):
    pass
  
  def toLatex(self):
    pass



  

fn = sys.argv[1]
tree = etree.parse(fn)
root = tree.getroot()

lexentries = []

for entry in root.findall('LexEntry'):
  lexentries.append(LexEntry(entry))
  
print(len(lexentries))

print(lexentries[0].__dict__)

for le in lexentries:
  le.toLatex()

#<CmTranslation_Translation>                                                                                                                                                         
#<ExportedDictionary>                                                                                                                                                                
#<LexEntry_Etymology>                                                                                                                                                                
#<LexEntry_HeadWord>                                                                                                                                                                 
#<LexEntry_LiteralMeaning>                                                                                                                                                           
#<LexEntry_Pronunciations>                                                                                                                                                           
#<LexEntryRefLink_OwningEntry>                                                                                                                                                       
#<LexEntryRef_VariantEntryTypes>                                                                                                                                                     
#<LexEntry_Senses>
#<LexEtymology>
#<LexEtymology_Form>
#<LexEtymology_Gloss>
#<LexEtymology_Source>
#<LexExampleSentence_Example>
#<LexExampleSentence_Translations>
#<LexPronunciation_Form>
#<LexReferenceLink>
#<LexReferenceLink_Type>
#<LexReference_Targets>
#<LexSense_Definition>
#<LexSense_Examples>
#<LexSense_Gloss>
#<LexSense_LexSenseReferences>
#<LexSense_ScientificName>
#<LexSense_UsageTypes>
#<LexSense_VariantFormEntryBackRefs>
#<Link>
#<MoMorphSynAnalysisLink_MLPartOfSpeech>
#<MoStemMsa_MLPartOfSpeech>
#<Str>

  