#!/usr/bin/python3
"""a simple fab file to create an archive file"""


from fabric.api import *
from datetime import datetime
import os


env.hosts = ["100.25.39.211", "100.26.180.73"]


def do_clean(number=0):
    """deletes files older than first numbers"""
    save = number
    res = local("ls versions", capture=True)
    lst = []
    res = res.split("\n")
    for i in res:
        lst.append(i.split("_")[2].split(".")[0])
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

    number = save
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
    for i in res:
        lst.append(i.split("_")[2])
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
