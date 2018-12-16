import random
# Copywrite James Kayes © 2018
# Genes represent an action for each agent to take for each of the possible states that the agent can be in.

def rank_based_selection(population):
    rank_proportions = [0.15, 0.1, 0.09, 0.85, 0.08, 0.07, 0.06, 0.05, 0.03, 0.025, 0.02, 0.0175, 0.015, 0.0125, 0.01]
    remaining_probability = 1.0 - sum(rank_proportions)
    remaining_items = float(len(population) - len(rank_proportions))
    # Applying this same probability to all values ranked lower than the number of items in the rank_proportions list:
    lower_rank_prob = remaining_probability/remaining_items
    for value in population[10:]:
        rank_proportions.append(lower_rank_prob)

    # Get a random rank from the genes acording to the rank_proportions distribution above:
    random_value = random.random()
    total = 0.0
    for rank_index in range(len(rank_proportions)):
        total += rank_proportions[rank_index] # Probability of choosing this rank
        if(random_value <= total): # Select this rank for breeding.
            return rank_index

    return (len(rank_proportions)-1) # Last element

def crossover(a_genes, b_genes):
    result = []
    # Uniform crossover with randomization such that each gene has an 50% chance of coming from either parent:
    for gene_index in range(len(a_genes)):
        if(random.random() > 0.5):
            result.append(a_genes[gene_index])
        else:
            result.append(b_genes[gene_index])
    return result

def mutate(genes, rate=0.025, max_gene=9):
    for gene_index in range(len(genes)):
        if(random.random() <= rate):
            genes[gene_index] = random.randint(0, max_gene)
    return genes