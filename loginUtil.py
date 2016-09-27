#!/usr/bin/env python3
# coding=utf-8
__author__ = 'smallfly'

import requests
import re
import sys

LOGIN_ADDRESS = "http://1.1.1.2/ac_portal/login.php"
FLOW_ADDRESS = "http://1.1.1.2/ac_portal/userflux"

def login(username, password, remember=0):
    data = {
        "opr": "pwdLogin",
        "userName": username,
        "pwd": password,
        "rememberPwd": remember
    }
    resp = requests.post(LOGIN_ADDRESS, data=data)
    resp.encoding = 'UTF-8'
    print(resp.status_code, resp.text)

def logout():
    data = {
        "opr": "logout"
    }
    resp = requests.post(LOGIN_ADDRESS, data=data)
    resp.encoding = 'UTF-8'
    print(resp.status_code, resp.text)

def query_quota(display=False):
    resp = requests.post(FLOW_ADDRESS)
    resp.encoding = "UTF-8"
    # print(resp.status_code, resp.text)
    content = resp.text
    if "错误" in resp.text:
        return None, None, None
    username_pattern = r'<td>(\d*[a-z]+\d*)</td>'
    username = re.search(username_pattern, content)
    # print(username.group(1))

    used_flow_pattern = r'(\d*\.?\d*)M'
    used_flow = re.search(used_flow_pattern, content)
    # print(used_flow.group(1))

    total_flow_pattern = r'(\d*\.?\d*)G'
    total_flow = re.search(total_flow_pattern, content)
    # print(total_flow.group(1))

    user, used, total = username.group(1), used_flow.group(1) , total_flow.group(1)
    if display:
        message = "username: {}\nused: {}M\ntotal: {}G\n".format(user, used, total)
        print(message)
    return user, used, total

def login_interaction():
    user = input("username: ")
    pwd = input("password: ")
    login(user, pwd)
    # query_quota()

def interact():
    choice = input("1. login\n2. logout\n3. query:\n")
    if not choice in ['1', '2', '3']:
        return -1
    return choice


def main():
    choice = None
    if len(sys.argv) > 1:
        try:
            choice = sys.argv[1]
        except Exception:
            choice = None
    if choice is None:
        choice = interact()
    if choice == '1':
        login_interaction()
        query_quota(display=True)
    elif choice == '2':
        logout()
    elif choice == '3':
        query_quota(display=True)
    else:
        print("fuck u!!!wrong choice")
        main()


if __name__ == "__main__":
    main()

