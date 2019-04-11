from ProxyCheck import *
import argparse


def CheckProxy():

    ### function to check that the grid certificate is set                                                                                                                                                  

    os.system("voms-proxy-info > proxylog")
    proxy_check = open ("proxylog", "r")
    proxy_ok=False
    for line in proxy_check:
        if "timeleft" in line:
            proxy_ok=True
    proxy_check.close()
    os.system("rm proxylog")
    return proxy_ok



parser = argparse.ArgumentParser(description='options')
parser.add_argument('-x', dest='email', default="")
args = parser.parse_args()
user_email = args.email


SKFlatTag = os.environ['SKFlatTag']

### function checks proxy is set                                                                                                                                                                            
os.system("voms-proxy-destroy")
os.system("voms-proxy-init -voms cms")


if not CheckProxy():
  print "Please set grid certificate: voms-proxy-init cms"
  sys.exit(10)
