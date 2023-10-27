#!/bin/bash

# Update package lists
sudo apt update

# Install ruby-foreman
sudo apt install -y ruby-foreman

# Install entr
sudo apt install -y entr

# ***** Block to install KrakenD *****
# Add the GPG key for the specified keyserver
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 5DE6FD698AD6FDD2

# Add Krakend repository to sources list
sudo echo "deb https://repo.krakend.io/apt stable main" | sudo tee /etc/apt/sources.list.d/krakend.list

# Update package lists
sudo apt update

# Install KrakenD
sudo apt install -y krakend
# *************************************

# Install HTTPie for Terminal to work with REST APIs
sudo apt install -y httpie

# Install pip for Python 3
sudo apt install -y python3-pip

# Install FastAPI
pip3 install -r requirements.txt

# Print 'Installation Successful'
echo "\n\n"
echo "*****************************************"
echo "*        Installation Successful        *"
echo "*****************************************"
echo "To start the servers, run: 'foreman start'"
echo "\n" 