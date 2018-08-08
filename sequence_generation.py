import random

def generate_sequence(length=3):

    sequence = []

    is_triple = True # assume that the current sequence is three of the same notes

    while is_triple:

        sequence = []

        sequence.append(random.choice([0,1,2]))
        sequence.append(random.choice([0,1,2]))
        sequence.append(random.choice([0,1,2]))

        # if we can demonstrate that we don't have three identical notes then the loop is broken out of
        if sequence[0] != sequence[1] or sequence[1] != sequence[2]:
            is_triple = False

    return(sequence)

def similar_contours(first_sequence, second_sequence):

    similar = bool()

    if ((first_sequence[0] - first_sequence[1] < 0 and second_sequence[0] - second_sequence[1] < 0) or (first_sequence[0] - first_sequence[1] > 0 and second_sequence[0] - second_sequence[1] > 0) or (first_sequence[0] - first_sequence[1] == 0 and second_sequence[0] - second_sequence[1] == 0)) and ((first_sequence[1] - first_sequence[2] < 0 and second_sequence[1] - second_sequence[2] < 0) or (first_sequence[1] - first_sequence[2] > 0 and second_sequence[1] - second_sequence[2] > 0) or (first_sequence[1] - first_sequence[2] == 0 and second_sequence[1] - second_sequence[2] == 0)):
        similar = True
    else:
        similar = False 

    return(similar)

def repetition(first_sequence, second_sequence):

    repetition = bool()

    if first_sequence == second_sequence:
        repetition = True
    else:
        repetition = False

    return(repetition)

def generate_single_band(n_repetitions=5, n=35):

    repetition_counter = int()
    repetition_probability = n_repetitions / n

    # repeatedly generate blocks of n trials until one has the desired number of repetitions
    while repetition_counter != n_repetitions:

        random.seed()

        repetition_counter = int()

        trials = list()
        repetitions = list()

        just_repeated = False

        # generate the first sequence of this block and add it to the sequence list
        sequence = generate_sequence()
        trials.append(sequence)

        # now generate all of the subsequent sequences
        for i in range(1,n):

            # if there has just been a repetition there should not be another one
            if just_repeated:

                sequence = generate_sequence()

                # keep generating sequences until there is one which is not a repetition
                while repetition(sequence, trials[i-1]):
                    sequence = generate_sequence()

                just_repeated = False

            else:
                if random.choices([True,False], weights=[repetition_probability, 1-repetition_probability])[0]:
                    
                    repetition_counter += 1
                    just_repeated = True

                    # add the index of this sequence to the list of repetitions
                    repetitions.append(i)
                else:

                    sequence = generate_sequence()

                    while repetition(sequence, trials[i-1]):
                        sequence = generate_sequence()
                    
                    just_repeated = False
                
            # append the sequence to the list of trials
            trials.append(sequence)
    
    return(trials, repetitions)