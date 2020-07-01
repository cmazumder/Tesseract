import os
import signal
import time

import psutil


def get_processid_by_name(process_name):
    '''
    Get a list of all the PIDs of the running process whose name contains
    the given string processName
    '''
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
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
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
    # process_detail = get_processid_by_name('chrome', 'conhost', 'pycharm64.exe', 'WinMergeU')
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


def test_close_process():
    spacer = '-' * 50
    # This is just a test function, and not to be used in code
    # to-do remove while refactoring
    # listOfProcessIds = get_processid_by_name('chrome', 'conhost', 'pycharm64.exe', 'WinMergeU')
    listOfProcessIds = get_processid_by_name('iexplore')

    if len(listOfProcessIds) > 0:
        print spacer
        for elem in listOfProcessIds:
            processID = elem['pid']
            processName = elem['name']
            processCreationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            # processCreationTime = elem['create_time']
            print processID, processName, processCreationTime
            status = kill_process_tree(pid=processID)
            print "Process: {0}\tpid: {1}\tStatus:{2}".format(processName, processID, status)
            print spacer
    else:
        print('No Running Process found with given text')

# test_close_process()