import os
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class HPCGCheck(rfm.RegressionTest):
    def __init__(self):
        super().__init__()

        self.descr = 'HPCG reference benchmark'
        self.valid_systems = ['epydia:remote','intelinx:remote']
        self.valid_prog_environs = ['Prg-gnu']
  
        self.prebuild_cmd = ['git clone https://github.com/hpcg-benchmark/hpcg.git',
                             'cp Make.cartesius_MPI hpcg/setup/',
                             'cd hpcg']
        self.build_system = 'Make'
        self.build_system.flags_from_environ = False
        self.build_system.options = ['arch=cartesius_MPI']
        
        self.executable = 'hpcg/bin/xhpcg'
        self.executable_opts = ['--nx=104', '--ny=104', '--nz=104', '--rt=600']
        
        self.output_file = sn.getitem(sn.glob('HPCG*.txt'), 0)
        self.num_tasks = 24
        self.num_cpus_per_task = 1

        self.time_limit = (0,30,0)
        self.reference = {
            'cartesius:normal-haswell': {
                'gflops': (14, -0.1, 0.1, 'GFLOPs/s')
            },
            '*': {'gflops': (0.0, None, None, 'GFLOPs/s')}
        }

        self.maintainers = ['Sagar Dolas']
        self.tags = {'diagnostic', 'benchmark'}

        self.sanity_patterns = sn.assert_found(r'PASSED',self.output_file)
        self.perf_patterns = {
            'gflops': sn.extractsingle(
                r'HPCG result is VALID with a GFLOP\/s rating of=\s*'
                r'(?P<perf>\S+)',
                self.output_file, 'perf',  float)
        }

    def setup(self, partition, environ, **job_opts):

        super().setup(partition, environ, **job_opts)