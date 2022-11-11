#!/bin/python3

""" sets up a web server """

from fabric.api import *

env.hosts = ["web-01.cloza.tech", "web-02.cloza.tech"]

def transfer_file(file_):
    """transfers files to server """
    for f in file_.split(','):
        put(f)

    print("======= done transfering ======")


def install():
    """ install packages """
    run("chmod u+x web_servers_setup.sh")
    run("./web_servers_setup.sh")


def run_script(file_):
    """ runs a script remotely """
    transfer_file(file_)
    for f in file_.split(','):
        run("chmod u+x " + f)
        run("./" + f)

def main(file_):
    """ transfer sript and installs poackages """
    transfer_file(file_)
    install()
