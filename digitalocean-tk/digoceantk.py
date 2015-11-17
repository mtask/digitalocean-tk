import os, requests, argparse, sys, digitalocean, time, re

'''
Author: mtask@github.com
Program: vpsclient.py
'''

class DigOcean(object):

    def __init__(self):
        self.blk = '\033[0m' # Black - Regular
        self.warn = '\033[93m' # yellow
        self.grn = '\033[92m' # Green
        self.fatal = '\033[91m' #red
        self.manager = None #Digitalocean manager
    
    def get_input(self, prompt):
        #################################################### #
        #Get user input maintaining the python compatibility #
        #with earlier and newer versions.                    #
        ######################################################

        if sys.hexversion > 0x03000000:
            return input(prompt)
        else:
            return raw_input(prompt)


    def arguments(self,custom=None):
        ###################################################
        #Parse commandline arguments or if used in custom #
        #enviroment parse passed list("custom" var)       #
        ###################################################

        self.parser = argparse.ArgumentParser(description="Manage Digitalocean droplets", prog="digitalocean-tk")
        self.parser.add_argument("-t", "--token", action='store_true', help="Add Digitalocean access token")
        self.parser.add_argument("-l", "--listdroplets", action='store_true', help="List all droplet's name, id, image, status,region.")
        self.parser.add_argument("-rr", "--resetroot", action='store_true', help="Reset root password")
        
        self.parser.add_argument("-S", "--snapshot", help="Take snapshot of droplet(s) - Give droplet id(s) to snapshot. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
        self.parser.add_argument("-R", "--restore", help="Restore droplet from image - Give droplet id. Image id will be asked.")
        self.parser.add_argument("-s", "--shutdown", help="shutdown droplet(s) - Give droplet id(s) to shutdown. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
        self.parser.add_argument("-p", "--poweron", help="power on droplet(s) - Give droplet id(s) to power on. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
        self.parser.add_argument("-r", "--reboot", help="reboot droplet(s) - Give droplet id(s) to reboot. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
        self.parser.add_argument("-d", "--delete", help="delete droplet(s) - Give droplet id(s) to delete. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
        self.parser.add_argument("-fr", "--forcereboot", help="Power cycle droplet(s) - Give droplet id(s) to power cycle. Use \"\" if multiple droplets. Give \"all\" instead of id(s) to perform on all droplets")
 
        try:
            if custom:
                self.args = self.parser.parse_args(custom)
                self.parser.print_help()
            else:
                if len(sys.argv) <= 1:
                    self.parser.print_help()
                    sys.exit(0)
                else:
                    self.args = self.parser.parse_args()
            return self.args
        
        except SystemExit:
            if custom:
                return
            else:
                sys.exit(1)
     
    def setToken(self):
        #########################################################
        #Set api's acces token as enviroment variable to .bashrc#
        #########################################################

         while True:
             self.userName = self.get_input("Give local username: ")
             if self.userName == "root":
                 self.bashrcLocation = "/root/.bashrc"
             else:   
                 self.bashrcLocation = "/home/"+self.userName+"/.bashrc"
             try:
                 with open(self.bashrcLocation, "a") as brc:
                     self.apiToken = self.get_input("Give Digital Ocean access token: ")
                     brc.write('export DOTOKEN="'+self.apiToken+'"')
                 print(self.warn+"Re-open terminal/reload .bashrc"+self.blk)
                 break
             except Exception as e:
                 print(e)
                 continue
                 
    def listDroplets(self):
         ##################
         #Get all droplets#
         ##################
         self.droplets = self.manager.get_all_droplets()
         self.names = []
         print("Loading droplets")
         print("Your droplets")
         print(self.grn+"--------------------")
         for self.droplet in self.droplets:
             print(self.warn+"Name/ID: "+self.grn+self.droplet.name+"/"+str(self.droplet.id))
             print(self.warn+"Image: "+self.grn+self.droplet.image['slug'])
             
             print(self.warn+"Status: "+self.grn+self.droplet.status)
             print(self.warn+"Region: "+self.grn+self.droplet.region['name'])
             print("-------------------------")
             
         print(""+self.blk)
         return
    
    def takeSnapshot(self,droplet):
        ################
        #Take snapshot#
        ################
        print(self.warn+"Taking snapshot"+self.blk)
        try:
            self.droplet = self.manager.get_droplet(droplet)
            self.date_raw = str(time.strftime("%x"))
            self.snapshotName = "testi"
            self.droplet.take_snapshot(self.snapshotName,return_dict=False).wait()
            return True
        except Exception as e:
            print(e)
           
    def restoreImage(self, dropletid):
        ################
        #Take snapshot#
        ################
        print(self.warn+"Taking snapshot"+self.blk)
        try:
            
            self.droplet = self.manager.get_droplet(dropletid)
            print("Restoring droplet from snapshot")
            
  
  #self.droplet.restore(self.snapshotName,return_dict=False).wait()
            return True
        except Exception as e:
            print(e)
      
    def resetRoot(self,dropletList):
        #####################
        #Reset root password#
        #####################
         
        if dropletList[0].lower() == "all":
            self.droplets = self.manager.get_all_droplets()
        else:
            self.droplets = []
            for self.d in dropletList:
                self.droplets.append(self.manager.get_droplet(self.d))
        
        for self.droplet in self.droplets:
            print("Reseting "+str(self.droplet.name)+"'s root password")
            self.droplet.reset_root_password(return_dict=False)
        return True
        
    def deleteDroplet(self, dropletIDs):
        ###################
        #Delete droplet(a)#
        ###################
        
        self.dIDs = dropletIDs
        if dIDs[0].lower() == "all":
            try:
                self.droplets = self.manager.get_all_droplets()
            except TokenError as e:
                print (e)
        else:
            self.droplets = []
            try:
                for seld.id_ in self.dIDs:
                    self.droplets.append(self.manager.get_droplet(self.id_))
            except Exception as e:
                print (e)
         
        for self.droplet in self.droplets:
            print(self.fatal+"Delete: "+self.blk+str(self.droplet))
            print("Are you sure?(y/n)")
            
    def powermanager(self,dropletList, type_=None, snapshot=False):
        ####################################
        #Power on/off and reboot droplet(s)#
        ####################################
        
        self.type_ = type_
        try:
            if dropletList[0].lower() == "all":
                self.droplets = self.manager.get_all_droplets()
            else:
                self.droplets = []
                for self.d in dropletList:
                    self.droplets.append(self.manager.get_droplet(self.d))
            
            if self.type_.lower() == "off":
                print(self.warn+"Shutting down droplet(s)"+self.blk)
                for self.droplet in self.droplets:
                    self.droplet.shutdown(return_dict=False).wait()
                    self.droplet.power_off(return_dict=False)
            elif self.type_.lower() == "on":
                for self.droplet in self.droplets:    
                    self.droplet.power_on(return_dict=False)
            elif self.type_.lower() == "reboot":
                for self.droplet in self.droplets:
                    self.droplet.reboot(return_dict=False)
            elif self.type_.lower() == "freboot":
                for self.droplet in self.droplets:
                    self.droplet.power_cycle(return_dict=False)
            
            return True
        except Exception as e:
                print (e)     

    def main(self,customArgs=None):
         #Check if custom or sysarg and parse arguments
         if customArgs:
             self.args = self.arguments(customArgs)
         else:
             self.args = self.arguments()
         #Set access token for Digitalocean api
         #Token is set in .bashrc as enviroment variable 
         #Bash shell needs to be restarted or .bashrc reloaded after setting token
         if self.args.token:
             self.setToken()
             return
         
         #Load access token 
         self.doToken = os.environ['DOTOKEN']  
         if not self.doToken:
             print(self.fatal+"[Error]: Could not find access token"+self.blk)
             if customArgs:
                 return
             else:
                 sys.exit(1)
         else:
             self.manager = digitalocean.Manager(token=self.doToken)
                 
         if self.args.listdroplets:
             #List users all droplets
             self.listDroplets()    
         elif self.args.shutdown:
             self.dropletList = self.args.shutdown.split()
             if self.powermanager(self.dropletList, type_='off'):
                 print(self.grn+"Droplet(s) shutdowned successfully"+self.blk)
         elif self.args.poweron:
             self.dropletList = self.args.poweron.split()
             if self.powermanager(self.dropletList, type_='on'):
                 print(self.grn+"Droplet(s) turned on successfully"+self.blk)
         elif self.args.reboot:
             self.dropletList = self.args.reboot.split()
             if self.powermanager(self.dropletList, type_='reboot'):
                 print(self.grn+"Droplet(s) rebooted successfully"+self.blk)
         elif self.args.forcereboot:
             self.dropletList = self.args.reboot.split()
             if self.powermanager(self.dropletList, type_='freboot'):
                 print(self.grn+"Droplet(s) rebooted successfully"+self.blk)
         elif self.args.resetroot:
             self.dropletList = self.args.reboot.split()
             if self.resetRoot(self.dropletList):
                 print(self.grn+"Droplet(s) root password reseted successfully"+self.blk)
         elif self.args.snapshot:
             self.droplet = self.args.snapshot
             if self.takeSnapshot(self.droplet):
                 print(self.grn+"Droplet snapshotted successfully"+self.blk)
         elif self.args.restore:
             self.droplet = self.args.restore
             if self.restoreImage(self.droplet):
                 print(self.grn+"Droplet restored successfully"+self.blk)
         
         
         
              
                  
if __name__ == "__main__":
    do = DigOcean()
    do.main()