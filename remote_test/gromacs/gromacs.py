import os
import reframe as rfm
import reframe.utility.sanity as sn

class GromacsBaseTestCPU(rfm.RegressionTest):
	def __init__(self):
		super().__init__()


		## Compilation Phase 

		# Name of the test and programming environment 
		self.descr = "Gromacs cpu benchmark for unknown system"
		self.valid_systems = ['intelinx:remote',]
		self.valid_prog_environs = ['Prg-gnu']
		
		#Source directory 
		self.prebuild_cmd = ['wget http://ftp.gromacs.org/pub/gromacs/gromacs-2019.tar.gz', 
								'tar -xvf  gromacs-2019.tar.gz',
								'cd gromacs-2019',
								'mkdir build',
								'cd build',
								'cmake ../ \
							    -DBUILD_SHARED_LIBS=off \
    							-DBUILD_TESTING=off \
    							-DREGRESSIONTEST_DOWNLOAD=OFF \
    							-DCMAKE_C_COMPILER=`which mpicc` \
    							-DCMAKE_CXX_COMPILER=`which mpicxx` \
    							-DGMX_BUILD_OWN_FFTW=on \
    							-DGMX_SIMD=AVX2_256 \
    							-DGMX_DOUBLE=off \
    							-DGMX_EXTERNAL_BLAS=off \
    							-DGMX_EXTERNAL_LAPACK=off \
    							-DGMX_FFT_LIBRARY=fftw3 \
    							-DGMX_GPU=off \
    							-DGMX_MPI=on \
    							-DGMX_OPENMP=off \
    							-DGMX_X11=off']
	
		self.build_system = 'Make'
		self.build_system.max_concurrency = 12
		self.build_system.flags_from_environ = False

		## Running Phase 

		self.executable = 'gromacs-2019/build/bin/gmx_mpi'

		self.time_limit = (2,0,0)

		self.sanity_patterns = sn.all([
			sn.assert_found(r'Finished mdrun on rank 0', 'logfile.log')])

		self.perf_patterns = {
			'perf': sn.extractsingle(r'Performance:\s+(?P<perf>\S+)', self.stderr, 'perf', float)
		}

		self.reference = {
			'cartesius:normal-haswell': {
				'perf': (8,-1.0, 1.0,'ns/day')
			},
			'intelinx:remote': {
				'perf': (1.079, -1.0,1.0, 'ns/day')}
		}

	def setup(self, partition, environ, **job_opts):

		super().setup(partition, environ, **job_opts)

