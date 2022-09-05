import json
import requests
import nltk
import pyttsx3
import os
import asyncio
import librosa
import soundfile as sf
import time
from nltk.corpus import words

#Uncomment this if you're running for first time.
#nltk.download('words')

basePath = os.path.dirname(os.path.abspath(__file__))
dataFolder = f'{basePath}/data'

#word_list = words.words()
word_list = ['be', 'a', 'in', 'have', 'I', 'he', 'on', 'do', 'say', 'at', 'but', 'not', 'by', 'as', 'go', 'can', 'get', 'all', 'make', 'about', 'know', 'will', 'as', 'up', 'one', 'time', 'there', 'year', 'so', 'think', 'some', 'people', 'take', 'out', 'just', 'see', 'come', 'now', 'like', 'other', 'then', 'two', 'more', 'want', 'way', 'look', 'first', 'also', 'new', 'day', 'more', 'use', 'no', 'man', 'find', 'here', 'thing', 'give', 'many', 'well', 'only', 'tell', 'one', 'very', 'even', 'back', 'any', 'good', 'woman', 'through', 'life', 'child', 'there', 'work', 'down', 'may', 'after', 'call', 'world', 'over', 'school', 'still', 'try', 'in', 'as', 'last', 'ask', 'need', 'too', 'feel', 'three', 'state', 'never', 'become', 'between', 'high', 'really', 'most', 'another', 'much', 'family', 'own', 'out', 'leave', 'put', 'old', 'while', 'mean', 'on', 'keep', 'student', 'why', 'let', 'great', 'same', 'big', 'group', 'begin', 'seem', 'country', 'help', 'talk', 'turn', 'problem', 'every', 'start', 'hand', 'might', 'American', 'show', 'part', 'about', 'place', 'over', 'such', 'again', 'few', 'case', 'most', 'week', 'company', 'system', 'each', 'right', 'program', 'hear', 'so', 'question', 'work', 'play', 'government', 'run', 'small', 'number', 'off', 'always', 'move', 'like', 'night', 'live', 'Mr', 'point', 'believe', 'hold', 'today', 'bring', 'happen', 'next', 'before', 'large', 'all', 'million', 'must', 'home', 'under', 'water', 'room', 'write', 'mother', 'area', 'national', 'money', 'story', 'young', 'fact', 'month', 'different', 'lot', 'right', 'study', 'book', 'eye', 'job', 'word', 'though', 'business', 'issue', 'side', 'kind', 'four', 'head', 'far', 'black', 'long', 'both', 'little', 'house', 'yes', 'after', 'long', 'provide', 'service', 'around', 'friend', 'important', 'father', 'sit', 'away', 'power', 'hour', 'game', 'often', 'yet', 'line', 'political', 'end', 'ever', 'stand', 'bad', 'lose', 'however', 'member', 'pay', 'law', 'meet', 'car', 'city', 'almost', 'include', 'continue', 'set', 'later', 'community', 'much', 'name', 'five', 'once', 'white', 'least', 'president', 'learn', 'real', 'change', 'team', 'minute', 'best', 'several', 'idea', 'kid', 'body', 'information', 'nothing', 'ago', 'right', 'lead', 'social', 'understand', 'back', 'watch', 'together', 'follow', 'around', 'parent', 'only', 'stop', 'face', 'create', 'public', 'already', 'speak', 'read', 'level', 'allow', 'add', 'office', 'spend', 'door', 'health', 'person', 'art', 'sure', 'such', 'war', 'history', 'party', 'within', 'grow', 'result', 'open', 'change', 'morning', 'walk', 'reason', 'low', 'win', 'research', 'girl', 'guy', 'early', 'food', 'before', 'moment', 'air', 'teacher', 'force', 'offer', 'enough', 'both', 'education', 'across', 'remember', 'foot', 'second', 'boy', 'maybe', 'able', 'age', 'off', 'policy', 'love', 'process', 'music', 'consider', 'appear', 'actually', 'buy', 'probably', 'human', 'wait', 'serve', 'market', 'die', 'send', 'expect', 'home', 'sense', 'build', 'stay', 'fall', 'nation', 'plan', 'cut', 'college', 'interest', 'death', 'course', 'someone', 'experience', 'behind', 'reach', 'local', 'kill', 'six', 'remain', 'effect', 'use', 'yeah', 'suggest', 'class', 'control', 'raise', 'care', 'perhaps', 'little', 'late', 'hard', 'field', 'pass', 'former', 'sell', 'major', 'sometimes', 'require', 'along', 'development', 'report', 'role', 'better', 'economic', 'effort', 'up', 'decide', 'rate', 'strong', 'possible', 'heart', 'drug', 'show', 'leader', 'light', 'voice', 'wife', 'whole', 'police', 'mind', 'finally', 'pull', 'return', 'free', 'military', 'price', 'report', 'less', 'according', 'decision', 'explain', 'son', 'hope', 'even', 'develop', 'view', 'relationship', 'carry', 'town', 'road', 'drive', 'arm', 'true', 'federal', 'break', 'better', 'difference', 'thank', 'receive', 'value', 'international', 'building', 'action', 'full', 'model', 'join', 'season', 'society', 'tax', 'director', 'early', 'position', 'player', 'agree', 'especially', 'record', 'pick', 'wear', 'paper', 'special', 'space', 'ground', 'form', 'support', 'event', 'official', 'matter', 'center', 'couple', 'site', 'end', 'project', 'hit', 'base', 'activity', 'star', 'table', 'need', 'court', 'produce', 'eat', 'American', 'teach', 'oil', 'half', 'situation', 'easy', 'cost', 'industry', 'figure', 'face', 'street', 'image', 'phone', 'either', 'data', 'cover', 'quite', 'picture', 'clear', 'practice', 'piece', 'land', 'recent', 'describe', 'product', 'doctor', 'wall', 'patient', 'worker', 'news', 'test', 'movie', 'certain', 'north', 'love', 'personal', 'open', 'support', 'simply', 'third', 'technology', 'catch', 'step', 'baby', 'computer', 'type', 'attention', 'draw', 'film', 'Republican', 'tree', 'source', 'red', 'nearly', 'organization', 'choose', 'cause', 'hair', 'look', 'point', 'century', 'evidence', 'window', 'difficult', 'listen', 'soon', 'culture', 'billion', 'chance', 'brother', 'energy', 'period', 'course', 'summer', 'less', 'realize', 'hundred', 'available', 'plant', 'likely', 'opportunity', 'term', 'short', 'letter', 'condition', 'choice', 'place', 'single', 'rule', 'daughter', 'administration', 'south', 'husband', 'Congress', 'floor', 'campaign', 'material', 'population', 'well', 'call', 'economy', 'medical', 'hospital', 'church', 'close', 'thousand', 'risk', 'current', 'fire', 'future', 'wrong', 'involve', 'defense', 'increase', 'security', 'bank', 'certainly', 'west', 'sport', 'board', 'seek', 'subject', 'officer', 'private', 'rest', 'behavior', 'deal', 'performance', 'fight', 'throw', 'top', 'quickly', 'past', 'goal', 'second', 'bed', 'order', 'author', 'fill', 'represent', 'focus', 'foreign', 'drop', 'plan', 'blood', 'agency', 'push', 'nature', 'color', 'no', 'recently', 'store', 'reduce', 'sound', 'note', 'fine', 'before', 'near', 'movement', 'page', 'enter', 'share', 'common', 'poor', 'other', 'natural', 'race', 'concern', 'series', 'significant', 'similar', 'hot', 'language', 'each', 'usually', 'response', 'dead', 'rise', 'animal', 'factor', 'decade', 'article', 'shoot', 'east', 'save', 'seven', 'artist', 'away', 'scene', 'stock', 'career', 'despite', 'central', 'eight', 'thus', 'treatment', 'beyond', 'happy', 'exactly', 'protect', 'approach', 'lie', 'size', 'dog', 'fund', 'serious', 'occur', 'ready', 'sign', 'thought', 'list', 'individual', 'simple', 'quality', 'pressure', 'accept', 'answer', 'hard', 'resource', 'identify', 'left', 'meeting', 'determine', 'prepare', 'disease', 'whatever', 'success', 'argue', 'cup', 'particularly', 'amount', 'ability', 'staff', 'recognize', 'indicate', 'character', 'growth', 'loss', 'degree', 'wonder', 'attack', 'region', 'television', 'box', 'TV', 'training', 'pretty', 'trade', 'deal', 'election', 'physical', 'lay', 'general', 'feeling', 'standard', 'bill', 'message', 'fail', 'outside', 'arrive', 'analysis', 'benefit', 'name', 'sex', 'forward', 'lawyer', 'present', 'section', 'environmental', 'glass', 'answer', 'skill', 'sister', 'PM', 'professor', 'operation', 'financial', 'crime', 'stage', 'ok', 'compare', 'authority', 'miss', 'design', 'sort', 'one', 'act', 'ten', 'knowledge', 'gun', 'station', 'blue', 'state', 'strategy', 'little', 'clearly', 'discuss', 'indeed', 'force', 'truth', 'song', 'example', 'democratic', 'check', 'environment', 'leg', 'dark', 'public', 'various', 'rather', 'laugh', 'guess', 'executive', 'set', 'study', 'prove', 'hang', 'entire', 'rock', 'design', 'enough', 'forget', 'claim', 'note', 'remove', 'manager', 'help', 'close', 'sound', 'enjoy', 'network', 'legal', 'religious', 'cold', 'form', 'final', 'main', 'science', 'green', 'memory', 'card', 'above', 'seat', 'cell', 'establish', 'nice', 'trial', 'expert', 'spring', 'firm', 'Democrat', 'radio', 'visit', 'management', 'care', 'avoid', 'imagine', 'tonight', 'huge', 'ball', 'no', 'close', 'finish', 'talk', 'theory', 'impact', 'respond', 'statement', 'maintain', 'charge', 'popular', 'traditional', 'reveal', 'direction', 'weapon', 'employee', 'cultural', 'contain', 'peace', 'head', 'control', 'base', 'pain', 
'apply', 'play', 'measure', 'wide', 'shake', 'fly', 'interview', 'manage', 'chair', 'fish', 'particular', 'camera', 'structure', 'politics', 'perform', 'bit', 'weight', 'suddenly', 'discover', 'candidate', 'top', 'production', 'treat', 'trip', 'evening', 'affect', 'inside', 'conference', 'unit', 'best', 'style', 'adult', 'worry', 'range', 'mention', 'rather', 'far', 'deep', 'past', 'edge', 'individual', 'specific', 'writer', 'trouble', 'necessary', 'throughout', 'challenge', 'fear', 'shoulder', 'institution', 'middle', 'sea', 'dream', 'bar', 'beautiful', 'property', 'instead', 'improve', 'stuff']


