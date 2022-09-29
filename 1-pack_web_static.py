#!/usr/bin/python3
"""a simple fab file to create an archive file"""


from fabric.api import *
from datetime import datetime


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
