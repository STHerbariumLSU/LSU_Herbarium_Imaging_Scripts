Nov 11/11/2020 
working with Eric Maxwell to try and get synology cbfla backup mounted on WS1 so it can act as a temp LaCie Drive. 

synology - z 
not in fstab 
didn't actually have synology properly mounted?
edit fstab with mount 

need to mount network drive via ubuntu on wsl 

sudo mount -t drvfs 'Z:' /mnt/cbfla

Need to edit etc/fstab to make sure network drive is always mounted. 
cifs is giving issues 



