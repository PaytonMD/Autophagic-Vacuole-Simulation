
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
            
        self.plot_win2 = self.add_new_plot_window(
            title='Average energy change by function',
            x_axis_title='Monte Carlo Step (MCS)',
            y_axis_title='Avg. Energy',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True)

        self.plot_win2.add_plot("VolAcc", style='Dots', color='green', size=5)
        self.plot_win2.add_plot("AdhAcc", style='Dots', color='red', size=5)
        self.plot_win2.add_plot("TotAcc", style='Dots', color='blue', size=5)
        self.plot_win2.add_plot("VolRej", style='Lines', color='green', size=5)
        self.plot_win2.add_plot("AdhRej", style='Lines', color='red', size=5)
        self.plot_win2.add_plot("TotRej", style='Lines', color='blue', size=5)
    def step(self,mcs):
        """
        type here the code that will run every frequency MCS
        :param mcs: current Monte Carlo step
        """

        cell_volu = 0
        for cell in self.cell_list:
            cell_volu += cell.volume

        cell_volu /= len(self.cell_list)

        for cell in self.cell_list:

            print("cell.id=",cell.id)
            print(" | Volume=",cell.volume)
        
        vol_list_acc = []
        adh_list_acc = []
        tot_list_acc = []
        vol_list_rej = []
        adh_list_rej = []
        tot_list_rej = []
        
        vol_mean_acc = 0
        adh_mean_acc = 0
        tot_mean_acc = 0
        vol_mean_rej = 0
        adh_mean_rej = 0
        tot_mean_rej = 0
        
        num_flips = 0
        
        for flip_result, energy_calculations in self.get_energy_calculations():
            num_flips += 1
            
            vol_e = energy_calculations['Volume']
            adh_e = energy_calculations['Contact']
            tot_e = vol_e + adh_e
            if flip_result:
                vol_list_acc.append(vol_e)
                adh_list_acc.append(adh_e)
                tot_list_acc.append(tot_e)
                
                vol_mean_acc += vol_e
                adh_mean_acc += adh_e
                tot_mean_acc += tot_e
            else:
                vol_list_rej.append(vol_e)
                adh_list_rej.append(adh_e)
                tot_list_rej.append(tot_e)
                
                vol_mean_rej += vol_e
                adh_mean_rej += adh_e
                tot_mean_rej += tot_e
        
        if num_flips == 0:
            return
        
        self.plot_win2.add_data_point('VolAcc', mcs, vol_mean_acc/num_flips)
        self.plot_win2.add_data_point('AdhAcc', mcs, adh_mean_acc/num_flips)
        self.plot_win2.add_data_point('TotAcc', mcs, tot_mean_acc/num_flips)
        self.plot_win2.add_data_point('VolRej', mcs, vol_mean_rej/num_flips)
        self.plot_win2.add_data_point('AdhRej', mcs, adh_mean_rej/num_flips)
        self.plot_win2.add_data_point('TotRej', mcs, tot_mean_rej/num_flips)

    def finish(self):
        """
        Finish Function is called after the last MCS
        """


        