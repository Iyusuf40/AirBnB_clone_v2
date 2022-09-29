#!/usr/bin/env bash
# installs nginx server
sudo apt-get -y update
sudo apt-get -y install nginx
echo ""
echo "install finished"
echo ""
echo "Hello World!" > /var/www/html/index.html
sudo service nginx start

hostname=$(hostname)
#configure redirect
# shellcheck disable=SC2154
isRewritePresent=$( grep rewrite < /etc/nginx/sites-available/default | \
cut -d " " -f1 )
if [ ! "$isRewritePresent" ]
then
sudo sed -i "s/server_name _;/server_name _;\n\trewrite ^\/redirect_me \
https:\/\/www.digitalocean.com\/community\/tutorials\/how-to-create-\
temporary-and-permanent-redirects-with-nginx permanent;/" /etc/nginx/\
sites-available/default
fi

#create custom_404 page
echo "Ceci n'est pas une page" > /var/www/html/custom_404.html

isErrorPagePresent=$( grep error_page < /etc/nginx/sites-enabled/default | \
cut -d " " -f1 ) 
#configure custom 404

if [ ! "$isErrorPagePresent" ]
then
sudo sed -i "s/server_name _;/error_page 404 \/custom_404.html;\
 \nserver_name _;/" /etc/nginx/sites-enabled/default
fi


#add a custom header
isAddHeaderPresent=$( grep add_header < /etc/nginx/sites-enabled/default | \
cut -d " " -f1 )

if [ ! "$isAddHeaderPresent" ]
then
sudo sed -i "s/error_page 404 \/custom_404.html;/add_header X-Served-By \
$hostname;\n\terror_page 404 \/custom_404.html;/" /etc/nginx/sites-enabled/default
fi

# create /data/web_static
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "this is a test" > /data/web_static/releases/test/index.html

# delete link if exist
if [ -e /data/web_static/current ]
then
rm -r /data/web_static/current
fi

sudo ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data

isStaticSet=$( grep hbnb_static < /etc/nginx/sites-enabled/default )

if [ ! "$isStaticSet" ]
then
echo "==== isStaticSet is false ===="
new="\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s/^\tlocation \/ {/$new\n\n\tlocation \/ {/" /etc/nginx/sites-enabled\
/default
fi

sudo service nginx restart
