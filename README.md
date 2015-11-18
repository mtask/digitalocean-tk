##digitalocean-tk

Toolkit for managing DigitalOcean's Virtual Private servers, also known as Droplets.

Tested with Python2.7 on Debian.	

###Features:

 - List all your Droplets with name, id, region, image and status info. 
 
 - Reset Droplets root password.
 
 - Powermanaging: Turn on/off and reboot Droplets.
 
 - Take and restore snapshots. 

###Depencies:

pip install -U python-digitalocean

###First run:

DigitalOceans access token needs to be set before other features come available.

Check "-t/--token" option below.

Access token is saved as enviroment variable and digitalocean-tk retrieves it from there.

###usage:

digitalocean-tk [-h] [-t] [-l] [-rr] [-S SNAPSHOT] [-R RESTORE]
                       
                       [-s SHUTDOWN] [-p POWERON] [-r REBOOT] [-d DELETE]
                       
                       [-fr FORCEREBOOT]

Manage Digitalocean droplets

optional arguments:

-h, --help
  
Show help message and exit

-t, --token

Add Digitalocean access token. Token will be saved as enviroment  variable.

-l, --listdroplets 

List all droplet's name, id, image, status,region.

-rr RESETROOT, --resetroot RESETROOT

Reset root password

-S SNAPSHOT, --snapshot SNAPSHOT

Take snapshot of droplet(s) - Give droplet id(s) to snapshot. Use "" if multiple droplets. Give "all" instead of id(s) to perform on all droplets

-R RESTORE, --restore RESTORE

Restore droplet from image - Give droplet id. Image id will be asked.

-s SHUTDOWN, --shutdown SHUTDOWN

Shutdown droplet(s) - Give droplet id(s) to shutdown.
Use "" if multiple droplets. Give "all" instead id(s) to perform on all droplets.

-p POWERON, --poweron POWERON

power on droplet(s) - Give droplet id(s) to power on.Use "" if multiple droplets. Give "all" instead of id(s) to perform on all droplets

-r REBOOT, --reboot REBOOT

Reboot droplet(s) - Give droplet id(s) to reboot. Use "" if multiple droplets. Give "all" instead of id(s)
                        to perform on all droplets
-d DELETE, --delete DELETE

Delete droplet(s) - Give droplet id(s) to delete. Use "" if multiple droplets. Give "all" instead of id(s) to perform on all droplets

-fr FORCEREBOOT, --forcereboot FORCEREBOOT

Power cycle droplet(s) - Give droplet id(s) to power cycle. Use "" if multiple droplets. Give "all" instead of id(s) to perform on all droplets
