import random
from Bio import SeqIO


def move(liver_len, brain_len):
    """
    This function implements the move of each player.He can subtract 2 elements from one sequence and 1 from the
    other.The choice is partly random.
    :param liver_len: the length of the first sequence(liver)
    :param brain_len: the length of the second sequence(brain)
    :return: the updated lengths of the sequences.
    """

    # if one of the sequences' length is 1, he will necessarily subtract one element from this sequence.Otherwise, the choice is random.
    if liver_len == 1:
        removal_pick = 1
    elif brain_len == 1:
        removal_pick = 0
    else:
        removal_pick = random.randint(0, 1)

    if removal_pick == 0:
        return liver_len - 2, brain_len - 1
    else:
        return liver_len - 1, brain_len - 2


if __name__ == '__main__':

    # Load data from files
    for sequence1 in SeqIO.parse("liver.fasta", "fasta"):
        xromo_liver = sequence1.seq
    for sequence2 in SeqIO.parse("brain.fasta", "fasta"):
        xromo_brain = sequence2.seq

    # set initial lengths of each sequence
    xromo_liver_len = len(sequence1)
    xromo_brain_len = len(sequence2)

    print(" Initial lengths = liver length:", xromo_liver_len, "       brain length:", xromo_brain_len)
    player = "First Player"

    counter = 0
    while True:
        # The algorithm iterates until one length of sequence is lower than 2 and the other lower than 1
        if (xromo_liver_len >= 2 and xromo_brain_len >= 1) or (xromo_liver_len >= 1 and xromo_brain_len >= 2):
            previous_player = player  # holding the previous player for prints
            if player == "First Player":
                # First player move(randomly) and update sequences' lengths
                xromo_liver_len, xromo_brain_len = move(xromo_liver_len, xromo_brain_len)

                # change player turn
                player = "Second Player"
            else:
                # Second player move(randomly) and update sequences' lengths
                xromo_liver_len, xromo_brain_len = move(xromo_liver_len, xromo_brain_len)

                # change player turn
                player = "First Player"

            # print the first and last iterations
            if counter < 3 or counter >= 20000:
                print("\n           plays:", previous_player)
                print("\n liver length:", xromo_liver_len, "       brain length:", xromo_brain_len)
            elif counter == 3:
                print(
                    "\n                     ...\n                     ...\n                     ...\n                     ...")
            counter += 1



        else:
            # if the player in turn cannot make any move, is the winner
            print("\n     -----", player, "wins! -----")
            break
