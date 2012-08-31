"""
rv_video.py - Starts video player

Requires: binaries Xorg, totem, gnome-session
          Test starts video player

"""
import logging
from autotest.client.virt import virt_remote
from autotest.client.virt import spice_utils

def launch_totem(guest_session, params):
    """
    Launch Totem player

    @param guest_vm - vm object
    """

    #repeat parameters for totem
    logging.info("Set up video repeat to '%s' to the Totem.",
                  params.get("repeat"))

    if params.get("repeat") == "yes":
        cmd = "gconftool-2 --set /apps/totem/repeat -t bool true"
    else:
        cmd = "gconftool-2 --set /apps/totem/repeat -t bool false"

    guest_session.cmd(cmd)

    cmd = "export DISPLAY=:0.0"
    guest_session.cmd(cmd)

    #fullscreen parameters for totem
    if params.get("fullscreen"):
        fullscreen = " --fullscreen "
    else:
        fullscreen = ""

    cmd = "nohup totem %s %s --display=:0.0 --play &> /dev/null &" \
            % (fullscreen, params.get("video_file"))
    guest_session.cmd(cmd)

def deploy_video_file(vm_obj, params):
    """
    Deploy video file into destination on vm

    @oaram file - file to transfer
    @param vm_obj - vm object
    @param destination - where to transfer
    """
    virt_remote.copy_files_to(vm_obj.get_address(), 'scp',
                          params.get("username"),
                          params.get("password"),
                          params.get("shell_port"),
                          params.get("source_video_file"),
                          params.get("video_file"))

def run_rv_video(test, params, env):
    """
    Test of video through spice

    @param test: KVM test object.
    @param params: Dictionary with the test parameters.
    @param env: Dictionary with test environment.
    """

    guest_vm = env.get_vm(params["guest_vm"])
    guest_vm.verify_alive()
    guest_session = guest_vm.wait_for_login(
            timeout=int(params.get("login_timeout", 360)))
    deploy_video_file(guest_vm, params)

    spice_utils.launch_xorg(guest_session)
    spice_utils.wait_timeout()
    spice_utils.launch_gnome_session(guest_session)
    spice_utils.wait_timeout()
    launch_totem(guest_session, params)
    guest_session.close()
