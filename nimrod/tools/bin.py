import os

PATH = os.path.dirname(os.path.abspath(__file__))

JUNIT = os.sep.join([PATH, 'bin', 'junit-4.12.jar'])
HAMCREST = os.sep.join([PATH, 'bin', 'hamcrest-core-1.3.jar'])
EVOSUITE = os.sep.join([PATH, 'bin', 'evosuite-1.0.6.jar'])
EVOSUITE_RUNTIME = os.sep.join([PATH, 'bin',
                                'evosuite-standalone-runtime-1.0.6.jar'])
MOD_RANDOOP = os.sep.join([PATH, 'bin', 'modified-randoop-all-4.2.5.jar'])
JMOCKIT = os.sep.join([PATH, 'bin', 'jmockit-1.40-marcio.1.jar'])
RANDOOP = os.sep.join([PATH, 'bin', 'randoop-all-4.2.5.jar'])
SAFIRA = os.sep.join([PATH, 'bin', 'safira.jar'])
JACOCOCLI = os.sep.join([PATH, 'bin', 'jacococli.jar'])
JACOCOAGENT = os.sep.join([PATH, 'bin', 'jacocoagent.jar'])
RANDOOPY = os.sep.join([PATH, 'bin', 'randoop-all-4.2.5-mod.jar'])