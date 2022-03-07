# Displaying visual stimuli and recording audio

This repository contains the custom codes and resources for building the audio stimuli used in the experiments reported in our article. The implementation is done in Python 3.5.2 and it deploys several functions from the package pydub 0.25.1.

We created two main routines: (i) for displaying the image stimuli to the "speaker" and recording his voice and (ii) for post-processing the raw recordings to detect silent segments, unify them and create audio clips to be used in e-learning experiments.

**Displaying image stimuli and recording speaker's voice**

The program show_and_record_cound.py displays visual stimuli (images) involving text or numbers to a person (i.e. "speaker") and records his/her voice into an audio clip, while he/she reads aloud the visual stimuli.

The speaker is notified with a brief beep sound at the beginning of each image, which is displayed for a time window of 4 seconds. After the notification, audio recordings starts and goes on until the end of the time window. As the time window is finished, an audio clip is saved. Subsequently, the current image is flushed and the next image (e.g. a word or number) is displayed. The outputs of the program are (i) an audio clip for each image and (ii) the 
list of words/numbers appearing on the images stored in a text file. 

**Post-processing of raw audio recordings**

The program silence_detect.py receives a list of raw audio recordings and distinguishes the voice and silent segments in each of them. It then builds an audio clip by appending a recording (i.e. country_name) with another one (i.e. capital_name) by padding a brief artificial silent segment in between. It repeats this sequence 
once more, appends to other silent segments at the beginning and at the end, and finally stores the result into an audio clip. 
