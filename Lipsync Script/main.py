import requests
import nltk
import pyttsx3
import os
from nltk.corpus import words

#Uncomment this if you're running for first time.
#nltk.download('words')

basePath = os.path.dirname(os.path.abspath(__file__))

word_list = words.words()

engine = pyttsx3.init()

url = 'http://127.0.0.1:8090/?transcription='

def callLipsyncService(transcription, filePath, fileName):
  with open(filePath, 'rb') as f:
    response = requests.post(f'{url}{transcription}', files={fileName: f})
  return response

def getAllFilesInFolder(folderName):
  files = []
  folderPath = f'{basePath}/data/{folderName}'
  os.chdir(f'{folderPath}')

  folderFiles = os.listdir(f'{folderPath}')

  for file in folderFiles:
    fileName = os.path.splitext(file)[0]

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

def createAndSaveAsFile(fileName):
  if not (os.path.exists(f'{basePath}/data/{fileName}')):
    os.mkdir(fileName)

  os.chdir(f'{basePath}/data/{fileName}')

  with open(f'{fileName}.lab', 'w') as f:
    f.write(fileName)

  engine.save_to_file(fileName, f'{fileName}.wav')
  engine.runAndWait()

#Comment out counter to enable full words amount 25000+
def loopAllWordsAndCreateFiles():
  counter = 0
  for word in word_list:
    if (counter >= 10):
      break

    counter += 1
    try:
      os.chdir(f'{basePath}/data')
    except Exception as e:
      errors.append(f'Directory Change Error: {e}')

    try:
      createAndSaveAsFile(word)
    except Exception as e:
      errors.append(f'CreatingAndSaving file error: {e}')

#Uncomment the response line to send requests.
def run():
  global errors
  errors = []

  print('Proccess started... \nCreating neccessary files...\n')

  try:
    if not (os.path.exists(f'{basePath}/data')):
      os.mkdir('data')

    loopAllWordsAndCreateFiles()
  except Exception as e:
    errors.append(f'Global Erros: {e}')

  try:
    for folder in os.listdir(f'{basePath}/data'):
      singleDirFiles = getAllFilesInFolder(folder)
      dotLabFile = None
      dotWavFile = None

      for file in singleDirFiles:
        if (os.path.splitext(file)[1] == ".lab"):
          dotLabFile = file
        elif (os.path.splitext(file)[1] == ".wav"):
          dotWavFile = file
          if (dotWavFile != None):
            dotWavFileABSPath = os.path.abspath(dotWavFile)
          else:
            continue
      if (dotLabFile != None):
        with open(f'{basePath}/data/{folder}/{dotLabFile}') as f:
          transcription = f.read()
      else:
        continue
      if (dotLabFile != None and dotWavFile != None):
        print('I would be doing a call rn')
        #response = callLipsyncService(transcription, dotWavFileABSPath, dotWavFile)
      else:
        continue
  except Exception as e:
    errors.append(f'Getting files in a dir error: {e}')


  print(f'\nFinished all proccesses.\nExisted with {len(errors)} Errors.')

  if not (len(errors) == 0):
    for error in errors:
      print(f'\nError --> {error}')

if __name__ == '__main__':
  run()
