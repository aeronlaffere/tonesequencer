import random

def generate_sequence(length=3):
    is_triple = True # flag for looping until a sequence with at least 2 different tones is generated
    while is_triple:
        sequence = []
        sequence.append(random.choice([0,1,2]))
        sequence.append(random.choice([0,1,2]))
        sequence.append(random.choice([0,1,2]))
        if sequence[0] != sequence[1] or sequence[1] != sequence[2]:
            is_triple = False
    return(sequence)

def similar_contours(first_sequence, second_sequence):
    if ((first_sequence[0] - first_sequence[1] < 0 and second_sequence[0] - second_sequence[1] < 0) or (first_sequence[0] - first_sequence[1] > 0 and second_sequence[0] - second_sequence[1] > 0) or (first_sequence[0] - first_sequence[1] == 0 and second_sequence[0] - second_sequence[1] == 0)) and ((first_sequence[1] - first_sequence[2] < 0 and second_sequence[1] - second_sequence[2] < 0) or (first_sequence[1] - first_sequence[2] > 0 and second_sequence[1] - second_sequence[2] > 0) or (first_sequence[1] - first_sequence[2] == 0 and second_sequence[1] - second_sequence[2] == 0)):
        similar = True
    else:
        similar = False 
    return(similar)

def generate_raw_trials(n=35, n_reps=5, n_similar_contours=0):

    reps_counter = 0
    reps_probability = n_reps / n
    while reps_counter != n_reps: # generate fresh sets of trials until one has the right number of repetitions
        random.seed()
        reps_counter = 0
        target_trials = []
        targets = []
        sequence = generate_sequence()
        target_trials.append(sequence)
        just_repeated = False
        for i in range(1,n):
            if just_repeated: # there has just been a repetition so don't roll the dice
                sequence = generate_sequence()
                while similar_contours(sequence, target_trials[i-1]): # keep generating new sequences until there is one which isn't a repeat of the previous trial
                    sequence = generate_sequence()
                just_repeated = False
            else:
                if random.choices([True,False], weights=[reps_probability,1-reps_probability])[0]:
                    just_repeated = True
                    reps_counter += 1
                    # no need to generate a sequence here because we're carrying over the sequence from the last trial
                    targets.append(i) # append index of target in series to list of targets
                else:
                    sequence = generate_sequence()
                    while similar_contours(sequence, target_trials[i-1]):
                        sequence = generate_sequence()
                    just_repeated = False
            target_trials.append(sequence)
    # end target trials

    keep_going = True

    while keep_going: # generate fresh sets of trials until one has the right number of similar contours
        random.seed()
        contour_counter = 0
        reps_counter = 0
        reps_probability = 0
        distractor_trials = []
        distractors = []

        sequence = generate_sequence()
        if similar_contours(sequence, target_trials[i]):
                contour_counter += 1
        distractor_trials.append(sequence)
        just_repeated = False

        for i in range(1,n):
            if just_repeated:
                sequence = generate_sequence()
                while similar_contours(sequence, distractor_trials[i-1]):
                    sequence = generate_sequence()
                just_repeated = False
            else:
                if random.choices([True,False], weights=[reps_probability,1-reps_probability])[0]:
                    just_repeated = True
                    reps_counter += 1
                    # no need to generate a sequence here because we're carrying over the sequence from the last trial
                    distractors.append(i) # append index of target in series to list of targets
                else:
                    sequence = generate_sequence()
                    while similar_contours(sequence, distractor_trials[i-1]):
                        sequence = generate_sequence()
                    just_repeated = False
            if similar_contours(sequence, target_trials[i]):
                contour_counter += 1
            distractor_trials.append(sequence)
        
        if contour_counter == n_similar_contours and reps_counter == 0:
            keep_going = False
    return(target_trials, distractor_trials, targets, distractors)