engine = pyttsx3.init()

urlLipsync = 'http://127.0.0.1:8090/?transcription='
urlTimedRecsn = 'http://127.0.0.1:8090/timed/recsn'
urlPhones = 'http://127.0.0.1:8090/phones'
urlRecsn = 'http://127.0.0.1:8080/api/v2/en-GB/ipa/recsn'

#################
# Borrowed Code #
#################
async def find_recsn_entries_v2( phones: list ):
    ipa = list( map( lambda phone: phone[2], phones ) )
    r = requests.post(urlRecsn, data={'source': ' '.join(ipa)})
    recsn = json.loads( r.text )
    if( len(recsn) != len(phones) ):
      pass
      #print(f'Error: recsn not the same length as source phones list: {phones}, {recsn}')
    for i, entry in enumerate(recsn):
        entry['start'] = phones[i][0]
        entry['stop'] = phones[i][1]
    return recsn
#################
# Borrowed Code #
#################

async def callTimedRscn():
  counter = 0
  lipsyncJsonAndTranscription = getLipsyncResponseDataAndTranscription()
  for transcription, json in lipsyncJsonAndTranscription:
    dirName = transcription

    # if (counter == 10):
    #   break
    counter += 1

    if (checkIfResponsesExist(f'{dataFolder}/{dirName}', 'T') == True):
      print(f'Response for TimedRcsn already exists... Skipping to the next call.')
      continue

    phones = await getPhones(json, transcription)
    if (phones != None):
      recsn = await find_recsn_entries_v2(phones.json())
      response = requests.post(f'{urlTimedRecsn}?transcription={transcription}&lipsync={json}&recsn={recsn}')
      os.chdir(f'{dataFolder}/{dirName}')
      await saveResponse(response.content, 'timedRescnRespone.json')
      # print(f'\nCode - {response.status_code} : Content - {response.json()}')
    else:
      continue 

