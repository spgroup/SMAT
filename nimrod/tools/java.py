import logging
import os
import sys
import subprocess

from nimrod.utils import get_java_files

TIMEOUT = 10 * 60


class Java:

    def __init__(self, java_home=None):
        self.java_home = java_home
        self._javac = None
        self._java = None
        self._set_home()
        self._check()

    def _check(self):
        try:
            self._version_javac()
            self._version_java()
        except FileNotFoundError:
            raise SystemExit()

    def _set_home(self):
        if not self.java_home:
            if 'JAVA_HOME' in os.environ and os.environ['JAVA_HOME']:
                self.java_home = os.environ['JAVA_HOME']
            else:
                print('JAVA_HOME undefined.', file=sys.stderr)
                raise SystemExit()

    @property
    def javac(self):
        return os.path.join(self.java_home, os.sep.join(['bin', 'javac']))

    @property
    def javap(self):
        return os.path.join(self.java_home, os.sep.join(['bin', 'javap']))

    @property
    def java(self):
        return os.path.join(self.java_home, os.sep.join(['bin', 'java']))

    def _version_javac(self):
        return self.simple_exec_javac('-version')

    def _version_java(self):
        return self.simple_exec_java('-version')

    def simple_exec_java(self, *args):
        return self.exec_java(None, self.get_env(), TIMEOUT, *args)

    def exec_java(self, cwd, env, timeout, *args):
        return self._exec(self.java, cwd, env, timeout, *args)

    def simple_exec_javac(self, *args):
        return self.exec_javac(None, None, self.get_env(), TIMEOUT, *args)

    def exec_javac(self, java_file, cwd, env, timeout, *args):
        args = list(args)
        if java_file:
            args.append(java_file)

        return self._exec(self.javac, cwd, env, timeout, *args)

    def exec_javap(self, class_file, cwd, env, timeout, *args):
        args = list(args)
        if class_file:
            args.append(class_file)

        return self._exec(self.javap, cwd, env, timeout, *args)    

    @staticmethod
    def _exec(program, cwd, env, timeout, *args):
        try:
            command = [program] + list(args)

            logging.debug(command)

            return subprocess.check_output(command, cwd=cwd, env=env,
                                           timeout=timeout,
                                           stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error(e)
            raise e
        except RuntimeError as e:
            logging.error(e)
            RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            raise e
        except subprocess.TimeoutExpired as e:
            logging.error(e)
            raise e
        except FileNotFoundError as e:
            logging.error('[ERROR] {0}: not found.'.format(program))
            raise e

    def get_env(self, variables=None):
        env = os.environ.copy()
        env['JAVA_HOME'] = self.java_home
        env['PATH'] = (os.environ['PATH'] + os.pathsep
                       + os.path.join(self.java_home, 'bin'))

        if variables:
            for key in variables.keys():
                env[key] = variables[key]

        return env

    def compile_all(self, classpath, directory):
        if os.path.exists(directory):
            java_files = get_java_files(directory)
            for java_file in java_files:
                class_file = os.path.join(directory,
                                          java_file.replace('.java', '.class'))
                if not os.path.exists(class_file):
                    self.exec_javac(java_file, directory, None, None,
                                    '-classpath', classpath)
