import random


def rank_based_selection(population):
    rank_proportions = [0.35, 0.2, 0.1, 0.08, 0.05, 0.04, 0.03, 0.025, 0.015, 0.01]
    remaining_probability = 1.0 - sum(rank_proportions)
    remaining_items = float(len(population) - len(rank_proportions))
    print(round(sum(rank_proportions), 2))
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

def crossover(a_genes, b_genes):
    result = []
    layer_num = 0
    for layer_genes in a_genes:
        result.append([])
        gene_num = 0
        for a_gene in layer_genes:
            if(random.random() > 0.5):
                result[layer_num].append(a_gene)
            else:
                result[layer_num].append(b_genes[layer_num][gene_num])
            gene_num += 1
        layer_num += 1
    return result

def mutate(genes, rate=0.01):
    for layer_indx in range(len(genes)):
        for gene_indx in range(len(genes[layer_indx])):
            if(random.random() <= rate):
                genes[layer_indx][gene_indx] = (random.randint(0, layer_indx), random.randint(0, len(genes[0])-1))
    return genes