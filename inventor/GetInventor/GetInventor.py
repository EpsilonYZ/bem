# Path for Inventor executable. Don't forget to escape the \ characters (use \\)!
InventorPath = "c:\\Program Files\\Autodesk\\Inventor 2012\\Bin\\Inventor.exe"

# Name of the batch file
CheckStatus = '"InventorStatus.bat"'


import warnings
# The following line suppresses popen2 deprecation warning message
warnings.simplefilter('ignore', DeprecationWarning)
import popen2
import string
import re               # Regular expressions module (to match strings)
import time
import os

while True:
    (pout, pin)  = popen2.popen2(CheckStatus)
    issued = -1
    inuse = -1
    displayUsers = False
    for line in pout:
        # The following works as of Nov. 2011, but may become obsolete once our license number is renewed
        if line.find("Users of 85814PDSP_F") >= 0:
            sLicensesIssued = re.search('[0-9]*(?= licenses issued| license issued)', line)
            if (not sLicensesIssued) or len(sLicensesIssued.group()) == 0:
                break
            sLicensesIssued = sLicensesIssued.group()
            issued = string.atoi(sLicensesIssued)
            sLicensesInUse = re.search('[0-9]*(?= licenses in use| license in use)', line)
            if (not sLicensesInUse) or len(sLicensesInUse.group()) == 0:
                break
            sLicensesInUse = sLicensesInUse.group()
            inuse = string.atoi(sLicensesInUse)
            if inuse >= issued:
                # Will display the list of current users
                displayUsers = True
                print "Current users:\n"
                continue
            else:
                break
        if displayUsers and line.find('Total of') >= 0:
            print ""
            break
        if displayUsers and line.find('start') >= 0:
            sUser = re.search('^\s*\w*', line)
            if sUser:
                print sUser.group()
    pout.close()
    pin.close()
    print "Total number of licenses: " + str(issued) + ". In use: " + str(inuse) + ".\n"
    if issued < 0 or inuse < 0:
        print "Error: Could not read status from server."
        print "There might be a connection problem,"
        print "or an issue with file " + CheckStatus
        break
    if inuse < issued:
        # Start inventor
        try:
            os.spawnl(os.P_NOWAIT,InventorPath,"DUMMY")
        except OSError:
            print "Could not find Inventor. Following path seems incorrect:"
            print InventorPath
            break
        except:
            print "Unknown error when trying to start Inventor."
            break
        print "Starting Inventor, be patient!..."
        break
    time.sleep(0.1)     # Allows repeated messages to not see still
    print "Will re-interrogate server in 10s...\n"
    time.sleep(9.9)     # Wait 10s before interrogating the server again

print"\nGetInventor is done. This window will close automatically in 20s."
time.sleep(20)          # Delay before closing output window, to allow printed message to be read