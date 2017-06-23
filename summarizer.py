import re
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
connectors = [
    "the", "for", "a", "as", "an", "or", "and", "thus", "hence", "he", "she"
]

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def summarizer (NumberOfSentences, content):
    sentences = split_into_sentences(content)
    rankedSen = []


    dict = {}

    for sentence in sentences:
        for word in sentence.split(' '):
            word = word.lower()
            if dict.get(word, None) is None:
                dict[word] = 1
            else:
                dict[word] += 1

    for word in connectors:
        dict[word] = 0

    for sentence in sentences:
        sentenceRank = 0
        for word in sentence.split (' '):
            word = word.lower()
            sentenceRank += dict[word]

        rankedSen.append((
            sentenceRank,
            sentence
        ))

    rankedSen.sort(reverse=True)
    rankedSen = [i[1] for i in rankedSen]


    return rankedSen[0:NumberOfSentences]

with open("content.txt") as content_file:
    s = summarizer(5, content_file.read())
    for a in s:
        print(a)



