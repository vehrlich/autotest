"""
rv_video_close.py - Checks if video binary is running.
          If so, kill it.

Requires: binaries Xorg, totem, gnome-session
"""
import logging

def run_rv_video_close(test, params, env):
    """
    Closes totem

    @param test: KVM test object.
    @param params: Dictionary with the test parameters.
    @param env: Dictionary with test environment.
    """
    guest_vm = env.get_vm(params["guest_vm"])
    guest_vm.verify_alive()
    guest_session = guest_vm.wait_for_login(
            timeout=int(params.get("login_timeout", 360)))

    #get PID of remote-viewer and kill it
    logging.info("Get PID of totem")
    guest_session.cmd("pgrep %s" % params.get("video_binary"))

    logging.info("Try to kill totem")
    guest_session.cmd("pkill %s" % params.get("video_binary"))

    guest_session.close()
