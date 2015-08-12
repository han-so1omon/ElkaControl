import sys, os, re, datetime, time, shutil
sys.path.append(os.getcwd()) 
print '{}/Logging/PrevLogs'.format(os.getcwd())


d = datetime.datetime.fromtimestamp(time.time())
s = './Logging/PrevLogs/inputs-{0}-{1}-{2}_{3}_{4}_{5}.log'.\
    format(d.year,d.month,d.day,d.hour,d.minute,d.second)

inl = './Logging/Logs/inputs.log'

try:
  os.mkdir('{}/Logging/PrevLogs'.format(os.getcwd()))
except OSError:
  pass # directory already exists

shutil.copy2(inl, s)
