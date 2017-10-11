function install {
    echo installing $1
    shift
    apt-get -y install "$@" >/dev/null 2>&1
}

echo adding swap file
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap defaults 0 0' >> /etc/fstab

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update
install "Mongo DB" mongodb-org
echo -e "[Unit]\n Description=High-performance, schema-free document-oriented database\n After=network.target\n [Service]\n User=mongodb\n ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf\n [Install]\n WantedBy=multi-user.target" >> /etc/systemd/system/mongodb.service
sudo systemctl start mongodb
sudo systemctl enable mongodb

install "python" python-pip python-dev build-essential python-blinker
sudo pip install --upgrade pip 

install "Git" git
cd /opt
sudo mkdir idatosabiertos
cd idatosabiertos

sudo git clone https://github.com/idatosabiertos/calidad-aire-cdmx-latam
sudo git clone https://github.com/idatosabiertos/api-calidad-aire

cd calidad-aire-cdmx-latam
pip3 install pandas
install "zip" zip
sudo chmod +x ./cronjob.sh 
nohup ./cronjob.sh > /dev/null 2>&1 &

cd /opt/idatosabiertos/api-calidad-aire 
sudo rm -rf src/flask-mongoengine
sudo rm -rf src/mongoengine
sudo pip install -r requirements.txt
export con_secret=sRl1gtwWjtEuEkqagJifZyZxE
export con_secret_key=IgusDRzyt8fVlzlFQtMQa6fnaeexLAXOYlBemUF7XuUczRPV7o
export token=2537971922-ZjqRTjrqWwkG8SiFFWnNuNqEbHU6cq5ulrt1CYe
export token_key=HPi61C53C11Qr5tok0IvLVuFBkFioeZud0ac5eHfUlnCz
export rollbar_key=api-calidad-aire
export rollbar_environment=development
python run.py 

echo 'API corriendo en / API running on http://localhost:8000'