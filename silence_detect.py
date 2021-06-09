# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:55:40 2019
@author: Parisa

This program receives a list of raw audio recordings and distinguishes the 
voice and silent segments in each of them. It then buils an audio clip by 
appending a recording (i.e.\ country_name)  with another one (i.e. capital_name) 
by padding a brief artifical silent segment in between. It repeast this sequence 
once more, appends to other silent segments at the begining and at the end, and 
finally stores the result into an audio clip. 


Parisa Supitayakul
2021-06-09

"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
import glob
import os

MIN_SILENCE_LEN = 100 # the minimum length for any silent section (msec)
SILENCE_THRESH = -70 # the upper bound for how quiet is silent (dFBS)

if __name__ = = '__main__':
    
    # If an output repository does not exist, then create a new one
    savepath = r'./test5/' 
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    # Open the text file with all list of country-capital pairs
    file_name = 'country-capital.txt'
    file = open(file_name, 'r', encoding = 'utf-8-sig')
    
    # Create a dictionary variable for storing all list of coutry-capital pairs
    country_list = dict() 
    
    """
    Create synthetic silence audio for padding before, after and between the 
    voice segments（e.g. 300 msec and 200 msec duration periods)
    """
    silence_sound_300ms = AudioSegment.silent(duration = 300)
    silence_sound_between_200ms = AudioSegment.silent(duration = 200)
    
    """
    Read the country name and capital name from the txt file and store them 
    in the dictionary
    """
    for line in file:
        country = line.split('\t')[0]
        capital = line.split('\t')[1].replace('\n', '')
        country_list[country] = capital
        

    for filepath in glob.glob('test/country/*'):
        
        # Get file path
        name_country_path = filepath.split('\\')[1]
        name_capital_path = country_list.get(name_country_path.split('.')[0])

        # Read wav file from filepath and store it in a variable
        rec_sound_country = AudioSegment.from_wav('test/'+name_country_path)
        rec_sound_capital = AudioSegment.from_wav('test/capital/'+name_capital_path+'.wav')
        print(rec_sound_country.dBFS)
        print(rec_sound_capital.dBFS)
        
        """
        Split the voice by using SILENCE_THRESH and store it into a list:
            E.g. [silence, voice, silence, voice, ...] -> [voice, voice, ...]
            
        If a certain period is "quiet enough" (determined based on SILENCE_THRESH)
        for more than MIN_SILENCE_LEN, then this period is considered to "silence"
        and discarded
        """
        voice_country = split_on_silence(rec_sound_country, MIN_SILENCE_LEN, SILENCE_THRESH)
        voice_capital = split_on_silence(rec_sound_capital, MIN_SILENCE_LEN, SILENCE_THRESH)
        
        """
        Build a sequence of voice segments and silent paddings:
            E.g. silence300ms + country name_audio + silence200ms + capital_name_audio  * 2 times
         """
        audio_result = \
        silence_sound_300ms + voice_country[0] + \
        silence_sound_between_200ms + voice_capital[0] + \
        silence_sound_300ms + voice_country[0] + \
        silence_sound_between_200ms + voice_capital[0]
        
        """
        Export the sequence of audio  (i.e. referred to as audio clip in the 
        article) into output repository
        """
        audio_result.export(savepath + '/' + name_country_path, bitrate = "192k", format = "wav")
    