def getLipsyncResponseDataAndTranscription():
  dataTuples = []
  dirsInData = os.listdir(dataFolder)
  for dir in dirsInData:
    dirName = os.path.basename(f'{dataFolder}/{dir}')
    files = os.listdir(f'{dataFolder}/{dir}')
    for file in files:
      if (file == 'response.json'):
        with open(f'{dataFolder}/{dir}/{file}', 'r', encoding="utf8") as f:
          dataTuples.append((dirName, f.read()))

  return dataTuples

async def getPhones(lipsyncJson, transcription):
  try:
    response = requests.post(f'{urlPhones}?transcription={transcription}&lipsync={lipsyncJson}')
    if (response.status_code == 200):
        return response
    else:
      return None
  except Exception as e:
    errors.append(f'Error happening during getPhones call : Code: {response.status_code} : Error {e}')

async def callLipsyncService(transcription, filePath, fileName):
  with open(filePath, 'rb') as f:
    response = requests.post(f'{urlLipsync}{transcription}', files={fileName: f})
    f.close()
  return response

def checkIfResponsesExist(path, idetifier):
  exists = False
  files = os.listdir(path)

  for file in files:
    if (idetifier == 'L'):
      if (file == "response.json"):
        exists = True
        return exists
    elif(idetifier == 'T'):
      if (file == 'timedRescnRespone.json'):
        exists = True
        return exists

