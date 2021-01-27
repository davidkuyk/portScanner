import socket
import common_ports
import re

def get_open_ports(target, port_range, *args):

  socket.setdefaulttimeout(.15)

  open_ports = []
  try:
  
    if re.search("\d+.\d+.\d+.\d+", target):
      ip = socket.gethostbyname(target)
      try:
        url = socket.gethostbyaddr(target)[0]
      except:
        url = False
    else:
      ip = socket.gethostbyname(target)
      url = target

    portRange = port_range

    for port in range(portRange[0], portRange[1] + 1):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new socket
        if serv.connect_ex((target, port)) == 0:
            open_ports.append(port)
        serv.close() # close connection

    finalPorts = []
    services = []

    for port in open_ports:
        if port in common_ports.ports_and_services.keys():
          finalPorts.append(port)
          services.append(common_ports.ports_and_services[port])

    if args and (args[0] == True):
      if url == False:
        url = ''
      else:
        url = url + ' '
        ip = '(' + ip + ')'
      prettyPorts = f'''Open ports for {url}{ip}
PORT     SERVICE'''
      
      for i in range(len(services)):
        if len(str(finalPorts[i])) == 2:
          spaces = '       '
        elif len(str(finalPorts[i])) == 3:
          spaces = '      '
        prettyPorts += f'\n{finalPorts[i]}{spaces}{services[i]}'
      
      return prettyPorts
    else:
      return(finalPorts)
  except:
    if re.search("\d+.\d+.\d+.\d+", target):
        return 'Error: Invalid IP address'
    else:
      return 'Error: Invalid hostname'