# Database Connect
##1 ping mongdb ip:port every 30s in config file
####config
ip1:port1
ip2:port2
ip3:port3
ip4:port4
###1.1 if the master DB has disconnected, the DBsets will elect a slave DB to be a master.(there is only one master DB)
##2 if successfully ping to the master database, then connect.
###2.1 if not, then ping next ip:port

###2.2 if it has no master database, connect to slave, but it can only be read.
### for example, if one mongodb disconnected to other DBs, then it will became a slave DB. If more than half DBs have disconnected, then no master DB will be elected.