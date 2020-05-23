import random
import matplotlib.pyplot as plt


class Algo:
    def __init__(self):
        pass

    # initialize chromosomes with random value
    def set_list(self, length, population):
        self.chromosome = [str(bin(random.randint(0, 2**length-1)))[2:]
                           for j in range(population)]
        for index, string in enumerate(self.chromosome):
            l = len(string)
            if l < length:
                self.chromosome[index] = "0" * (length-l) + string

    # sort by the chromosome having highest fitness value
    def sorter(self, x):
        return int(x, 2)

    # take random point and crossover two strings until new chromosome set is created
    def crossover(self, length, population):
        selection = self.chromosome = sorted(
            self.chromosome, key=self.sorter, reverse=True)
        self.chromosome = []
        while len(self.chromosome) < population:
            old1 = selection[0]
            old2 = selection[1]
            crossover_range = length//4
            crossover_point = random.randint(
                crossover_range, length - crossover_range - 1)
            new1 = old1[:crossover_point] + old2[crossover_point:]
            new2 = old2[:crossover_point] + old1[crossover_point:]
            new1 = self.mutate(new1)
            new2 = self.mutate(new2)
            self.chromosome.append(new1)
            self.chromosome.append(new2)
            selection.pop(0)

    # select random index from string and flip that bit
    def mutate(self, string):
        r_no = random.randint(0, len(string)-1)
        character = '1' if string[r_no] == '0' else '0'
        string = string[:r_no] + character + string[r_no+1:]
        return string

    # compute generations needed for answer
    def solve(self, length, population):
        generation = 0
        self.set_list(length, population)

        # keep computing crossover until all bits are '1' in any chromosome
        while '1'*length not in self.chromosome:
            generation += 1
            self.crossover(length, population)
        return generation


if __name__ == "__main__":

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(
        'Effect of Population and Length on Generation Count', fontweight='bold')
    ax1.set_xlabel('Population', fontweight='bold')
    ax1.set_ylabel('No. of Generations', fontweight='bold')
    ax2.set_xlabel('Length', fontweight='bold')

    algo = Algo()

    # variable population when bit_length = 8 (constant)
    bit_length = 8
    populations = [i for i in range(4, 11)]
    generations = []
    for population in populations:
        generations.append(algo.solve(bit_length, population))
    print("\nVariable Population:".upper())
    print("Bit Length:  ", bit_length)
    print("Populations: ", populations)
    print("Generations: ", generations)
    ax1.plot(populations, generations, color='b', marker='.')

    # variable bit_length when population = 8 (constant)
    population = 8
    bit_lengths = [i for i in range(8, 22, 2)]
    generations = []
    for bit_length in bit_lengths:
        generations.append(algo.solve(bit_length, population))
    print("\nVariable Bit Length:".upper())
    print("Population:  ", population)
    print("Bit Lengths: ", bit_lengths)
    print("Generations: ", generations)
    ax2.plot(bit_lengths, generations, color='r', marker='.')

    plt.show()
