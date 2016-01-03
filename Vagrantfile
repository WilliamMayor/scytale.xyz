Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.network "private_network", ip: "192.168.33.40"
    config.vm.hostname = "scytale.local"

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
    end

    config.vm.provision "shell", inline: <<-SCRIPT
        locale-gen en_GB.UTF-8

        apt-add-repository --yes ppa:fish-shell/release-2
        apt-get --assume-yes update
        apt-get --assume-yes dist-upgrade
        apt-get --assume-yes install git fish

        chsh -s /usr/bin/fish vagrant

        wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh

        wget -qO- https://get.docker.com/ | sh
        usermod -aG docker vagrant

        wget -qO- https://raw.githubusercontent.com/vantage-org/vantage/master/bootstrap | sh
        vantage plugins install pg
    SCRIPT
end
