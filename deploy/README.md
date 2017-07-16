
mkdir ~/pirest-sense-hat

git clone https://github.com/jregueirar/pirest-sense-hat.git 

COMMANDS


vagrant up 
ansible-playbook -i staging pirest-sense-hat.yml 
