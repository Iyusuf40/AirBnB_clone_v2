#!/usr/bin/python3
'''a simple fab file to create an archive file'''


from fabric.api import *
from datetime import datetime
import os


env.hosts = ["100.25.39.211", "100.26.180.73"]


def do_deploy(archive_path):
    '''deploys files to servers in env.hosts'''
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
    print("\n=== done deploying ===\n")
    return True


def do_pack():
    '''creates an archive file'''
    local("mkdir -p versions")
    name = "web_static_{}{}{}{}{}{}.tgz"
    date_obj = datetime.now()
    name = name.format(date_obj.year, date_obj.month, date_obj.day,
                       date_obj.hour, date_obj.minute, date_obj.second)
    path = "versions/" + name
    cmd = "tar -cvzf " + path + " web_static"
    res = local(cmd)
    if res.succeeded:
        print("\n=== archive formed ===\n")
        return path


def deploy():
    '''deploys most recent version'''
    path = do_pack()
    if not path:
        return False
    res = do_deploy(path)
    return res


def clean_remote(number=0):
    '''removes old directories'''
    res = run("ls /data/web_static/releases")
    res = res.stdout
    delimeters = "\t\n\r"
    for delimeter in delimeters:
        res = res.split(delimeter)
        res = " ".join(res)
    print("after delimeter op:", res)
    res = res.split(" ")
    save = []
    for item in res:
        if item:
            save.append(item)
    res = save
    res.remove("test")
    print("res = ", res)
    lst = []
    for item in res:
        lst.append(item.split("_")[2])
    lst.sort(reverse=True)
    print(lst)
    number = int(number)
    lent = len(lst)
    if number > lent:
        number = lent
    if number < 2:
        keep = lst[:1]
    else:
        keep = lst[:number]
    print(keep)
    for item in res:
        num = item.split("_")[2]
        if num not in keep:
            run(f"rm -rf /data/web_static/releases/{item}")


def clean_local(number=0):
    '''cleans local archive'''
    res = local("ls versions", capture=True)
    lst = []
    res = res.split("\n")
    for item in res:
        lst.append(item.split("_")[2].split(".")[0])
    lst.sort(reverse=True)
    print(lst)
    number = int(number)
    lent = len(res)
    if number > lent:
        number = lent
    if number < 2:
        keep = lst[:1]
    else:
        keep = lst[:number]
    print(keep)
    for item in res:
        num = item.split("_")[2].split(".")[0]
        if num not in keep:
            local(f"rm -rf versions/{item}")


def do_clean(number=0):
    '''deletes files older than first numbers'''
    print("\n====== local clean starts ======\n")
    clean_local(number)
    print("\n====== local clean ends ======\n")
    print("\n====== remote clean starts ======\n")
    clean_remote(number)
    print("\n====== remote clean ends ======\n")
    return True
