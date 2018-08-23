#!/usr/bin/python3

import cgi

import cgitb
cgitb.enable()

import os

import string

import nltk

from nltk import word_tokenize, sent_tokenize, Text

play_list = [("Waiting for Godot", "En attendant Godot"), ("All That Fall", "Tous ceux qui tombent"), ("Act Without Words 1", "Acte sans paroles 1"), 
("Act Without Words 2", "Acte sans paroles 2"), ("Endgame", "Fin de partie"),("Krapp's Last Tape", "La Dernière Bande"),("Embers", "Cendres"),("Happy Days", "Oh les beaux jours"),("Cascando", "Cascando"),("Play", "Comédie"),("Words and Music", "Paroles et musique"),("Eh Joe", "Dis Joe"),("Film", 
"Film"),("Breath", "Souffle"),("Come and Go", "Va et vient"),("Not I", "Pas moi"),("Footfalls", "Pas"),("Ghost Trio", "Trio du Fantôme"),("Rough for Radio 1", "Pochade radiophonique"),("Rough for Theatre 1", "Fragment de théâtre 1"),("Rough for Theatre 2", "Fragment de théâtre 2"),("That Time", 
"Cette fois"),("Rough for Radio 2", "Esquisse radiophonique"),("...but the clouds...",  "...que nuages..."),("A Piece of Monologue", "Solo"),("Ohio Impromptu", "Impromptu d'Ohio"),("Rockaby", "Berceuse"),("Nacht und Traume", "Nacht und Traume"),("What Where", "Quoi où"),("Catastrophe", 
"Catastrophe"),("Quad","Quad")]
novel_list = [("Molloy", "Molloy"), ("Malone Dies", "Malone meurt"), ("Murphy", "Murphy"), ("The Unnameable", "L'innommable"), ("Watt", "Watt"), ("How It Is", "Comment c'est"), ("Mercier and Camier", "Mercier et Camier"), ("Company", "Compagnie"), ("Ill Seen Ill Said", "Mal vu mal dit"), 
("Worstword Ho", "Cap au pire")]
short_list = [("A Wet Night", "Rincée Nocturne"), ("Dante and the Lobster", "Dante et le homard"), ("Ding-Dong", "Ding-Dong"), ("Draff", "Résidu"), ("Fingal", "Fingal"), ("Love and Lethe", "Amour et léthé"), ("The Smeraldina's Billet Doux", "Le billet doux de la Smeraldina"), ("Walking Out", 
"Promenade"), ("What a Misfortune", "Quelle calamité"), ("Yellow", "Blême"), ("A Case in a Thousand",""), ("From an Abandoned Work", "D'un ouvrage abandonné"), ("Imagination Dead Imagine", "Imagination morte imaginez"), ("Enough", "Assez"), ("Ping", "Bing"), ("Texts for Nothing", "Textes pour rien"), ("Lessness", "Sans"), ("The Lost Ones", "Le Dépeupleur"), ("The Cliff", ""), ("",""), ("neither", "ni l’un ni l’autre"), ("All Strange Away",""), ("Fizzles", "Foirades"), ("First Love", "Premier amour"), ("The Calmative", "Le calmant"), ("The End", "Le Fin"), ("The Expelled", "L’expulsé"),
("Heard in the Dark 1", ""), ("Heard in the Dark 2", ""), ("One Evening", ""), ("Ceiling", "Plafond"), ("As the Story Was Told", ""), ("Stirrings Still", ""), ("Variations on a Still Point", "")]
directory = r"/srv/http/beckett/"

server = "www.especiallygreatliterature.com/"

path_list = []

plays = {}
novels = {}
shorts = {}
works = {}

def getFileNames(directory):
  for root, dirs, files in os.walk(directory, topdown=False):
    for name in files:
      if name.find("txt") != -1:
        f = os.path.join(root, name)
        path_list.append(f)
  return path_list

