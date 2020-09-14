
from cc3d.core.PySteppables import *

class WallTest2Steppable(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        any code in the start function runs before MCS=0
        """
        #Code for setting target volumes to initial volumes.
        #Forces cells to roughly maintain constant volume.
        for cell in self.cell_list:
            cell.targetVolume = cell.volume
            cell.lambdaVolume = 1.0

    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """

        for cell in self.cell_list:

            print("cell.id=",cell.id)
            print(" | Volume=",cell.volume)

    def finish(self):
        """
        Finish Function is called after the last MCS
        """


        