#!/usr/bin/python3
"""a simple fab file to create an archive file"""


from fabric.api import *
from datetime import datetime
import os


env.hosts = ["100.25.39.211", "100.26.180.73"]


def do_deploy(archive_path):
    """deploys files to servers in env.hosts"""
    if not os.path.exists(archive_path):
        return False
    res = put(archive_path, "/tmp/")
    file_name = archive_path.split(".")[0]
    file_name = file_name.split("/")[1]
    cmd = "mkdir -p /data/web_static/releases/" + file_name
    run(cmd)
    cmd = "tar -xzf /tmp/" + file_name + ".tgz -C /data/web_static/releases/"\
        + file_name + "/"
    run(cmd)
    cmd = "rm /tmp/" + file_name + ".tgz"
    run(cmd)
    releases = "/data/web_static/releases/"
    releases_plus_file = releases + file_name
    cmd = "rm -rf " + releases_plus_file + "/styles"
    run(cmd)
    cmd = "rm -rf " + releases_plus_file + "/images"
    run(cmd)
    cmd = "mv -f " + releases_plus_file + "/web_static/* " + releases_plus_file
    run(cmd)
    cmd = "rm -rf " + releases_plus_file + "/web_static"
    run(cmd)
    cmd = "rm -rf /data/web_static/current"
    run(cmd)
    cmd = "ln -s " + releases_plus_file + "/ /data/web_static/current"
    run(cmd)
    return True


def do_pack():
    """creates an archive file"""
    local("mkdir -p versions")
    name = "web_static_{}{}{}{}{}{}.tgz"
    date_obj = datetime.now()
    name = name.format(date_obj.year, date_obj.month, date_obj.day,
                       date_obj.hour, date_obj.minute, date_obj.second)
    path = "versions/" + name
    cmd = "tar -cvzf " + path + " web_static"
    res = local(cmd)
    if res.succeeded:
        print(res.succeeded)
        return path


def deploy():
    """deploys most recent version"""
    path = do_pack()
    if not path:
        return False
    res = do_deploy(path)
    return res
