import requests
import nltk
import pyttsx3
import os
import asyncio
from nltk.corpus import words

#Uncomment this if you're running for first time.
#nltk.download('words')

basePath = os.path.dirname(os.path.abspath(__file__))

word_list = words.words()

engine = pyttsx3.init()

urlLipsync = 'http://127.0.0.1:8090/?transcription='
urlTimedRecsn = 'http://127.0.0.1:8090/timed/recsn?transcription='

async def callTimedRecsnService(transcript, lipsyncjson):
  return await requests.post(f'{urlTimedRecsn}{transcript}', lipsyncjson)

async def callLipsyncService(transcription, filePath, fileName):
  with open(filePath, 'rb') as f:
    response = await requests.post(f'{urlLipsync}{transcription}', files={fileName: f})
    f.close()
  return response

async def saveResponse(response):
  with open(f'{response}', 'w') as f:
    f.write(response)
    f.close()
  print(response)

async def prepCallToLipsyncService():
  try:
    for folder in os.listdir(f'{basePath}/data'):
      singleDirFiles = await getAllFilesInFolder(folder)
      dotLabFile = None
      dotWavFile = None

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
          print('Calling Lipsync service...')
          response = await callLipsyncService(transcription, dotWavFileABSPath, dotWavFile)
          if (response != None):
            await saveResponse(response)
            print(f'Response was revieced and saved.\n')
          else:
            print(f'No Response. Error was logged and will be shown at the end of the process.')
            errors.append(f'Response from Lipsync Service was empty. Transcription: {transcription} - {os.path.dirname(dotWavFileABSPath)} - {dotWavFile}')
  except Exception as e:
    errors.append(f'Error comes from (prepCallToLipsyncService) - {e}')

async def getAllFilesInFolder(folderName):
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
    if (counter >= 10):
      break

    counter += 1
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
  global errors
  errors = []

  print('Proccess started... \nCreating neccessary files...\n')

  try:
    if not (os.path.exists(f'{basePath}/data')):
      os.mkdir('data')

    await loopAllWordsAndCreateFiles()
  except Exception as e:
    errors.append(f'Global Erros: {e}')

  try:
    await prepCallToLipsyncService()
  except Exception as e:
    errors.append(f'Something went wrong with prepCallToLipsyncService - {e}')

  print(f'\nFinished all proccesses.\nExisted with {len(errors)} Errors.')

  if not (len(errors) == 0):
    for error in errors:
      print(f'\nError --> {error}')

if __name__ == '__main__':
  asyncio.run(main())
