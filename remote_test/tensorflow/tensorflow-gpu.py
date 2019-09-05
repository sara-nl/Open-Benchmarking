import os
import reframe as rfm
import reframe.utility.sanity as sn

class TensorFlowBaseTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        super().__init__()

        self.valid_systems = ['intelinx:remote-nompi','epydia:remote-nompi']
        self.valid_prog_environs = ['Prg-gnu']
        self.tags = {'experimental','deep-learning'}

        self.sanity_patterns = sn.assert_found(r'images/sec',self.stdout)
	
        self.perf_patterns = {
		'performance' : sn.extractsingle(r'[1][0][0]\simages\Ssec\S\s(?P<performance>\S+)',self.stdout,'performance',float)
	    } 

        self.reference = {
		    'cartesius:gpu' : {
			    'performance' : (51,-0.1,0.1,'images/second'),
		    },  
            'intelinx:remote-nompi' : {
                'performance' : (283,-0.1,0.1,'images/second'),
            }
        }

    def setup(self, partition, environ, **job_opts):
		
        super().setup(partition, environ, **job_opts)


@rfm.simple_test
class tensorflowBenchmarkResnetGPU(TensorFlowBaseTest):
    def __init__(self):
        super().__init__()

        self.num_tasks = 1 

        self.num_cpus_per_task_dict = {
			'epydia:remote': 24,
			'intelinx:remote':12
		}

        self.descr = 'Tensorflow official GPU Benchmark with RESNET-50'
        self.pre_run = ['git clone https://github.com/tensorflow/benchmarks.git']
        self.executable = 'python benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py'
        self.executable_opts = ['--num_gpus=1 --batch_size=32 --model=resnet50 --variable_update=parameter_server']
	
    def setup(self, partition, environ, **job_opts):

        self.num_cpus_per_task = self.num_cpus_per_task_dict[partition.fullname]
        super().setup(partition, environ, **job_opts)
