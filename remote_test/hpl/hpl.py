import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class hpltest(rfm.RegressionTest):
    def __init__(self):
        super().__init__()

        self.name = 'HPL'
        self.descr = 'High Performance LinPack for CPUs'
        self.valid_systems = ['epydia','intelinx:remote']
        self.valid_prog_environs = ['Prg-gnu']


        #self.prebuild = ['git clone https://github.com/xianyi/OpenBLAS.git']
        self.prebuild_cmd = ['echo $EBROOTOPENMPI',
                             'wget http://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz',
                             'tar -xvf hpl-2.3.tar.gz',
                             'cp Make.gcc hpl-2.3/',
                             'cd hpl-2.3',
                             'sed -i "/TOPdir       =/c TOPdir       = $PWD" Make.gcc']

        self.build_system = 'Make'
        self.build_system.max_concurrency = 1
        self.build_system.options = ['arch=gcc']
        self.build_system.flags_from_environ = False


        self.executable = 'hpl-2.3/bin/gcc/xhpl'
        self.time_limit = (1,0,0)

        self.sanity_patterns = sn.assert_found(r'Gflops',self.stdout)
        self.perf_patterns = {
			'perf': sn.extractsingle(r'Gflops\n\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(?P<perf>\S+)',self.stdout, 'perf', float )
		}

        self.reference = {
			'cartesius:normal-haswell': {
				'perf': (650, -0.25, 0.25,'GFLOPs/s'),
			},
            'intelinx:remote': {
                'perf': (470, -0.5,0.5,'GFLOPs/s')
                }
		}
		
    def setup(self, partition, environ, **job_opts):
        self.num_tasks = 12
        self.variables['OMP_NUM_THREADS'] = str(1)
        super().setup(partition, environ, **job_opts)
