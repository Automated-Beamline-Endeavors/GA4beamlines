#!/usr/bin/env python 3

print("Imported!")

import pandas as pd
import random
import numpy as np
import ackley

#################### VARIABLES AND CONSTANTS DEFINITIONS ####################
#Valid survivor selection methods
sMode =     [{"name": "age", "nElite": 0},
             {"name": "genitor"}]
#Valid parent selection methods
pMode =     [{"name": "probRank", "s": 1.5},
             {"name": "probFit"}]
#Valid child generation methods
cxMode =    [{"name": "single", "alpha": 0.5},
             {"name": "simple", "alpha": 0.75},
             {"name": "whole", "alpha": 0.75}]
#Valid mutation methods
mMode =     [{"name": "uniform"},
             {"name": "gaussian"},
             {"name": "cauchy"}]

fMode =     [{"type": "Func", "name": ackley.AckleyFunc}]

#################### CLASS DEFINITIONS ####################
########## ERROR CLASSES ##########

class BeamlineError(Exception):
    '''This is the base class for exeptions in this module'''
    pass

class MethodError(BeamlineError):
    '''Exception raised for errors in methods to use'''

    def __init__(self, message):
        super().__init__(message)

########## GA CLASSES ##########

class GA4Beamline:
    def __init__(self, motors, survivorMode, parentMode, cxMode, mutationMode,
                    fitness, nPop = 10, initPop = None, OM = False):
        '''
        # motors        : An array of dictionaries –each motor has upper limit, lower limit, name (PV name for epics motors), sigma
        # survivorMode  : Survivor selection method (name: Age, progRank, probFit) and parameters (nElite optional)
        # parentMode    : Parent selection method (name: Fitness) and parameters (alpha)
        # cxMode        : Recombination method (name: simple,single or whole) and parameters (kwargs: alpha)
        # mutationMode  : Mutation method (name: uniform, nonuniform) and parameters (kwargs: Pm);
                            For nonuniform Pm =1; for uniform Pm set to ~0.05 and applied gene-wise
        # fitness       : How to measure fitness type is either ‘PV’ or ‘Func’ and name is the either the PV or function name to be used
        # nPop          : Number of individuals in population
        # initPop       : Initial population; if None, will create one
        # OM            : Turn on Observer Mode –only set to True when using against epics motors/fitness function
        '''

        self.motors = motors
        self.generation = 0
        self.sSel = self._VerifySurvivorMode(survivorMode)
        self.pSel = self._VerifyParentMode(parentMode)
        self.cxMode = self._VerifyCXMode(cxMode)
        self.mMode = self._VerifyMMode(mutationMode)
        self.obsMode = OM
        self.fitness = fitness

        self.nPop = nPop

        if initPop == None:
            self.population = self.CreatePop()

        #self.parents = pd.DataFrame()
        self.parents = []
        self.children = pd.DataFrame(self._MakeDataFrameCat())
        self.fitHistory = pd.DataFrame(self._MakeDataFrameCat())

        #print(f"children is:\n{self.children}\n")
        #print(f"fitHistory is:\n{self.fitHistory}\n")

    def CreatePop(self):
        #NOTE: still need to see if population is set up correctly
        categories = {}

        for motor in self.motors:
            categories[motor["name"]] = []

            for i in range(self.nPop):
                categories[motor["name"]].append(random.uniform(motor["lo"], motor["hi"]))

        categories["fitness"] = np.zeros(self.nPop)
        categories["ranking"] = [0] * self.nPop
        categories["probability"] = np.zeros(self.nPop)

        population = pd.DataFrame(categories)

        #print(population)

        return population

    def SurvivorSel(self):
        #NOTE: WILL FINISH LATER.  Need to verify functionality.
        tmp = None

        print("In survivor selection!")

        #if nElite > 0: get to ranked individuals into new population
        #For remainder just looking for nPop-nElite individuals

        if self.generation == 0:
            self.generation += 1
        else:
            self.generation += 1

            if self.sSel["name"] == "age":
                if self.sSel["nElite"] > 0:
                    #NOTE: NEED TO CHANGE SO THAT THE HIGHEST RANKED nELITE INDIVIDUALS GET CARRIED OVER
                    self.population = self.population.iloc[0:self.sSel["nElite"], :]
                    print(f"Copied eldest.  public is:\n{self.population}")

                self.population = pd.concat([self.population, self.children])
                #self.RankPop()
                print(f"Combined old and new.  public is:\n{self.population}")

            elif self.sSel["name"] == "genitor":
                self.population = pd.concat([self.population, self.children])

                #Use rankPop to set rank column of population + children
                self.RankPop()
                #self.population = top nPop of population + children
                self.population = self.population.iloc[0:self.nPop, :]

    def ParentSel(self):
        #NOTE: Need to verify functionality

        self.RankPop()

        if self.pSel["name"] == "probRank":
            #Use rankPop to set rank column
            #use calcProb("rank") to set probability column
            self.CalcProb("rank")

        elif self.pSel["name"] == "probFit":
            #use calcProb("fitness") to set probability column
            self.CalcProb("fitness")

        #With probabilities set, create parent sets (lists of indexes to population?) using stochastic universal sampling (fig. 5.2 from Eiben & Smith 2 ed)
        self.parents = self.StochasticUnivSampling(numParents = self.nPop - self.sSel["nElite"])
        #List of parents should have nPop - nElite parents
        #Set self.parents/returns parents

    def StochasticUnivSampling(self, numParents):
        print("\nInside StochasticUnivSampling\n")

        cmlProb = self.population["probability"].cumsum().tolist()
        parents = []

        #print(cmlProb)

        currMember = i = 1
        r = random.uniform(0, 1 / numParents)

        #print(f"r is: {r}")

        while currMember <= numParents:
            while r <= cmlProb[i]:
                parents.append(i)
                r += 1 / numParents
                currMember += 1

            i += 1

        print(f"The parents are:\n{parents}")
        return parents


    def Recombine(self):
        #NOTE: Need to verify functionality.  ALSO, NEED TO ADJUST HOW MANY CHILDREN ARE GENERATED

        #Need to create pairs of individuals from self.parents
        pairs = self.CreatePairs(self.parents)

        '''
        for p in range(len(pairs)):
            self.children.iloc[p:p + 2, :] = self.Recombination(pairs[p], self.cxMode)
        '''
        for p in range(len(pairs)):
            self.children = pd.concat([self.children, self.Recombination(pairs[p], self.cxMode)], ignore_index = True)
            #print([self.children, self.Recombination(pairs[p], self.cxMode)])
        print(f"\nchildren is:\n{self.children}")

    def CreatePairs(self, parents):
        print("\nIn CreatePairs\n")
        pairs = []

        for i in range(len(parents)):
            pairs.append(random.choices(parents, k = 2))

        print(f"The pairs are:\n{pairs}")

        return pairs

    def Recombination(self, parents, mode):
        #NOTE: Need to verify functionality
        #print("\nInside Recombination\n")
        #print(f"mode is:{mode}")

        #Create 2 children from pair of parents
        alpha = mode["alpha"]
        parent1 = self.population.iloc[parents[0], :].tolist()
        parent2 = self.population.iloc[parents[1], :].tolist()
        child1 = None
        child2 = None

        #print(f"parent1 is: {parent1}\nparent2 is: {parent2}\n")

        #pick a random allele (k)
        #NOTE: DOING THIS SINCE THE MOTORS ARE THE FIRST COLUMNS IN THE POPULATION DATATABLE.  IF THIS IS CHANGED,
        #       THEN THE METHOD TO GENERATE K NEEDS TO CHANGE.
        k = int(random.choice(range(len(self.motors))))
        #print(f"k is: {k}")

        if mode["name"] == "single":
            child1 = parent1[0:k]
            child1.append(parent1[k] * (1.0 - alpha) + parent2[k] * alpha)
            child1 = child1 + parent1[k + 1:]

            child2 = parent2[0:k]
            child2.append(parent2[k] * (1.0 - alpha) + parent1[k] * alpha)
            child2 = child2 + parent2[k + 1:]

        elif mode["name"] == "simple":
            child1 = parent1[0:k]
            child1 = child1 + np.add(np.multiply(parent1[k:], 1 - alpha), np.multiply(parent2[k:], alpha)).tolist()

            child2 = parent2[0:k]
            child2 = child2 + np.add(np.multiply(parent2[k:], 1 - alpha), np.multiply(parent1[k:], alpha)).tolist()

        elif mode["name"] == "whole":
            child1 = np.add(np.multiply(parent1, 1 - alpha), np.multiply(parent2, alpha)).tolist()

            child2 = np.add(np.multiply(parent2, 1 - alpha), np.multiply(parent1, alpha)).tolist()

        #print(child1)

        tmp = self._MakeDataFrameCat()
        i = 0

        for column in tmp:
            tmp[column].append(child1[i])
            tmp[column].append(child2[i])
            i += 1

        tmp = pd.DataFrame(tmp)
        #print(f"\ntmp is:\n{tmp}")

        return tmp


    def Mutate(self):
        #NOTE: WILL FINISH LATER

        #NOT SURE IF THIS WILL WORK WITH CHILDREN MEANT TO BE A DATAFRAME.  NEED TO LOOK INTO FURTHER
        #self.children ==[self.mutation(child, self.motors, self.mMode["name"]) for child in self.children]

        pass

    def Mutation(self, child, motors, mode):
        #NOTE: WILL FINISH LATER

        mutatedValue = []

        for i, gene in enumerate(child["HOWEVER WE'RE REFERRING TO MOTORS"]):
            if mode == "nonuniform":
                mutatedValue.append("random pick from gaussian centered on gene.value, with stdev of motor[j]['sigma']")
                # to ensure that we are within the limits of the motor scipy.stats has a function truncnorm that should be
                #   useful here so that we don’t have a pileup at the edges
            elif mode == "uniform":
                mutatedValue.append("random pick from uniform distribution with range of motor")

        return mutatedValue

    def FitnessFunc(self, pop):
        #NOTE: WILL FINISH LATER
        tmpFit = []

        if self.fitness["type"] == "epics":
            pass
            '''
            will implement code later but it would look like the following:

            for p in population: # does for loop create unattached copy of range values?
                move motors to p[motor] values
                if not OM:
                    wait for motor move to complete
                else:# implement Observer mode

                 p[‘fitness’] = read fitness[‘pv’]
            '''
        elif self.fitness["type"] == "Func":
            for row in pop.index:
                tmpFit.append(self.fitness["name"](pop.loc[row,:].tolist()))

            #print(f"tmpFit is:\n{tmpFit}")
            pop["fitness"] = tmpFit
            #print(f"\npopulation is:\n{self.population}")

        #returns population but with the fitness values filled in

    def RankPop(self):
        #NOTE: Need to verify functionality

        #Set the ranking column of the self.population dataframe (1 being the highest for descending = True)
        self.population = self.population.sort_values(by = ["fitness"], ascending = False)
        self.population["ranking"] = [i for i in range(len(self.population.index) - 1, -1, -1)]
        self.population.index = [i for i in range(len(self.population.index))]
        #print(self.population)

    def CalcProb(self, probMode):
        #NOTE: WILL FINISH LATER.  Need to implement "rank"
        probs = []

        #Set the probability column in the self.population dataframe
        if probMode == "rank":
            #Loop through population and set probability using RankingProb
            for row in self.population.index:
                probs.append(self.RankingProb(self.population.loc[row, "ranking"], self.nPop, self.pSel['s']))

        elif probMode == "fitness":
            #Get sum of Fitness
            cmltFitness = self.population["fitness"].sum()
            #Loop through population and set probability column to individual fitness/cumulative fitness
            for row in self.population.index:
                probs.append(self.population.loc[row, "fitness"] / cmltFitness)

        #print(f"probs sum is: {np.sum(probs)}")

        self.population["probability"] = probs
        #print(self.population)


    def RankingProb(self, rank, nPop, s):
        #NOTE: Need to verify functionality.
        return (2 - s) / nPop + 2 * rank * (s - 1) / nPop / (nPop - 1)

    def Measure(self, childrenOnly = True):
        #NOTE: Need to verify functionality

        #SINCE FITNESSFUNC IS SUPPOSED TO RETURN A MODIFIED POPULATION, I SHOULD PROBABLY SET SOMETHING EQUAL TO THESE
        if childrenOnly:
            self.FitnessFunc(self.children)
        else:
            self.FitnessFunc(self.population)

    #################### HELPER FUNCTIONS ####################

    def _VerifySurvivorMode(self, survivorMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for determining the survivor selection method.

        # Parameters:
            # survivorMode  : Survivor selection method (name: Age, progRank, probFit) and parameters (nElite optional)
        '''
        valid = False
        tmpDict = {}

        for dictn in sMode:
            if dictn["name"] == survivorMode["name"]:
                valid = True
                tmpDict["name"] = survivorMode["name"]

                if "nElite" in survivorMode and survivorMode["nElite"] >= 0:
                    tmpDict["nElite"] = survivorMode['nElite']
                else:
                    tmpDict["nElite"] = 0

                break

        if not valid:
            raise MethodError(message = f"{survivorMode['name']} is not a valid method for Survivor Selection.")

        return tmpDict

    def _VerifyParentMode(self, parentMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for determining the parent selection method.

        # Parameters:
            # parentMode    : Parent selection method (name: Fitness) and parameters (alpha)
        '''
        valid = False
        tmpDict = {}

        for dictn in pMode:
            if dictn["name"] == parentMode["name"]:
                valid = True
                tmpDict["name"] = parentMode["name"]

                #NOT SURE IF THERE SHOULD BE ANY CHECKS ON THE VALUE OF "S" OR WHAT SHOULD HAPPEN IF IT ISN'T DEFINED
                if "s" in parentMode:
                    if 1.0 < parentMode['s'] and parentMode['s'] <= 2.0:
                        tmpDict['s'] = parentMode['s']
                    else:
                        raise ValueError(f"{parentMode['s']} is not a valid 's' value")
                else:
                    tmpDict['s'] = dictn['s']

                break

        if not valid:
            raise MethodError(message = f"{parentMode['name']} is not a valid method for Parent Selection.")

        return tmpDict

    def _VerifyCXMode(self, childMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for determining the recombination method.

        # Parameters:
            # cxMode        : Recombination method (name: simple,single or whole) and parameters (kwargs: alpha)
        '''
        valid = False
        tmpDict = {}

        for dictn in cxMode:
            if dictn["name"] == childMode["name"]:
                valid = True
                tmpDict["name"] = childMode["name"]

                if "alpha" in childMode:
                    if 0.0 <= childMode["alpha"] and childMode["alpha"] <= 1.0:
                        tmpDict["alpha"] = childMode['alpha']
                    else:
                        raise ValueError(f"{childMode['alpha']} is not a valid 'alpha' value.")
                else:
                    tmpDict["alpha"] = dictn["alpha"]

                break

        if not valid:
            raise MethodError(message = f"{childMode['name']} is not a valid method for Recombination.")

        return tmpDict

    def _VerifyMMode(self, mutationMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for determining the mutation method.

        # Parameters:
            # cxMode        : Recombination method (name: simple,single or whole) and parameters (kwargs: alpha)
        '''
        valid = False
        tmpDict = {}

        for dictn in mMode:
            if dictn["name"] == mutationMode["name"]:
                valid = True
                tmpDict["name"] = mutationMode["name"]

                break

        if not valid:
            raise MethodError(message = f"{mutationMode['name']} is not a valid method for Mutation.")

        return tmpDict

    def _MakeDataFrameCat(self):
        categories = {}

        for motor in self.motors:
            categories[motor["name"]] = []

        categories["fitness"] = []
        categories["ranking"] = []
        categories["probability"] = []

        #tmp = pd.DataFrame(categories)

        return categories
