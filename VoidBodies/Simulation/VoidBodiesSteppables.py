#import CompuCellSetup
from cc3d.core.PySteppables import *
from cc3d.cpp import CompuCell
from random import random
#from PlayerPython import * 
#import CompuCellSetup

class VoidBodiesSteppable(SteppableBasePy):

    def __init__(self,frequency=1):

        SteppableBasePy.__init__(self,frequency)
        #self.track_cell_level_scalar_attribute(field_name='COM_RATIO',attribute_name='ratio')
        #self.track_cell_level_scalar_attribute(field_name='ColorField', attribute_name='colorID')
        
        
    def start(self):
        """
        any code in the start function runs before MCS=0
        """
        
        #Code for setting target volumes to initial volumes.
        for cell in self.cell_list:
            cell.targetVolume = cell.volume
            cell.lambdaVolume = 5.0
            #cell.targetSurface = cell.surface + (cell.surface * 1.00)
            #cell.lambdaSurface = 2.0
            
        self.plot_win1 = self.add_new_plot_window(
            title='Total Energy of Model',
            x_axis_title='Monte Carlo Step (MCS)',
            y_axis_title='Total Energy',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True)
            
        self.plot_win1.add_plot("totalEnergy", style='Dots', color='red', size=5)
            
        #Coloring Code:
        
        #self.create_scalar_field_cell_level_py("ColorField")
       #field = self.field.PixelColors
        #field[:, :, :, :] = 0.0
        

        #for x in range(0, self.dim.x, 1):
         #   for y in range(0, self.dim.y, 1):
          #      for z in range(self.dim.z):
           #         field[x, y, z] = [x * random(), y * random(), z * random()]
        
        
        '''try:
            color_field = self.field.ColorField
            color_field.clear()
        except KeyError:
            self.create_scalar_field_cell_level_py("ColorField")
            color_field = self.field.ColorField
        
        for cell in self.cell_list:
            color_field[cell] = cell.id'''
        
        

    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """
        
        '''try:
            color_field = self.field.ColorField
            color_field.clear()
        except KeyError:
            self.create_scalar_field_cell_level_py("ColorField")
            color_field = self.field.ColorField'''
        
        #for cell in self.cell_list:
           #color_field[cell] = cell.id

        for cell in self.cell_list:
            print("cell.id=",cell.id)
            print("cell.id=",cell.id, " Volume=", cell.volume, " TargetVolume=", cell.targetVolume)
            #print("cell.id=",cell.id, " Surface=", cell.surface, " TargetSurface=", cell.targetSurface)
            #color_field[cell] = cell.id
            #print("Volume=", cell.volume)
            
        totEnergy = self.potts.getEnergy()
        print("Total Energy = %s" %(totEnergy))
        self.plot_win1.add_data_point('totalEnergy', mcs, totEnergy)
            

    def finish(self):
        """
        Finish Function is called after the last MCS
        """