async def saveResponse(response, fileName):
  with open(fileName, 'wb') as f:
    f.write(response)
    f.close()

async def prepCallToLipsyncService():
  counter = 0
  try:
    for folder in os.listdir(f'{basePath}/data'):
      singleDirFiles = await getLabAndWavFilesInFolder(folder)
      dotLabFile = None
      dotWavFile = None

      # if (counter == 10):
      #   break

      if (checkIfResponsesExist(f'{dataFolder}/{folder}', 'L') == True):
        print(f'Response already exists... Skipping to next directory.')
        continue

      for file in singleDirFiles:
        if (os.path.splitext(file)[1] == ".lab"):
          dotLabFile = file
        elif (os.path.splitext(file)[1] == ".wav"):
          dotWavFile = file
          dotWavFileABSPath = os.path.abspath(dotWavFile)

        with open(f'{basePath}/data/{folder}/{dotLabFile}') as f:
          transcription = f.read()
          f.close

        if (dotLabFile != None and dotWavFile != None):
          print('Calling Lipsync service... In Progress. DO NOT END THIS')
          response = await callLipsyncService(transcription, dotWavFileABSPath, dotWavFile)
          if (response.status_code == 200):
            await saveResponse(response.content, 'response.json')
            counter += 1
            print(f'Response was revieced and saved. Word Count: {counter} - Word Completed: {dotLabFile}\n')
          else:
            print(f'No Response. Error was logged and will be shown at the end of the process.')
            errors.append(f'Response from Lipsync Service was empty. StatusCode: {response.status_code} - Transcription: {transcription} - {os.path.dirname(dotWavFileABSPath)} - {dotWavFile}')
  except Exception as e:
    errors.append(f'Error comes from (prepCallToLipsyncService) - {e}')

