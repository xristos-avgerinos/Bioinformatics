import numpy as np

emissions = ['A', 'G', 'T', 'C']
states = ['a', 'b']

# initial probabilities
initial_prob = [0.5, 0.5]

# Transition matrix
# [[p(a|a), p(b|a)],
#  [p(a|b), p(b|b)]]
transition_prob = [[0.9, 0.1],
                   [0.1, 0.9]]

# Emission matrix
# [[p(A|a), p(A|b)],
#  [p(G|a), p(G|b)],
#  [p(T|a), p(T|b)],
#  [p(C|a), p(C|b)]]
emission_prob = [[0.4, 0.2],
                 [0.4, 0.2],
                 [0.1, 0.3],
                 [0.1, 0.3]]

# Observable state
observation = 'GGCT'


def viterbi(observation, emissions, states, A, B, Pi):
    '''
    Implementation of Viterbi algorithm so as to find the best path of observation state sequence for the specific Hidden Markov Model.
    :param observation:  Observation state sequence.
    :param emissions: All the emissions.
    :param states: All the states.
    :param A: State transition matrix.
    :param B: Emission matrix.
    :param Pi: Initial state probabilities.
    :return: a matrix with the max scores of each step and the parallel matrix with the previous state of each step
    '''
    # Holds the max score of each step
    max_scores = []

    # A parallel matrix to 'max_scores' that holds the previous state of each step(for a,b states)
    max_scores_previous_states = []

    for i in range(len(observation)):
        # an auxiliary list holding the max score of each state for each step
        temp_scores = []

        if i == 0:
            # Initialize tracking table from initial probabilities of first observation
            temp_scores.append(Pi[0] + B[emissions.index(observation[i])][0])
            temp_scores.append(Pi[1] + B[emissions.index(observation[i])][1])
            previous1 = None
            previous2 = None
        else: # Iterate through the observations updating the tracking table

            # tmp1 and tmp2 are the scores that come from each arrow(route) taking into account the previous state as well as the next state
            tmp1 = A[states.index('a')][0] + B[emissions.index(observation[i])][0] + \
                   max_scores[i - 1][0]
            tmp2 = A[states.index('b')][0] + B[emissions.index(observation[i])][0] + \
                   max_scores[i - 1][1]

            # calculate max of the 2 arrows(routes)
            max_score = tmp1
            previous1 = 'a'
            if tmp2 > max_score:
                max_score = tmp2
                previous1 = 'b'
            temp_scores.append(max_score)

            tmp1 = A[states.index('a')][1] + B[emissions.index(observation[i])][1] + \
                   max_scores[i - 1][0]
            tmp2 = A[states.index('b')][1] + B[emissions.index(observation[i])][1] + \
                   max_scores[i - 1][1]
            max_score = tmp1
            previous2 = 'a'
            if tmp2 > max_score:
                max_score = tmp2
                previous2 = 'b'
            temp_scores.append(max_score)

        max_scores.append([temp_scores[0], temp_scores[1]]) # adding the max scores for each state to 'max_scores'  matrix
        max_scores_previous_states.append([previous1, previous2])# keeping the previous state of each state

    return max_scores, max_scores_previous_states


if __name__ == '__main__':

    # Transform probability matrices to log-scores so as to avoid underflow situations
    transition_prob_log = np.log2(transition_prob)
    emission_prob_log = np.log2(emission_prob)
    initial_prob_log = np.log2(initial_prob)

    max_scores, max_scores_previous_states = viterbi(observation, emissions,states,transition_prob_log,emission_prob_log,initial_prob_log)

    # finding the max probability and its state(best state)
    hidden_state = []
    max_prob = max(max_scores[-1])
    best_state = max_scores_previous_states[-1][max_scores[-1].index(max_prob)]

    hidden_state.append(best_state)
    previous = best_state

    # Follow the backtrack till the first observation so as to find the final hidden states(best path os obsevation sequence)
    for i in range(len(max_scores_previous_states) - 2, -1, -1):
        hidden_state.insert(0, max_scores_previous_states[i + 1][states.index(previous)])
        previous = max_scores_previous_states[i + 1][states.index(previous)]

    for st in states:
        print(st + ": " + " ".join(
            ("%lf " % v[states.index(st)]) + "(previous state:%s)     " % s[states.index(st)] for v, s in zip(max_scores, max_scores_previous_states)))

    print("\nThe best path for the sequence", observation, "is: " + " ".join(hidden_state) + " with highest probability "
                                                                                           "of %s" % max_prob)
