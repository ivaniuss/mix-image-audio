import json
import os
from posixpath import split
from random import sample
from tempfile import tempdir
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip



def main():
  #obtain layers in a specific format
  getLayers = True
  mixSamples= True
  mixVideos = True

  #if you have the layers with the correspondent samples assign in the next variable
  mixMetadataWithSamplesDict = {}

  samplesNames = []


#save samples into samples directory
  for sample_name in os.listdir('./samples'):
    if not sample_name.startswith('.'):
      samplesNames.append(sample_name)
  # print(samplesNames)


#get layers to connect with samples
  if getLayers == True:
    counter = 0
    for layer_name in os.listdir('./layers'):
      if not layer_name.startswith('.'):
        tempDict = {}
        for trait_name in os.listdir(f'./layers/{layer_name}'):
          if not trait_name.startswith('.'):
            splitted_name = ''
            if "#" in trait_name:
              splitted_name = trait_name.split("#")[0]
            else:
              splitted_name = trait_name.split(".png")[0]
            #the next line is for testing purposes only  
            tempDict[splitted_name] = samplesNames[counter]
            #uncomment the next line to get only layers
            #tempDict[splitted_name] = ""
            counter = counter+1
        mixMetadataWithSamplesDict[layer_name] = tempDict
    counter = 0  
    # print(json.dumps(mixMetadataWithSamplesDict))


  if mixSamples == True:
    #mixing audio with trait_types
    metadataCollectionFile = open("./build/json/_metadata.json", "r")
    metadataCollection = json.load(metadataCollectionFile)

    samplesToMix = []

    for nft in metadataCollection:
      samples = []
      for attribute in nft["attributes"]:
        samples.append(mixMetadataWithSamplesDict[attribute['trait_type']][attribute['value']])
      samplesToMix.append({"id":nft['name'].split("#")[1],"samples":samples})

    # print(json.dumps(samplesToMix))


    for samples in samplesToMix:
      combinedSample = ""
      for sampleIndex in range(len(samples["samples"])):
        if(sampleIndex == 0):
          combinedSample = AudioSegment.from_wav(f"./samples/{samples['samples'][0]}")
          print(f"mixed {samples['id']}: {sampleIndex}")
        else:
          sampleToCombine = AudioSegment.from_wav(f"./samples/{samples['samples'][sampleIndex]}")
          combinedSample = combinedSample.overlay(sampleToCombine)
          print(f"mixed {samples['id']}: {sampleIndex-1} with {sampleIndex}")
      combinedSample.export(f"./build/samples/{samples['id']}.wav", format='wav')


  if mixVideos == True:
  #creation of the video
    for imageIndex in range(len(os.listdir('./build/images'))):
      print(os.listdir('./build/images')[imageIndex])
      audio_clip = AudioFileClip(f"./build/samples/{imageIndex}.wav")
      image_clip = ImageClip(f"./build/images/{imageIndex}.png")
      video_clip = image_clip.set_audio(audio_clip)
      video_clip.duration = 10
      video_clip.fps = 1
      video_clip.write_videofile(f"./build/videos/{imageIndex}.mp4")

if __name__ == "__main__":
  main()
