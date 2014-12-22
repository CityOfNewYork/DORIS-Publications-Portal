Vagrant.configure("2") do |config|
  config.vm.box = "chef/centos-6.5"
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

#   Web Server Configuration
  config.vm.define "web" do |web|
    web.vm.network "forwarded_port", guest: 80, host: 9500
    web.vm.network "private_network", ip: "192.168.10.2"
  end
  
#   Database Server Configuration
  config.vm.define "db" do |db|
    db.vm.network "private_network", ip: "192.168.10.3"
  end

end