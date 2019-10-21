import os
import reframe as rfm
import reframe.utility.sanity as sn

class IGABaseTestCPU(rfm.RegressionTest):
    def __init__(self):
        super().__init__()

        ## Compilation phase 

        self.descr = "IGA CPU benchmark"
        self.valid_systems = ['intelinx:remote-nompi']
        self.valid_prog_environs = ['Prg-gnu']

        #Source Directory 
        self.prebuild_cmd = ['git clone https://github.com/gismo/gismo',
                            'cd gismo',
                            'mkdir build',
                            'cd build',
                            'cmake .. -DGISMO_WITH_OPENMP=ON'
                            'make poisson2_example'
                            ]

        self.build_system = 'Make'
        self.build_system.options = ['poisson2_example']
        self.build_system.max_concurrency = 12
        self.build_system.flags_from_environ = False

        self.executable = 'bin/poisson2_example'

        self.time_limit = (2,0,0)

        self.sanity_patterns = sn.all([
			sn.assert_found(r'Done', self.stdout)])

		#self.perf_patterns = {
		#	'perf': sn.extractsingle(r'Performance:\s+(?P<perf>\S+)', self.stderr, 'perf', float)
		#}

        #self.reference = {
		#	'intelinx:remote': {
		#		'perf': (1.079, -1.0,1.0, 'ns/day')}
		#}

    def setup(self, partition, environ, **job_opts):

    	super().setup(partition, environ, **job_opts)

@rfm.simple_test
class IGATestPoisson(IGABaseTestCPU):
	def __init__(self):
		super().__init__()

		self.executable_opts = ['-r 8 -e 19']

	def setup(self, partition, environ, **job_opts):

		self.variables['OMP_NUM_THREADS'] = str(12)       
		self.variables['OMP_PROC_BIND'] = 'true'
		super().setup(partition, environ, **job_opts)