#import os

import reframe as rfm
import reframe.utility.sanity as sn


#@rfm.parameterized_test([1000000], [80000000])

@rfm.parameterized_test([80000000],[1000000],[4000000])
class StreamTest(rfm.RegressionTest):
	def __init__(self, array_size):
		super().__init__()
		self.name = 'stream-{}'.format(array_size)
		self.descr = 'STREAM Benchmark - Array={}'.format(array_size)
		self.exclusive_access = True

		self.valid_systems = ['epydia:remote-nompi','intelinx:remote-nompi']
		self.valid_prog_environs = ['Prg-gnu']

		self.sourcepath = 'stream.c'
		self.build_system = 'SingleSource'
		self.prgenv_flags = {
			'Prg-gnu': [' -fopenmp -O3 -DSTREAM_ARRAY_SIZE={}'.format(array_size)],
			'PrgEnv-eb-Intel': [' -openmp -O2 -DSTREAM_ARRAY_SIZE={}'.format(array_size)]
		}

		self.num_tasks = 1
		self.num_tasks_per_node = 1
		self.stream_cpus_per_task = {
			'epydia:remote-nompi': 24,
			'intelinx:remote-nompi':24
		}

		self.variables = {
			'OMP_PLACES': 'threads',
			'OMP_PROC_BIND': 'spread',
		}

		self.sanity_patterns = sn.assert_found(r'Solution Validates: avg error less than', self.stdout)
		self.perf_patterns = {
			'triad': sn.extractsingle(r'Triad:\s+(?P<triad>\S+)\s+\S+',
					self.stdout, 'triad', float)
		}
		self.stream_bw_reference = {
			'eb-foss': {
				'cartesius:broadwell': {'triad': (109000.0, -1, 1,'GB/s')},
				'cartesius:normal-haswell': {'triad': (109000.0, -1, 1,'GB/s')},
				'*': {'triad': (0.0, None, None, 'GB/s')}
			},
			'PrgEnv-eb-Intel': {
				'cartesius:broadwell': {'triad': (109000.0, -1, 1,'GB/s')},
				'cartesius:normal-haswell': {'triad': (109000.0, -1, 1,'GB/s')},
				'*': {'triad': (0.0, None, None, 'GB/s')}
			},
			'Prg-gnu' : {
				'intelinx:remote-nompi' : {'triad' : (124440,-1.0,1.0,'GB/s')},
				'*' : {'triad':(0.0,None,None,'GB/s')}
			}
		}

	def setup(self, partition, environ, **job_opts):
		self.num_cpus_per_task = self.stream_cpus_per_task[partition.fullname]
		self.reference = self.stream_bw_reference[environ.name]

		self.variables['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
		self.build_system.cflags = self.prgenv_flags[environ.name]

		super().setup(partition, environ, **job_opts)


