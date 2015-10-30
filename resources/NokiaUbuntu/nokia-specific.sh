# Nokia package
wget http://linux.inside.nokiasiemensnetworks.com/ftp/nsn/ubuntu/nsn-release_1.5-1_all.deb
sudo dpkg -i nsn-release_1.5-1_all.deb
# logout
# login
ls /etc/apt/sources.list.d/ # nsn.list should be here
sudo apt-get update
sudo apt-get install nokia-register
sudo nokia-register # Enter your NOKIA_USERNAME

# Linux Certificate guide (https://confluence.int.net.nokia.com/display/EE/Linux+Certificate+Guide)
openssl req -new -newkey rsa:2048 -keyout <NOKIA_USERNAME>.ipa.nsn-net.net.key -out <NOKIA_USERNAME>.ipa.nsn-net.net.csr
#    PEM pass phrase: <OWN_PASSWORD>
#    Country Name: PH
#    State or Province Name: Metro Manila
#    Locality Name: Quezon City
#    Organization Name: Nokia
#    Organizational Unit Name: [BLANK]
#    Common Name: <NOKIA_USERNAME>.ipa.nsn-net.net
#    Email Address: <NOKIA_EMAIL_ADDRESS>
#    A challenge password: [BLANK]
#    An optional company name: [BLANK]
mv <NOKIA_USERNAME>.ipa.nsn-net.net.key ~/certs
mv <NOKIA_USERNAME>.ipa.nsn-net.net.csr ~/certs
openssl req -in ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.csr -text -noout | grep -e 'Version:' -e 'Attributes' -A 1
sudo apt-get install nsn-config-certs
# When Service Desk replies with your request, download *.pem.txt and *.crt.txt to ~/certs
mv *.pem.txt *.pem
mv *.crt.txt *.crt
openssl x509 –in ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.crt -dates # validity (2 years)
openssl req -new -key ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.key -out <PATH/TO/NEW/.csr> # renew certificate

# NOSI access (https://confluence.int.net.nokia.com/display/EE/NOSI+access)
# 1. Follow Linux Certificate guide
# 2. Create a SNOW ticket
#    1. https://nsnsi.service-now.com/ess/home.do
#    2. Type NOSI in the search bar -> Choose NOSI certificate creation
#        Request on behalf on: <SEARCH_YOUR_NAME>
#        Kindly follow...: <SEARCH_YOUR_NAME>
#        Mention the...: "Please provide NOSI certificate. Csr file attached."
#    3. Attach .csr in the request
#    4. Order Now
# 3. Configure NetworkManager
#    1. Connect to NOSI wireless
#        Authentication: TLS
#        Identity: host/<NOKIA_USERNAME>.ipa.nsn-net.net
#        User certificate: ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.crt
#        CA certificate: ~/etc/pki/tls/certs/NSN_Root_CA.crt
#        Private key: ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.key
#        Private key password: <PEM_PASS_PHRASE>

# AnyConnect client (32-bit)
wget http://linux.inside.nsn.com/ftp/nsn/rhel/testing/anyconnect-predeploy-linux-3.1.04066-k9.tar.gz
tar -xf anyconnect-predeploy-linux-3.1.04066-k9.tar.gz

# AnyConnect client (64-bit) (https://confluence.int.net.nokia.com/display/EE/NRA+VPN+Guide+for+NSN+Linux)
wget http://linux.inside.nsn.com/ftp/nsn/rhel/testing/anyconnect-predeploy-linux-64-3.1.04066-k9.tar.gz
tar -xf anyconnect-predeploy-linux-64-3.1.04066-k9.tar.gz
cd anyconnect-3.1.04066/vpn
sudo ./vpn_install.sh
sudo ln -s /etc/pki/tls/certs/NSN_Root_CA.crt /opt/.cisco/certificates/ca/NSN_Root_CA.crt # Symbolic link creation
cd /opt/cisco/anyconnect/profile/
sudo wget http://linux.inside.nokiasiemensnetworks.com/ftp/nsn/conf/vpn/anyconnect-cert-latest-linux.xml
# Assuming that you have proper .crt and .pem in ~/certs
mkdir -p ~/.cisco/certificates/client/private/
cp ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.pem ~/.cisco/certificates/client/
cp ~/certs/<NOKIA_USERNAME>.ipa.nsn-net.net.key ~/.cisco/certificates/client/private/

# gitlab SSH
ssh-keygen -t rsa -C "paolo.de_los_santos@nokia.com"
cat ~/.ssh/id_rsa.pubd
xclip -sel clip < ~/.ssh/id_rsa.pub
# Copy-paste the key to the 'My SSH Keys' section under the 'SSH' tab in your user profile. Please copy the complete key starting with ssh- and ending with your username and host.
