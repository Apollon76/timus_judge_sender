#!/usr/bin/python3

import os
import urllib.request
import requests
import sys
import itertools
import time
import pyquery
import pickle

import timusAPI

judge_id = ""

ext_id = {
    "cpp"   : "46",
    "c"     : "45",
    "py"    : "48",
    "java"  : "32",
}

"""
Timus Online Judge compilators' ids:
"31" > 	FreePascal 2.6
"39" >  Visual C 2017
"40" >  Visual C++ 2017
"45" > 	GCC 7.1
"46" >  G++ 7.1
"30" >  Clang++ 4.0.1
"32" >  Java 1.8
"41" >  Visual C# 2017
"34" >  Python 2.7
"48" >  Python 3.6
"14" >  Go 1.3
"18" >  Ruby 1.9
"19" >  Haskell 7.6
"33" >  Scala 2.11
"""
def main():
    if len(sys.argv) < 2:
        print("Solution filename not specified")
        sys.exit()
    if not os.path.exists(sys.argv[1]):
        print("Solution file does not exist or not enough rights to read it")
        sys.exit()
    filename = os.path.basename(sys.argv[1])
    filename, extension = os.path.splitext(filename)
    extension = extension[1:]
    problem_index = timusAPI.get_task_id(filename)
    if (problem_index is None):
        print("Incorrect filename name.")
        sys.exit()
    if extension not in ext_id:
        print("Unknown extension. Please check 'ext_id' variable")
        sys.exit()
    data = {
        "Action":               "submit",
        "JudgeID":              judge_id,
        "ProblemNum":           problem_index,
        "Source":               open(sys.argv[1], "rb").read(),
        "Language":             ext_id[extension],
        "SourceFile":           "",
        "SpaceID":              "1"
    }
    submit_addr = "http://acm.timus.ru/submit.aspx"
    requests.post(submit_addr, data=data)
    print ("\n Solution is successfully sent. Current time is " + time.strftime("%H:%M:%S") + "\n")
    status_addr = "http://acm.timus.ru/status.aspx"
    author_id = ''.join(itertools.takewhile(lambda c: c.isdigit(), judge_id))
    old_verdict = " "
    while True:
        req = requests.get(status_addr, params={"author": author_id})

        con = req.text
        id0 = con.find("Memory used")
        
        id1 = con.find("nofollow", id0)
        id2 = con.find("<", id1)
        submit_id = con[id1+10:id2]

        id1 = con.find("verdict", id2)
        id2 = con.find("<", id1)
        new_verdict = con[id1+12:id2]
        br = new_verdict.find("(")
        if (br != -1):
            new_verdict = new_verdict[:br-1]
        
        id1 = con.find("test", id2)
        id2 = con.find("<", id1)
        test = con[id1+6:id2]
                
        id1 = con.find("runtime", id2)
        id2 = con.find("<", id1)
        runtime = con[id1+9:id2]
                
        id1 = con.find("memory", id2)
        id2 = con.find("<", id1)
        memory = con[id1+8:id2]

        if (old_verdict != new_verdict):
            if (new_verdict == "Compiling" or new_verdict == "Running"):
                print (" " + new_verdict + "...")
            else:
                print("--------------------------------------------------------------------")
                if (new_verdict == ""):
                    print ('%22s' % ("Compilation error"), "\t\tTime: 0", "\tMemory used: 0 KB", '\n')
                    ses = requests.Session()
                    ses.post("http://acm.timus.ru/auth.aspx", data = { "JudgeID" : judge_id, "Action" : "login" } )
                    print(ses.get("http://acm.timus.ru/ce.aspx?id=" + submit_id).text)
                elif (new_verdict == "Accepted"):
                    print ('Time: %s\tMemory used: %s\t%22s\n' % (runtime, memory, new_verdict))
                else:
                    print ('Time: %s\tMemory used: %s\t%22s %s\n' % (runtime, memory, new_verdict, test))
                break
            old_verdict = new_verdict
        time.sleep(0.5)


if __name__ == '__main__':
    main()
