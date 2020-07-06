from util.OSProcess import get_processid_by_name, kill_process_tree, time

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