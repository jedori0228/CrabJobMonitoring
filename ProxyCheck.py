import os,time

from datetime import datetime, timedelta

#user="jalmond"
#email_user='jalmond@cern.ch'
#e_subject="Lxplus connection script"

time_reset= 60*60 ### set to an hour (in seconds). This is time between loops
time_renewal=12 #### in hours : This is time before ticket renewal stops, when email is sent to let user know to renew manually


def CheckProxy():
    
    os.system("voms-proxy-info > proxylog")
    proxy_check = open ("proxylog", "r")
    proxy_ok=False
    for line in proxy_check:
        if "timeleft" in line:
            proxy_ok=True
    proxy_check.close()
    os.system("rm proxylog")
    return proxy_ok



###########################################
def CheckKerbos(email_user):

    ### Only send email if ticket is almost run out
    SendEmail=False

    os.system("klist")
    os.system("klist > klist_check")
    check_klist = open("klist_check","r")
    email_content =  open("email.txt","w")

    afs_kerb=False
    ticket_is_valid=True
    renewal_expiring=False

    for x in check_klist:
        if "afs/cern.ch@CERN.CH" in x:
            afs_kerb=True
            email_content.write("Current ticket AFS:\n")
            email_content.write(x+"\n")
        if not afs_kerb:
            continue
        if "renew until" in x:
            email_content.write(x+"\n")
            sx = x.split()
            renew_date = sx[2]
            renew_date=renew_date.replace("/"," ")
            s_renew_date = renew_date.split()
            
            renew_year= 2000+ int(s_renew_date[2])
            renew_month= int(s_renew_date[0])
            renew_day=int( s_renew_date[1])
            
            renew_time=sx[3] 
            renew_time=renew_time.replace(":"," ")
            s_renew_time=renew_time.split()
            renew_hour= int(s_renew_time[0])
            renew_minute= int(s_renew_time[1])
            

            future_time = datetime.now() + timedelta(hours=time_renewal)

            #### check if renewal date is within "time_reset" hours from now, if so send email to let user know

            if datetime(renew_year, renew_month, renew_day,renew_hour,renew_minute ) < datetime.now():
                ticket_is_valid=False
                
            elif datetime(renew_year, renew_month, renew_day,renew_hour,renew_minute ) < future_time:
                email_content.write("\n")

                renewal_expiring=True
                email_content.write("renew allowed until " + sx[2] + "\n")
                email_content.write("\n")
                email_content.write("Ticket extended by "+ str(time_renewal)+" hours \n")

            ### Reset- expiration of ticket 
            os.system("kinit -R")
            break

    status = -1
    if not afs_kerb or not ticket_is_valid:
        ### if no proxy make user setup
        print "No kerberos. Check kinit"
        SendEmail=True
        status= 0

    if renewal_expiring: 
        SendEmail=True
        status = 1

    check_klist.close()
    email_content.close()


    if email_user== "":
        SendEmail=False

    ###################################################
 
    if SendEmail:
        
        path_file_email="./email.sh"
        file_email=open(path_file_email,"w")
        if renewal_expiring:
            file_email.write('cat email.txt | mail -s "'+e_subject + ': New kerberos ticket needed within '+str(time_renewal)+' hours " ' +str(email_user))

        file_email.close()

        os.system("cat " + path_file_email)
        os.system("source " + path_file_email)
        
        os.remove(path_file_email)
        os.remove("email.txt")
        os.remove("klist_check")
    return status

    
