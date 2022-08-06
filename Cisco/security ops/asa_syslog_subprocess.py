# Clean up syslog file by removing lines with eventid ASA-6-106015, UDP, ICMP, ASA-6-302013
# we use the sed bash command so this only works within a bash shell/linux environment.
# This script will extract udp and icmp traffic and write it to a separate file

import subprocess

syslogfile = "myfile.log"

bashcommands = [
  "sed -i '/ASA-6-106015/d' cisco_syslog.log", \
  "sed -i '/ASA-6-302013/d' cisco_syslog.log", \
  f"grep -i 'icmp' {syslogfile} > ./output/myfile_icmp.log && sed -i '/icmp/Id' {syslogfile}", \
  f"grep -i 'udp' {syslogfile} > ./output/myfile_udp.log && sed -i '/udp/Id' {syslogfile}"
]

for command in bashcommands:
  process1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  output, error = process1.communicate()

# if you plan on calling subprocess more than once in the same script
# Use different var names for each process e.g. process1, process2, etc..

print("start with final clean up")
final_cleanup = f"sed -i '/ASA-6-106015/d' {syslogfile} && mv {syslogfile} ./output/myfile_tcp"
process2 = subprocess.Popen(final_cleanup, shell=True, stdout=subprocess.PIPE)
output, error = process2.communicate()
 
