import os
import reframe as rfm
import reframe.utility.sanity as sn

class IGABaseTestCPU(rfm.RegressionTest):
    def __init__(self):
        super().__init__()

        ## Compilation phase 

        