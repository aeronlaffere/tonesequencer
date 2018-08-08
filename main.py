from scipy.io.wavfile import write

import sequence_generation as seqgen
import tone_generation as tonegen
import numpy as np

Fs = 44100                 
tone_duration = 1/6
n = 35
n_repetitions = 5

spectral_conditions = ['high', 'low']

def generate_stimulus(target_band='high', Fs=Fs, tone_duration=tone_duration, distractor_volume=1):
    
    target_trials, targets = seqgen.generate_single_band(n_repetitions=n_repetitions, n=n)
    distractor_trials, distractors = seqgen.generate_single_band(n_repetitions=n_repetitions, n=n)

    if target_band == 'high':
        waveform = tonegen.generate_tone_sequence(distractor_trials, target_trials, target_band)
    elif target_band == 'low':
        waveform = tonegen.generate_tone_sequence(target_trials, distractor_trials, target_band)

    target_list = list([int(np.floor(x*8*tone_duration*1000)) for x in targets])
    distractor_list = list([int(np.floor(x*8*tone_duration*1000)) for x in distractors])
    json_output = '{\n\t\"targetData\":' + str(target_list).replace(' ', '') + ',\n\t\"distractorData\":' + str(distractor_list).replace(' ', '') + '\n}'
    
    return(waveform, json_output)

n_blocks = int(input("How many blocks for each frequency? "))

for i in spectral_conditions:
    for j in range(n_blocks):
        stimulus, json = generate_stimulus(target_band=i)
        write('output/' + i + '_' + str(j+1) + '.wav', Fs, stimulus)
        f = open('output/' + i + '_' + str(j+1) + ".json", "w")
        f.write(json)
        f.close()

