#
# SURFsara regression settings for running reframe on cartesius.
#


class ReframeSettings:
    _reframe_module = None
    _job_poll_intervals = [1, 2, 3]
    _job_submit_timeout = 60
    _checks_path = ['checks/']
    _checks_path_recurse = True
    _site_configuration = {
        'systems': {
            # AMD EPYC + NVIDIA GPUs
            'epydia': {
                'descr': 'Test system for das-6',
                'modules_system': [],
                # Adjust to your system's hostname
                'hostnames': ['localhost'],     
                'partitions': {
                    'login': {
                        'scheduler': 'local+mpirun',
                        'modules': [],
                        'access':  [],
                        'environs': ['Prg-gnu'],
                        'descr': 'Login nodes'
                    },
                    'remote': {
                        'scheduler': 'local+mpirun',
                        'modules': [],
                        'access':  [],
                        'environs': ['Prg-gnu'],
                        'descr': 'Login nodes'
                    },
                }
            },
            'cartesius': {
                'descr': 'Dutch National Supercomputer',
                'hostnames': ['int*','tcn*','fcn*','gcn*'],
                'modules_system': 'tmod4',
                'prefix': '/home/sagard/reframe/test/Reframe/tests',
                'stagedir': '/home/sagard/reframe/test/Reframe/staging',
                'resourcesdir': '/home/sagard/reframe/test/Reframe/resources',
                'partitions': {

                    'login': {
                        'scheduler': 'local',
                        'modules': [],
                        'access':  [],
                        'environs': ['PrgEnv-eb-Intel','eb-foss'],
                        'descr': 'Login nodes'
                    },
                    'normal-ivy': {
                        'descr': 'Thin nodes (Ivybridge)',
                        'scheduler': 'nativeslurm',
                        'access':  ['-p normal --constraint=ivy'],
                        'environs': ['PrgEnv-eb-Intel','eb-foss'],
                        'max_jobs': 100
                    },
                    'normal-haswell': {
                        'descr': 'Thin nodes (Haswell)',
                        'scheduler': 'nativeslurm',
                        'access':  ['-p normal --constraint=haswell'],
                        'environs': ['PrgEnv-eb-Intel','eb-foss'],
                        'max_jobs': 100
                    },
                    'broadwell': {
                        'descr': 'Thin nodes (Broadwell)',
                        'scheduler': 'nativeslurm',
                        'access':  ['-p broadwell'],
                        'environs': ['PrgEnv-eb-Intel','eb-foss'],
                        'max_jobs': 100
                    },
                    'fat': {
                        'descr': 'Fat nodes (Sandybridge)',
                        'scheduler': 'nativeslurm',
                        'access':  ['-p fat'],
                        'environs': ['PrgEnv-eb-Intel','eb-foss'],
                        'max_jobs': 100
                    },
                    'gpu': {
                        'descr': 'GPU nodes (K40) ',
                        'scheduler': 'nativeslurm',
                        'access':  ['-p gpu'],
                        'environs': ['eb-foss', 'PrgEnv-eb-Intel'],
                        'max_jobs': 100
                    },
		}
	    }


        },
        'environments': {
            'epydia': {
                'builtin': {
                    'type': 'ProgEnvironment',
                    'cc':  'cc',
                    'cxx': '',
                    'ftn': '',
                },
                'Prg-gnu': {
                    'type': 'ProgEnvironment',
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                }
            },
            'cartesius' : {
                'PrgEnv-eb-Intel' : {
                    'type' : 'ProgEnvironment',
                    'modules' : [ 'intel/2017b' ],
                    'cc'   : 'mpiicc',
                    'cxx'  : 'mpiicpc',
                    'ftn'  : 'mpiifort',
                },
                'eb-foss' : {
                    'type' : 'ProgEnvironment',
                    'modules' : [ 'foss/2017b', 'CMake/3.12.1-GCCcore-6.4.0' ],
                    'cc'   : 'mpicc',
                    'cxx'  : 'mpicxx',
                    'ftn'  : 'mpifort',
                },
                'PrgEnv-cuda': {
                    'type' : 'ProgEnvironment',
                    'modules':['cuda'],
                    'cxx'  : ''
                }
            },
        }
    }

    logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'file',
                'name': 'reframe.log',
                'level': 'DEBUG',
                'format': '[%(asctime)s] %(levelname)s: '
                          '%(check_info)s: %(message)s',
                'append': False,
            },

            # Output handling
            {
                'type': 'stream',
                'name': 'stdout',
                'level': 'INFO',
                'format': '%(message)s'
            },
            {
                'type': 'file',
                'name': 'reframe.out',
                'level': 'INFO',
                'format': '%(message)s',
                'append': False,
            }
        ]
    }

    perf_logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'filelog',
                'prefix': '%(check_system)s/%(check_partition)s',
                'level': 'INFO',
                'format': (
                    '%(asctime)s|reframe %(version)s|'
                    '%(check_info)s|jobid=%(check_jobid)s|'
                    '%(check_perf_var)s=%(check_perf_value)s|'
                    'ref=%(check_perf_ref)s '
                    '(l=%(check_perf_lower_thres)s, '
                    'u=%(check_perf_upper_thres)s)'
                ),
                'append': True
            }
        ]
    }

settings = ReframeSettings()
