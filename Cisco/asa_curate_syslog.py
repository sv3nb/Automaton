# Clean up syslog file by removing lines with eventid ASA-6-106015, UDP, ICMP, ASA-6-302013
# we use the sed bash command so this only works within a bash shell/linux environment.

import subprocess

bashcommands = ["sed -i '/ASA-6-106015/d' cisco_syslog.log", \
  "sed -i '/ASA-6-302013/d' cisco_syslog.log", \
  "sed -i '/UDP/Id' cisco_syslog.log", "sed -i '/ICMP/Id' cisco_syslog.log"]

for command in bashcommands:
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
