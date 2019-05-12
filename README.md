# bankAPI
This is a API that can be used to make bank transactions.
1)Register new user
2)Check balance
3)Tranfer Funds
4)Take Loan
5)Repay Loan


Software Requirements to run on Ubuntu Machine
---------------------------------------------
1)Docker
    Set up the repository

        Update the apt package index:

        $ sudo apt-get update

        Install packages to allow apt to use a repository over HTTPS:

        $ sudo apt-get install \
            apt-transport-https \
            ca-certificates \
            curl \
            gnupg-agent \
            software-properties-common
        
   Add Docker’s official GPG key:

         $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   
   Use the following command to set up the stable repository.
        
          $ sudo add-apt-repository \
             "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
             $(lsb_release -cs) \
             stable"
             
  Install Docker CE
          
         1- Update the apt package index.

          $ sudo apt-get update

         2- Install the latest version of Docker CE and containerd, or go to the next step to install a specific version:

          $ sudo apt-get install docker-ce docker-ce-cli containerd.io
         
         3- Verify that Docker CE is installed correctly by running the hello-world image.

          $ sudo docker run hello-world

2)Docker Compose 
    Run this command to download the current stable release of Docker Compose:

        sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o       /usr/local/bin/docker-compose
    

   Apply executable permissions to the binary:

        sudo chmod +x /usr/local/bin/docker-compose



   Test the installation.

        $ docker-compose --version
        
3)Postman -- To test the API -- https://www.getpostman.com/


RUN on your local machine
--------------------------
sudo docker-compose build

sudo docker-compose up

go to postman app and post data in json format & see the API work.
