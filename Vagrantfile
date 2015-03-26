Vagrant.configure("2") do |config|
  config.vm.box = "chef/centos-6.5"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

#   Web Server Configuration
  config.vm.define "app" do |app|
    app.vm.network "forwarded_port", guest: 80, host: 9500
    app.vm.network "forwarded_port", guest: 8000, host: 8000
    app.vm.network "forwarded_port", guest: 22, host: 2223
    app.vm.network "private_network", ip: "192.168.10.2"
    app.vm.synced_folder "/Users/joel/Desktop/data", "/data"
  end
  
#   Database Server Configuration
  config.vm.define "db" do |db|
    db.vm.network "forwarded_port", guest: 9200, host: 9200
    db.vm.network "private_network", ip: "192.168.10.3"
  end

end
