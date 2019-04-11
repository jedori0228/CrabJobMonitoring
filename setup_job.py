from ProxyCheck import *
import argparse

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
