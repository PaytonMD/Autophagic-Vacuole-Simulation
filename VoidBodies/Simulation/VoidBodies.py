
from cc3d import CompuCellSetup
        

from VoidBodiesSteppables import VoidBodiesSteppable

CompuCellSetup.register_steppable(steppable=VoidBodiesSteppable(frequency=1))


CompuCellSetup.run()
