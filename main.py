from scipy.io.wavfile import write

import sequence_generation as seqgen
import tone_generation as tonegen
import numpy as np

Fs = 44100                          # integer   | samples per second
tone_duration = 1/6                 # float     | duration of one tone in seconds

spectral_conditions = ['high', 'low']
separation_conditions = ['8va', '16va']
synchrony_conditions = ['synchronous', 'interleaved']
similar_contour_conditions = [0, 11] # number of similar contours, 11 is roughly 30% of trials

def generate_stimulus(target_band='high', lowest_tone=185, separation='8va', synchrony='interleaved', n_similar_contours=0, Fs=Fs, tone_duration=tone_duration, training_volume=0, simple_tones=False, training=False):
    target_trials, distractor_trials, targets, distractors = seqgen.generate_raw_trials(n_similar_contours=n_similar_contours)
    waveform = tonegen.generate_tone_sequence(distractor_trials, target_trials, separation=separation, synchrony=synchrony, training=training, training_volume=training_volume, target_band=target_band) if target_band == 'high' else tonegen.generate_tone_sequence(target_trials, distractor_trials, separation=separation, synchrony=synchrony, training=training, training_volume=training_volume, target_band=target_band)
    target_list = zip([x*(8*tone_duration)-4*tone_duration+8*tone_duration for x in targets],[x*(8*tone_duration)+4*tone_duration+8*tone_duration for x in targets])
    target_output = ''
    for a, b in target_list:
        a = a
        b = b
        target_output += '{0},{1}\n'.format(a, b)
    target_output = target_output[:-1]
    # TODO add a click using np.ones() to one channel of wav file

    # print('{0},{1},{2},{3}'.format(target_band, separation, synchrony, n_similar_contours) + str([int(np.floor(x*8*tone_duration*1000)) for x in targets]))

    distractor_list = zip([x*(8*tone_duration)-4*tone_duration+8*tone_duration for x in distractors],[x*(8*tone_duration)+4*tone_duration+8*tone_duration for x in distractors])
    distractor_output = ''
    for a, b in distractor_list:
        a = a
        b = b
        distractor_output += '{0},{1}\n'.format(a, b)
    distractor_output = distractor_output[:-1]

    json_target_list = list([int(np.floor(x*8*tone_duration*1000)) for x in targets])
    json_distractor_list = list([int(np.floor(x*8*tone_duration*1000)) for x in distractors])
    json_output = '{\n\t\"targetData\":' + str(json_target_list).replace(' ', '') + ',\n\t\"distractorData\":' + str(json_distractor_list).replace(' ', '') + '\n}'
    
    
    return(waveform, target_output, distractor_output, json_output)


# for i in spectral_conditions:
#     for j in separation_conditions:
#         for k in synchrony_conditions:
#             for l in similar_contour_conditions:
#                 stimulus, targets, distractors, json = generate_stimulus(target_band=i, separation=j, synchrony=k, n_similar_contours=l)
#                 write('output/' + i + '_' + j + '_' + k + '_contours' + str(l) + '_stream.wav', Fs, stimulus)
#                 f = open('output/' + i + '_' + j + '_' + k + '_contours' + str(l) + "_targets.txt", "w")
#                 f.write(targets)
#                 f.close()
#                 f = open('output/' + i + '_' + j + '_' + k + '_contours' + str(l) + "_distractors.txt", "w")
#                 f.write(distractors)
#                 f.close()
#                 f = open('output/' + i + '_' + j + '_' + k + '_contours' + str(l) + ".json", "w")
#                 f.write(json)
#                 f.close()

for i in spectral_conditions:
    for j in range(20):
        stimulus, targets, distractors, json = generate_stimulus(target_band=i)
        write('output/lori/' + i + '_' + str(j+1) + '.wav', Fs, stimulus)
        f = open('output/lori/' + i + '_' + str(j+1) + ".json", "w")
        f.write(json)
        f.close()

# for i in spectral_conditions:
#     counter = 0
#     for m in [0, 0.2, 0.6]:
#         counter += 1
#         stimulus, targets = generate_stimulus(target_band=i, training=True, training_volume=m)
#         write('training/' + i + str(counter) + '_stream.wav', Fs, stimulus)
#         f = open('training/' + i + str(counter) + '_targets.txt', "w")
#         f.write(targets)
#         f.close()