async def convertWavFileProperties():
  dataDir = f'{basePath}/data'
  allDirsInData = os.listdir(dataDir)

  for dir in allDirsInData:
    filesInDataDir = os.listdir(f'{dataDir}/{dir}')
    for file in filesInDataDir:
      if (file.endswith('.wav')):
        currentFilePath = os.path.dirname(os.path.abspath(file))
        currentFileName = os.path.splitext(file)[0]
        data, sr = librosa.load(f'{dataDir}/{currentFileName}/{currentFileName}.wav', sr=16000)
        sf.write(f'{dataDir}/{currentFileName}/{currentFileName}.wav', data=data, samplerate=sr)

async def getLabAndWavFilesInFolder(folderName):
  files = []
  folderPath = f'{basePath}/data/{folderName}'
  os.chdir(f'{folderPath}')

  folderFiles = os.listdir(f'{folderPath}')

  for file in folderFiles:
    fileName = os.path.splitext(file)[0]
    fileExtension = os.path.splitext(file)[1]

    if (fileExtension == '.lab' or fileExtension == '.wav'):
      if (os.path.isfile(f'{fileName}.lab') and os.path.isfile(f'{fileName}.wav')):
        files.append(file)
        #print(f'  File --> {file}')
      elif not (os.path.isfile(f'{fileName}.lab')):
        errors.append(f'Missing file: {fileName}.lab - Check: {folderPath}')
        continue
      elif not (os.path.isfile(f'{fileName}.wav')):
        errors.append(f'Missing file: {fileName}.wav - Check: {folderPath}')
        continue
      else:
        errors.append(f'Missing files check: {folderPath} --> You Should Never See This!!!')
        continue

  return files

async def createAndSaveAsFile(fileName):
  if not (os.path.exists(f'{basePath}/data/{fileName}')):
    os.mkdir(fileName)

  os.chdir(f'{basePath}/data/{fileName}')

  with open(f'{fileName}.lab', 'w') as f:
    f.write(fileName)
    f.close

  engine.save_to_file(fileName, f'{fileName}.wav')
  engine.runAndWait()

#Comment out if statement for counter to enable full words amount 25000+
async def loopAllWordsAndCreateFiles():
  counter = 0
  for word in word_list:
    # if (counter == 10):
    #   break

    counter += 1

    if (os.path.exists(f'{dataFolder}/{word}')):
      print(f'These files already exist... skipping to the next word')
      continue

    try:
      os.chdir(f'{basePath}/data')
    except Exception as e:
      errors.append(f'Directory Change Error: {e}')

    try:
      await createAndSaveAsFile(word)
    except Exception as e:
      errors.append(f'CreatingAndSaving file error: {e}')

#Uncomment the response line to send requests.
async def main():
  startTime = time.time()
  global errors
  errors = []

  print('\nProccess started\nCreating neccessary files...\n')

  try:
    if not (os.path.exists(f'{basePath}/data')):
      os.mkdir('data')

    await loopAllWordsAndCreateFiles()
  except Exception as e:
    errors.append(f'Global Erros: {e}')

  try:
    await convertWavFileProperties()
  except Exception as e:
    errors.append(f'Something went wrong with convertWavFileProperties - {e}')

  try:
    await prepCallToLipsyncService()
  except Exception as e:
    errors.append(f'Something went wrong with prepCallToLipsyncService - {e}')

  try:
    await callTimedRscn()
  except Exception as e:
    errors.append(f'Something went wrong with callTimedRcsn in Main() - {e}')

  print(f'\nFinished all proccesses.\nExisted with {len(errors)} Errors.')
  endTime = (time.time() - startTime) / 60 
  print(f'\nProcess took: {endTime} minutes.')

  if not (len(errors) == 0):
    for error in errors:
      print(f'\nError --> {error}')

if __name__ == '__main__':
  asyncio.run(main())
  #print(len(word_list))
  # r = asyncio.run(callTimedRscn())
  # print(r)