@rfm.simple_test
class GromacsCPUTestPrace(GromacsBaseTestCPU):
	def __init__(self):
		super().__init__()

		self.executable_opts = ['mdrun -s lignocellulose-rf.tpr -maxh 0.25 -nsteps 50000 -g logfile -pin on']

		self.pre_run = ['wget http://www.prace-ri.eu/UEABS/GROMACS/1.2/GROMACS_TestCaseB.tar.gz',
						'tar -xvf GROMACS_TestCaseB.tar.gz']

		self.num_task = {
			'epydia:remote': 24,
			'intelinx:remote':12
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		super().setup(partition, environ, **job_opts)

		
@rfm.simple_test
class GromacsCPUTestSABS(GromacsBaseTestCPU):
	def __init__(self):
		super().__init__()

		self.executable_opts = ['mdrun -v -pin on -dlb auto -deffnm topol']

		self.pre_run = [
			'tar xf SABS_gromacs_input.tar.gz',
			'{} grompp -f sabs.mdp -c sabs.gro -p sabs.top -n sabs.ndx -maxwarn 1'.format(self.executable)
		]

		self.num_cpus_per_task = 1 

		self.sanity_patterns = sn.all([
			sn.assert_found(r'Finished mdrun on rank 0', 'topol.log')])

		self.num_task = {
			'epydia:remote': 24,
			'intelinx:remote':12
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		super().setup(partition, environ, **job_opts)


#############################################################################################################


class GromacsTestGPUBase(rfm.RegressionTest):
	def __init__(self):
		super().__init__()

		## Compilation Phase 

		# Name of the test and programming environment 
		self.descr = "Gromacs gpu benchmark for unknown system"
		self.valid_systems = ['intelinx:remote','epydia:remote']
		self.valid_prog_environs = ['Prg-gnu']
		
		#Source directory 
		self.prebuild_cmd = ['wget http://ftp.gromacs.org/pub/gromacs/gromacs-2019.tar.gz', 
								'tar -xvf  gromacs-2019.tar.gz',
								'cd gromacs-2019',
								'mkdir build',
								'cd build',
								'cmake ../ \
							    -DBUILD_SHARED_LIBS=off \
    							-DBUILD_TESTING=off \
    							-DREGRESSIONTEST_DOWNLOAD=OFF \
    							-DCMAKE_C_COMPILER=$EBROOTOPENMPI/bin/mpicc \
    							-DCMAKE_CXX_COMPILER=$EBROOTOPENMPI/bin/mpicxx \
    							-DGMX_BUILD_OWN_FFTW=on \
    							-DGMX_SIMD=AVX2_256 \
    							-DGMX_DOUBLE=off \
    							-DGMX_EXTERNAL_BLAS=off \
    							-DGMX_EXTERNAL_LAPACK=off \
    							-DGMX_FFT_LIBRARY=fftw3 \
    							-DGMX_GPU=on -DCUDA_TOOLKIT_ROOT_DIR=$CUDAHOME\
    							-DGMX_MPI=on \
    							-DGMX_OPENMP=on \
    							-DGMX_X11=off']
	
		self.build_system = 'Make'
		self.build_system.max_concurrency = 12
		self.build_system.flags_from_environ = False


		## Running Phase 
		self.executable = 'gromacs-2019/build/bin/gmx_mpi'

		self.time_limit = (2,0,0)

		#self.readonly_files = ['GROMACS_TestCaseB.tar.gz']

		self.sanity_patterns = sn.all([
			sn.assert_found(r'Finished mdrun on rank 0', 'logfile.log')])

		self.perf_patterns = {
			'perf': sn.extractsingle(r'Performance:\s+(?P<perf>\S+)', self.stderr, 'perf', float)
		}

		self.num_gpus_per_node = 1  

		self.reference = {
			'cartesius:normal-haswell': {
				'perf': (8,-1.0, 1.0,'ns/day')
			},
			'intelinx:remote': {
				'perf': (3.364, -1.0,1.0, 'ns/day')}
		}

	def setup(self, partition, environ, **job_opts):

		super().setup(partition, environ, **job_opts)

@rfm.simple_test
class GromacsGPUTestPrace_2_MPI_task(GromacsTestGPUBase):
	def __init__(self):
		super().__init__()

		example_name = 'lignocellulose-rf.tpr'
		self.executable_opts = ['mdrun -s {} -maxh 0.0625 -nsteps 50000 -g logfile -pin on'.format(example_name)]

		self.pre_run = ['wget http://www.prace-ri.eu/UEABS/GROMACS/1.2/GROMACS_TestCaseB.tar.gz',
						'tar -xvf GROMACS_TestCaseB.tar.gz']

		self.num_task = {
			'epydia:remote': 6,
			'intelinx:remote':2
		}
		self.openmp_num_threads = {
			'epydia:remote': 4,
			'intelinx:remote':6
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		self.variables['OMP_NUM_THREADS'] = str(self.openmp_num_threads[partition.fullname])
		super().setup(partition, environ, **job_opts)

@rfm.simple_test
class GromacsGPUTestPrace_1_MPI_task(GromacsGPUTestPrace_2_MPI_task):
	def __init__(self):
		super().__init__()

		self.num_task = {
			'epydia:remote': 24,
			'intelinx:remote':1
		}
		self.openmp_num_threads = {
			'epydia:remote': 24,
			'intelinx:remote':12
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		self.variables['OMP_NUM_THREADS'] = str(self.openmp_num_threads[partition.fullname])
		super().setup(partition, environ, **job_opts)



@rfm.simple_test
class GromacsGPUTestSABS_2_MPI_task(GromacsTestGPUBase):
	def __init__(self):
		super().__init__()

		self.executable_opts = ['mdrun -v -pin on -dlb auto -deffnm topol']

		self.pre_run = [
			'tar xf SABS_gromacs_input.tar.gz',
			'{} grompp -f sabs.mdp -c sabs.gro -p sabs.top -n sabs.ndx -maxwarn 1'.format(self.executable)
		]

		self.sanity_patterns = sn.all([
			sn.assert_found(r'Finished mdrun on rank 0', 'topol.log')])

		self.num_task = {
			'epydia:remote': 24,
			'intelinx:remote':2
		}
		self.openmp_num_threads = {
			'epydia:remote': 24,
			'intelinx:remote':6
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		self.variables['OMP_NUM_THREADS'] = str(self.openmp_num_threads[partition.fullname])
		super().setup(partition, environ, **job_opts)

@rfm.simple_test
class GromacsGPUTestSABS_1_MPI_task(GromacsGPUTestSABS_2_MPI_task):
	def __init__(self):
		super().__init__()

		self.num_task = {
			'epydia:remote': 24,
			'intelinx:remote':1
		}
		self.openmp_num_threads = {
			'epydia:remote': 24,
			'intelinx:remote':12
		}

	def setup(self, partition, environ, **job_opts):
		self.num_tasks = self.num_task[partition.fullname]
		self.variables['OMP_NUM_THREADS'] = str(self.openmp_num_threads[partition.fullname])
		super().setup(partition, environ, **job_opts)
