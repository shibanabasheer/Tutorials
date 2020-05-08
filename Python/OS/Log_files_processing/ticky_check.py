#!/usr/bin/env python3
import re
import csv
import operator
error_message={}
user_statistics={}
pattern_error=r"ERROR ([\w ]+)"
pattern_username=r"\(([\w.]+)\)"
with open("syslog.log") as f:
  for line in f:
    result_user=re.search(pattern_username,line)
    result_user=str(result_user.group(1)).strip()
    if "ERROR" in line:
      result=re.search(pattern_error,line)
      result=result.group()
      result=str(result).strip()
      if result in error_message:
        error_message[result] += 1
      else:
        error_message[result] = 1
      if result_user in user_statistics:
        user_statistics[result_user][1] += 1
      else:
        user_statistics[result_user] = [0,1]
    else:
      if result_user in user_statistics:
        user_statistics[result_user][0] += 1
      else:
        user_statistics[result_user] = [1,0]



usr_stst=[]
err_msg=[]
for item in user_statistics:
  d={}
  d["Username"] = item
  d["INFO"] = user_statistics[item][0]
  d["ERROR"] = user_statistics[item][1]
  usr_stst.append(d)
for item in sorted(error_message.items(), key = operator.itemgetter(1), reverse=True):
  d={}
  d["Error"] = item[0]
  d["Count"] = item[1]
  err_msg.append(d)
keys = ["Username", "INFO", "ERROR"]
with open("user_statistics.csv","w") as file:
  writer=csv.DictWriter(file,fieldnames=keys)
  writer.writeheader()
  writer.writerows(usr_stst)
keys = ["Error", "Count"]
with open("error_message.csv","w") as file:
  writer=csv.DictWriter(file,fieldnames=keys)
  writer.writeheader()
  writer.writerows(err_msg)