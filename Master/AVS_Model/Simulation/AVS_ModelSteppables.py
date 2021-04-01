from cc3d.core.PySteppables import *
from cc3d import CompuCellSetup

class AVS_ModelSteppable(SteppableBasePy):

    def __init__(self,frequency=1):

        Steppab-leBasePy.__init__(self,frequency)

    def start(self):
        """
        any code in the start function runs before MCS=0
        """
        #Codes restricts all cell volumes.
        for cell in self.cell_list:
            cell.targetVolume = cell.volume
            cell.lambdaVolume = 5.0
            
        #Sets up plot of Total Model Energy changes over time(Steps).
        self.plot_win1 = self.add_new_plot_window(
            title='Total Energy of Model',
            x_axis_title='Monte Carlo Step (MCS)',
            y_axis_title='Total Energy',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True)
            
        self.plot_win1.add_plot("totalEnergy", style='Dots', color='red', size=5)

    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """

        for cell in self.cell_list:
            print("cell.id=",cell.id)
        
        #Updates Total Energy graph with this steps current total energy.
        totEnergy = self.potts.getEnergy()
        print("Total Energy = %s" %(totEnergy))
        self.plot_win1.add_data_point('totalEnergy', mcs, totEnergy)

    def finish(self):
        """
        Finish Function is called after the last MCS
        """
        #CC3D Return code.
        #Associated with python code that calls CC3D:
        pg = ComuCellSetup.persistent_globals
        pg.return_object = 25.0
        