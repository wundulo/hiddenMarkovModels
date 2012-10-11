import sys

# mock data for test conditioning
transition = {
    'S1' : {'S1':0.333333333333333333333333333, 
            'S2':0.333333333333333333333333333, 
            'S3':0.333333333333333333333333333},
    'S2' : {'S1':0.333333333333333333333333333, 
            'S2':0.333333333333333333333333333, 
            'S3':0.333333333333333333333333333},
    'S3' : {'S1':0.333333333333333333333333333, 
            'S2':0.333333333333333333333333333, 
            'S3':0.333333333333333333333333333}
}

emission = {
    'S1' : {'a':0.25, 'c':0.25, 't':0.25, 'g':0.25},
    'S2' : {'a':0.25, 'c':0.25, 't':0.25, 'g':0.25},
    'S3' : {'a':0.25, 'c':0.25, 't':0.25, 'g':0.25}
}

inital_prob = {
    'S1' : 0.333333333333333333333333333,
    'S2' : 0.333333333333333333333333333,
    'S3' : 0.333333333333333333333333333
}

# hw5 data
states = ['S1', 'S2', 'S3']

inital_prob = { 'S1' : 0.25, 'S2' : 0.5, 'S3' : 0.25 }
prior_prob = { 'S1' : 1.0, 'S2' : 1.0, 'S3' : 1.0 }
curr_prob = { 'S1' : 1.0, 'S2' : 1.0, 'S3' : 1.0 }

transition = {
    'S1' : {'S1':0.4, 'S2':0.5, 'S3':0.1},
    'S2' : {'S1':0.1, 'S2':0.4, 'S3':0.5},
    'S3' : {'S1':0.3, 'S2':0.3, 'S3':0.4}
}

emission = {
    'S1' : {'a':0.4, 'c':0.4, 't':0.1, 'g':0.1},
    'S2' : {'a':0.25, 'c':0.25, 't':0.25, 'g':0.25},
    'S3' : {'a':0.1, 'c':0.1, 't':0.4, 'g':0.4}
}

def forward_algorithm(sequence, normalize=False):
    
    # initial round
    first_nucleotide = sequence[0]
    for state in states:
        prior_prob[state] = inital_prob[state] * emission[state][first_nucleotide]
        
        # tune value for normalization
        if normalize is True: 
            prior_prob[state]*=len(emission[state])
    
    # from 2 to n
    for nucleotide in sequence[1:]:
        
        # update current probability
        for state in states:    
            prior_sum = sum(prior_prob[from_state] * transition[from_state][state] for from_state in states)
            curr_prob[state] = prior_sum * emission[state][nucleotide]
            
            # tune value for normalization
            if normalize is True: 
                curr_prob[state]*=len(emission[state])
            
        # update prior probability
        for state in states:    
            prior_prob[state] = curr_prob[state]
    
    # sum of final nucleotide
    total_prob = sum(curr_prob[state] for state in states)
    return total_prob

def main(): 
    
    # default parameters
    sequence = 'aatcgtcgaa'
    normalized = True
    
    print
    if len(sys.argv)>1 and sys.argv[1] is not None:
        sequence = sys.argv[1]
        print "Calculating sequence =",sequence
    else:
        print "To specify sequence, use: $ python hiddenMarkovModels.py {sequence composed of a,c,t,g}"
        print "Default sequence for calculation =",sequence
    
    score = forward_algorithm(sequence, normalized)
    if normalized is True:
        print "Normalized score =",score
    else:
        print "Raw score =",score

if __name__ == '__main__':
    main()