
from cc3d import CompuCellSetup
        

from AVS_ModelSteppables import AVS_ModelSteppable

CompuCellSetup.register_steppable(steppable=AVS_ModelSteppable(frequency=1))


CompuCellSetup.run()
