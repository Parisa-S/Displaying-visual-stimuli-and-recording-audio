# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:55:40 2019

@author: Parisa

This program is 






"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob
import os

if __name__ == '__main__':
    
    #if output repository is not exist then create new repository
    savepath = r'./test5/' 
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    #open file which store the all list of country-capital pair
    file_name = 'country-capital.txt'
    file = open(file_name,'r', encoding='utf-8-sig')
    
    country_list = dict() # dictionary for storing all list of coutry and capital
    
    #read the country name and capital name from txt file and convert to python dictionary
    for line in file:
        country = line.split('\t')[0]
        capital = line.split('\t')[1].replace('\n','')
        country_list[country] = capital
        

    for filepath in glob.glob('test/country/*'):
        #get file paths
        name_country_path = filepath.split('\\')[1]
        name_capital_path = country_list.get(name_country_path.split('.')[0])

        #read wav file from exist path and store in variables
        rec_sound_country = AudioSegment.from_wav('test/'+name_country_path)
        rec_sound_capital = AudioSegment.from_wav('test/capital/'+name_capital_path+'.wav')
        print(rec_sound_country.dBFS)
        print(rec_sound_capital.dBFS)
        
        #split the voice by using silence thresh, the result return into a list of voices
        #ex. silience,voice,silience,voice.. -> [voice,voice,...]
        #min_silience_len -> if it become silence more than one sec,it will considered to be silience  
        #silence_thresh - (in dBFS) anything quieter than this will be considered silence.
        voice_country = split_on_silence(rec_sound_country,min_silence_len = 100,silence_thresh=-70)
        voice_capital = split_on_silence(rec_sound_capital,min_silence_len = 100,silence_thresh=-70)
        
        #create synthetic silence audio （e.g.300 ms and 200 ms duration periods  )
        silence_sound_300ms = AudioSegment.silent(duration=300)
        silence_sound_between_200ms = AudioSegment.silent(duration=200)
        
        #combined each part of audio together (audio clips and silence parts)
        #e.g. silence300ms +country name audio clip + silence200ms + capital name audio clip for 2 times
        audio_result = silence_sound_300ms + voice_country[0] + silence_sound_between_200ms + voice_capital[0]+silence_sound_300ms+voice_country[0] + silence_sound_between_200ms + voice_capital[0]
        
        #export the modified audio into output repository
        audio_result.export(savepath+'/'+name_country_path,bitrate = "192k",format="wav")
    

