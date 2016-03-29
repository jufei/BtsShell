# -*- coding: utf-8 -*-
"""
:author: Pawel Kunat
:contact: pawel.kunat@nsn.com
"""

import os
import time
from subprocess import Popen, PIPE
from pkg_resources import resource_filename
from ute_common_java_remote.exception import RemoteJavaServerFailedToStartException


class JavaRemoteServer(object):

    SERVER_JAR_PATH = resource_filename(__name__, 'jar/jrobotremoteserver-3.0-standalone.jar')

    SERVER_MAIN_CLASS = 'org.robotframework.remoteserver.RemoteServer'

    def __init__(self, classpath, keyword_classes, **jvm_options):
        self._process = None
        self.port = None
        self.urls = None
        self._classpath = classpath
        self._keyword_classes = keyword_classes
        self._jvm_options = jvm_options

    def start(self):
        """Runs the underlying remote Java server process and creates the mapping of urls to keyword classes."""
        classpath_str = self._create_classpath_string(self._classpath)
        env = self._create_env(classpath_str)
        command = self._create_command(self._keyword_classes, self._jvm_options)
        self._process = Popen(command, env=env, stdout=PIPE)
        self.port = self._wait_for_port_bound(self._process)
        self.urls = self._create_urls(self.port, self._keyword_classes)

    def _create_env(self, classpath_str):
        env = os.environ.copy()
        env['CLASSPATH'] = classpath_str
        return env

    def _create_command(self, keyword_classes, jvm_options={}):
        command = ['java']
        command.extend(self._create_jvm_options(jvm_options))
        command.append(self.SERVER_MAIN_CLASS)
        command.extend(self._create_library_options(keyword_classes))
        return command

    def _create_jvm_options(self, jvm_options):
        options = []
        for name, value in jvm_options.items():
            option_expression = '-%s=%s' % (name, value)
            options.append(option_expression)
        return options

    def _create_library_options(self, keyword_classes):
        """Creates the --library command line options for the remote java server based on the list of keyword classes.
        Each option requires two parameters: --library <class>:<relative_url>. Since Java class names are unique and are valid URL paths,
        they are used as relative URLs here.
        """
        options = []
        for keyword_class in keyword_classes:
            options.append('--library')
            options.append('{0}:/{0}'.format(keyword_class))
        return options

    def _create_classpath_string(self, classpath):
        classpath_with_server_jar = list(classpath)
        classpath_with_server_jar.append(JavaRemoteServer.SERVER_JAR_PATH)
        return os.pathsep.join(classpath_with_server_jar)

    def _wait_for_port_bound(self, server_process):
        """Waits for the log 'Robot Framework remote server started on port [port].' in the server process's output or for EOF.

        :return: the port on which the remote java server is listening
        :rtype: string
        :raises RemoteJavaServerFailedToStartException: when the server process returns EOF before returning the log mentioned above
        """
        for line in iter(server_process.stdout.readline, b''):
            if 'server started on port' in line:
                return line.rstrip('.\r\n').split(' ')[-1]
        raise RemoteJavaServerFailedToStartException(str(server_process))

    def _create_urls(self, port, keyword_classes):
        urls = {}
        for kw_class in keyword_classes:
            urls[kw_class] = self._create_url(port, kw_class)
        return urls

    def _create_url(self, port, keyword_class):
        return '127.0.0.1:%s/%s' % (port, keyword_class)

    def stop(self, timeout_seconds=2.0):
        """Kills the underlying remote Java server process if it is running."""
        if not self._process:
            return
        if self._is_process_terminated():
            return
        self._process.stdout.close()
        self._process.terminate()
        if self._process_terminates_within(timeout_seconds):
            return
        self._process.kill()

    def _process_terminates_within(self, timeout_seconds):
        return self._wait(self._is_process_terminated, 0.25, timeout_seconds)

    def _is_process_terminated(self):
        return self._process.poll() is not None

    def _wait(self, cond_func, sleep_step, max_wait):
        start = time.time()
        while not cond_func():
            now = time.time()
            if now - start >= max_wait:
                return False
            time.sleep(sleep_step)
        return True