def searchSents(string, lang, genre):
    # to do: support regexes
    # This only searches for strings on a sentence level.
    string = string.lower()
    result_dict = {}
    sents = []
    if genre == "drama":
        dict_to_search = plays
    elif genre == "novel":
        dict_to_search = novels
    elif genre == "short_prose":
        dict_to_search = shorts
    for work in dict_to_search.keys():
        if lang == "en":
            sents = dict_to_search[work]["sents_en"]
        else:
            sents = dict_to_search[work]["sents_fr"]
        result_index = 0
        for x in range(0, len(sents)):
            if string in sents[x].lower():
                if work not in result_dict.keys():
                    result_dict[work] = {}
                result_dict[work][result_index] = []
                if len(sents[x]) > 200:
                    location = sents[x].find(string)
                    result_dict[work][result_index].append(sents[x][(location-75):(location+75)])
                else:    
                    try:
                        previous_line = sents[x-1]
                    except IndexError:
                        previous_line = ""
                    try:
                        next_line = sents[x+1]
                    except IndexError:
                        next_line = ""
                    result_dict[work][result_index].append(previous_line)
                    result_dict[work][result_index].append(sents[x])
                    result_dict[work][result_index].append(next_line)
                result_index = result_index + 1
        if result_index != 0:
            url = "url_" + lang
            title = "title_" + lang
            print("Found " + str(result_index) + " results in <a href = 'http://" + dict_to_search[work][url] + "'>" + dict_to_search[work][title] + 
".</a><br>")
    return result_dict

def searchRaws(string, lang, genre):
  string = string.lower()
  textsToSearch = []
  result_dict = {}
  if genre == "drama":
      dict_to_search = plays
  elif genre == "novel":
      dict_to_search = novels
  elif genre == "short":
      dict_to_search = shorts
  for work in dict_to_search.keys():
    if lang == "en":
      raw = dict_to_search[work]["raw_en"]
    else:
      raw = dict_to_search[work]["raw_fr"]
    if string in raw:
      textsToSearch.append(work)
#      print("Found string in" + work)
  for work in textsToSearch:
    getSents(work, genre)
    if lang == "en":
      sents = dict_to_search[work]["sents_en"]
    else:
      sents = dict_to_search[work]["sents_fr"]
    result_index = 0
    for x in range(0, len(sents)):
      if string in sents[x].lower():
          if work not in result_dict.keys():
              result_dict[work] = {}
          result_dict[work][result_index] = []
          if len(sents[x]) > 200:
              location = sents[x].find(string)
              result_dict[work][result_index].append(sents[x][(location-75):(location+75)])
          else:    
              try:
                previous_line = sents[x-1]
              except IndexError:
                  previous_line = ""
              try:
                  next_line = sents[x+1]
              except IndexError:
                  next_line = ""
              result_dict[work][result_index].append(previous_line)
              result_dict[work][result_index].append(sents[x])
              result_dict[work][result_index].append(next_line)
          result_index = result_index + 1
    if result_index != 0:
       url = "url_" + lang
       title = "title_"+lang
       print("Found " + str(result_index) + " results in <a href = 'http://" + dict_to_search[work][url] + "'>" + dict_to_search[work][title] + 
".</a><br>")
  return result_dict

def txtToDict(title_en, genre, getSents=True):
  work = {}
  path_en  = getPath(title_en, path_list)
  file_en = open(path_en, "r", encoding="utf-8")
  work["title_en"] = title_en
  work["path_en"] = path_en
  work["raw_en"] = file_en.read()
#  play["words_en"] = word_tokenize(play["raw_en"])
#  play["text_en"] = Text(play["words_en"])
  work["url_en"] = getURL(path_en)
  if getSents:
    work["sents_en"] = sent_tokenize(work["raw_en"])
  title_fr = getFrenchTitle(title_en, genre)
  path_fr = getPath(title_fr, path_list, language="fr")
  if path_fr != None:
    file_fr = open(path_fr, "r", encoding="utf-8")
    work["title_fr"] = title_fr
    work["path_fr"] = path_fr
    work["raw_fr"] = file_fr.read()
#    play["words_fr"] = word_tokenize(play["raw_fr"])
#    play["text_fr"] = Text(play["words_fr"])
    work["url_fr"] = getURL(path_fr)
    if getSents:
      work["sents_fr"] = sent_tokenize(work["raw_fr"])
#  print("Successfully gobbled up " + title_en + ", AKA " + title_fr)
  file_en.close()
  return work

def initPlays(getSents=True):
    for x in range(0, len(play_list)):
        plays[play_list[x][0]] = txtToDict(play_list[x][0], "drama", getSents)

def initNovels(getSents=True):
    for x in range(0, len(novel_list)):
        novels[novel_list[x][0]] = txtToDict(novel_list[x][0], "novel", getSents)

