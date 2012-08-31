"""
spice_common.py - shared methods for spice tests

"""
import os, logging, time


def wait_timeout(timeout=10):
    """
    time.sleep(timeout) + logging.debug(timeout)
    @param timeout=10
    """
    logging.debug("Waiting (timeout=%ss)", timeout)
    time.sleep(timeout)

def launch_gnome_session(vm_session):
    """
    Launches gnome session inside VM session
    @param vm_session - vm.wait_fo_login()

    metacity ensures that newly raised window will be active
    (remote-viewer auth dialog)
    which is not done by default in pure Xorg
    """
    cmd = "nohup gnome-session --display=:0.0 &> /dev/null &"
    return vm_session.cmd(cmd)

def launch_xorg(vm_session):
    """
    Launches Xorg inside vm_session on background
    @param vm_session - vm.wait_for_login()
    """
    cmd = "Xorg"
    killall(vm_session, cmd)
    wait_timeout() # Wait for Xorg to exit
    cmd = "nohup " + cmd + " &> /dev/null &"
    return vm_session.cmd(cmd)

def killall(vm_session, pth):
    """
    calls killall execname
    @params vm_session
    @params pth - path or execname
    """
    execname = pth.split(os.path.sep)[-1]
    vm_session.cmd("killall %s &> /dev/null" % execname, ok_status=[0, 1])
