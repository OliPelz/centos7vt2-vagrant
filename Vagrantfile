# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

require "yaml"
# include a file specifying all the repos we want to add to our reposerver, e.g. main or EPEL
vagrant_root = File.dirname(__FILE__)
vms = YAML.load_file(vagrant_root + "/vms_config.yml")

valid_vms = vms['lab_machines']

# every lesson at least needs the reposrv


has_end_state = false

#  I didn’t want this environment conflicting with others so I set the name of the internal network to some random string.
INTNET_NAME = [*('A'..'Z')].sample(8).join

#           puts <<-EOT
#     	     "#{valid_vms}"
#     "#{INTNET_NAME}"
#     	   EOT


Vagrant.configure("2") do |config|
# like global settings valid for all machines
   config.vm.provider "virtualbox"
  # config.vm.box = "centos/7"

   config.ssh.insert_key = false
   
   valid_vms.each_with_index do |(infos), index|
       config.vm.define "#{infos["name"]}" do |machine|
           machine.vm.box = "#{infos["box"]}"  
           machine.vm.network "private_network", ip: "#{infos["ip"]}"
	   #machine.ssh.username = "#{infos["ssh_username"]}"
           #puts <<-EOT
	   #  "total #{infos}"
           #EOT
           machine.vm.provider "virtualbox" do |vb|
               vb.gui = infos["gui"]
    	       vb.customize ["modifyvm", :id, "--memory", "#{infos["mem"]}"]
	       vb.customize ["modifyvm", :id, "--cpus", "#{infos["cpus"]}"]
	       vb.customize ["modifyvm", :id, "--nic2", "intnet", "--intnet2", "#{INTNET_NAME}"]
	   end
	      if infos.key? "mountpoints"
		      infos["mountpoints"].each do |mountpoint|
                  local_mp = mountpoint["local"]
	          remote_mp = mountpoint["remote"]
		  puts local_mp
		  puts remote_mp
		  machine.vm.synced_folder local_mp, remote_mp, owner:"root", group:"root", mount_options: ["dmode=755,fmode=644"]
	        end
              end
	    

              if ! has_end_state
   	         machine.vm.provision :ansible do |ansible|
	           ansible.limit = "#{infos["name"]}"
                   ansible.playbook = "#{infos["playbook"]}"
	      end
	# only exec at the nd for the last time
	      if has_end_state && index == valid_vms.size - 1
	         endstate_playbooks.each do |path|
		    me = /playbook-(.*).yml/.match(path)
   	            machine.vm.provision :ansible do |ansible|
	              ansible.limit = me[1]
	              ansible.playbook = path
	            end	     
		 end  
	     end
           end
       end
   end
end 