def initShorts(getSents=True):
    for x in range(0, len(short_list)):
        shorts[short_list[x][0]] = txtToDict(short_list[x][0], "short", getSents)

def getSents(title_en, genre):
  if genre == "drama":
    plays[title_en] = txtToDict(title_en, "drama")
  elif genre == "novel":
    novels[title_en] = txtToDict(title_en, "novel")
  elif genre == "short":
    shorts[title_en] = txtToDict(title_en, "short")

def initAll():
    initPlays()
    initNovels()
    initShorts()
    works["plays"] = plays
    works["novels"] = novels
    works["shorts"] = shorts

def initAllRaw():
    initPlays(getSents=False)
    initNovels(getSents=False)
    initShorts(getSents=False)
    works["plays"] = plays
    works["novels"] = novels
    works["shorts"] = shorts

def printResults(result_dict, genre):
    for key in result_dict.keys():
        if genre == "drama":
            url = plays[key]['url_en']
        elif genre == "novel":
            url = novels[key]['url_en']
        elif genre == "short":
            url = shorts[key]['url_en']
        else:
            url = "error"
# Sometimes this block breaks stuff. I'm not sure why. This is what needs to be fixed for printing search results to a page.
#        print("<h3>* * * Found " + str(len(result_dict[key].keys())) + " results in <a href='http://" + url + "'>" + key+"</a></h3>")
#        for x in range(0, len(result_dict[key].keys())):
#            print("<h4>#" + str(x+1)+"</h4>")
#            for line in result_dict[key][x]:
#                print(line+ "<br>")
        
def getFrenchTitle(title_en, genre):
  if genre == "drama":
      title_fr = [title[1] for title in play_list if title[0] == title_en]
  elif genre == "novel":
      title_fr = [title[1] for title in novel_list if title[0] == title_en]
  elif genre == "short":
      title_fr = [title[1] for title in short_list if title[0] == title_en]
  return title_fr[0]
  
def getURL(path):
  split_path = path.split("/")
  file_info = [entry for entry in split_path if split_path.index(entry) > split_path.index("beckett")]
  url = server + "/beckett/" +  "/".join(file_info)
  url = url.replace(".txt", ".html")
  return url

def getPath(title, path_list, language="en"):
  filename = title.lower()
  accents = [("é", "e"), ("ô", "o"), ("ù", "u"), ("è", "e"), ("â", "a"), (" ", "_"), ("'", ""), (".", "")]
  for x in range(0, len(accents)):
    hit = filename.find(accents[x][0])
    if hit != -1:
      filename = filename.replace(accents[x][0], accents[x][1])
  filename = filename + ".txt"
  if language == "en":
    file_path = [path for path in path_list if filename in path and "english" in path]
  elif language == "fr":
    file_path = [path for path in path_list if filename in path and "french" in path]
  if len(file_path) == 0:
#    print(" XXX Could not find " + title)
    return None
  else:
#    print(" !!! Found " + title)
    return file_path[0]

print("Content-type: text/html")
print()
print("<title>Beckett Search Results</title>")
print("<h1>Beckett Subsublibrarian Search Results:</h1>")


form= cgi.FieldStorage()

path_list = getFileNames(directory)

langs = []
if "en" in form.keys():
	langs.append("en")
if "fr" in form.keys():
	langs.append("fr")

genres = []

initAllRaw()
if "drama" in form.keys():
	genres.append("drama")
if "novel" in form.keys():
	genres.append("novel")
if "short_prose" in form.keys():
	genres.append("short")

print("Languages: " + ', '.join(langs) + "<br>")
print("Genres: " + ', '.join(genres) + "<br><br>")

print("For now, the best way to view your results is to click the link to the work in question and then ctrl+f to find the individual results.<br>")
print("I'm trying to work out the best way to output the search results neatly - coming soon!<br>")

search_string = form['searchstring'].value
print("<h3>You searched for " + search_string + "</h3>")
for genre in genres:
	if "en" in langs:
		print("<h4>Results in English:</h4>")
		results = searchRaws(search_string, "en", genre)
    print(results)
	if "fr" in langs:
		print("<h4>Results in French:</h4>")
		results = searchRaws(search_string, "fr", genre)
    print(results)

print("<hr>")



exit()
