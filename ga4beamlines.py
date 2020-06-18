#!/usr/bin/env python 3

print("Imported!")

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

#################### CLASS DEFINITIONS ####################
########## ERROR CLASSES ##########

class BeamlineError(Exception):
    '''This is the base class for exeptions in this module'''
    pass

class MethodError(BeamlineError):
    '''Exception raised for errors in methods to use'''

    def __init__(self, message):
        '''

        '''
        super().__init__(message)

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
        self.generation = 1
        self.sSel = self._VerifySurvivorMode(survivorMode)
        self.pSel = self._VerifyParentMode(parentMode)
        self.cxMode = self._VerifyCXMode(cxMode)


    #################### HELPER FUNCTIONS ####################

    def _VerifySurvivorMode(self, survivorMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for sSel.

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
            raise MethodError(message = f"{survivorMode['name']} is not a valid method for Survivor Selection")

        return tmpDict

    def _VerifyParentMode(self, parentMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for pSel.

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
                    tmpDict["s"] = parentMode['s']
                else:
                    tmpDict["s"] = dictn["s"]

                break

        if not valid:
            raise MethodError(message = f"{parentMode['name']} is not a valid method for Parent Selection")

        return tmpDict

    def _VerifyCXMode(self, cxMode):
        '''
        # Purpose:
            Ensure that valid values have been passed in for cxMode.

        # Parameters:
            # cxMode        : Recombination method (name: simple,single or whole) and parameters (kwargs: alpha)
        '''
        valid = False
        tmpDict = {}

        for dictn in cxMode:
            if dictn["name"] == cxMode["name"]:
                valid = True
                tmpDict["name"] = cxMode["name"]

                if "alpha" in cxMode:
                    if 0.0 <= cxMode["alpha"] or cxMode["alpha"] <= 1.0:
                        tmpDict["alpha"] = cxMode['alpha']
                    else:
                        #NOT SURE WHAT SHOULD HAPPEN IN THE EVENT OF AN INVALID ALPHA VALUE
                        pass
                else:
                    tmpDict["alpha"] = dictn["alpha"]

                break

        if not valid:
            raise MethodError(message = f"{cxMode['name']} is not a valid method for Recombination")

        return tmpDict
