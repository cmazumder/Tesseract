"""
Standalone operations on based on OS processes
"""

import os
import signal
import time

import psutil


def get_processid_by_name(process_name):
    """
    Get a list of all the PIDs of the running process whose name contains
    the given string processName

    :param process_name: windows process name
    :type process_name: str
    :return: list of running process information with process_name
    :rtype: list
    """
    gone = alive = []
    list_of_processes = []
    # Iterate over the all the running process
    for process in psutil.process_iter():
        try:
            info = process.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if process_name.lower() in info['name'].lower():
                list_of_processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_processes


def kill_process_tree(pid, sig=signal.SIGTERM, include_parent=True,
                      timeout=None, on_terminate=None):
    """
    Kill a process tree (including grandchildren) with signal "sig" and
    return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is called as soon as a child terminates.

    :param pid: Process id of process
    :type pid: str
    :param sig: Optional argument for Termination Signals
    :type sig: str
    :param include_parent: Optional if parent process to be included
    :type include_parent: bool
    :param on_terminate: Optional for *callback* which is a function which gets called every time a process
        terminates (a Process instance is passed as callback argument)
    :param timeout: Process wait timeout
    :type timeout: float
    :type on_terminate: str
    :return: status of terminating the process
    :rtype: bool
    """
    assert pid != os.getpid(), "won't kill myself"
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            p.send_signal(sig)
        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    status = lambda pid: 'Running' if psutil.pid_exists(pid) else 'Terminated'
    return status(pid)


def close_running_process(process_name):
    """
    This will handle the termination of running processes passed in the list
    E.g. process_detail = get_processid_by_name('chrome', 'conhost', 'pycharm64.exe', 'WinMergeU')

    :param process_name: list of process to be terminated
    :type process_name: list
    """
    try:
        process_detail = get_processid_by_name(process_name=process_name)
        if len(process_detail) > 0:
            for element in process_detail:
                curr_pid = element['pid']
                curr_name = element['name']
                curr_created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(element['create_time']))
                print curr_pid, curr_name, curr_created_time
                status = kill_process_tree(pid=curr_pid)
                print "Process: {0}\tpid: {1}\tStatus:{2}".format(process_name, curr_pid, status)
        else:
            print"No running process found: {}".format(process_name)
    except (ValueError, TypeError, AttributeError) as err:
        print "Error closing process: {}\nargs:".format(err.message, err.args)
