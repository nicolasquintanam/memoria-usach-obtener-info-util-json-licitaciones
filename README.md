### Instalación en Linux

```
wget --load-cookies /tmp/cookies.txt "https://drive.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/uc?export=download&id=1Z9Brr7AEwkknWmYi8U_KCYYMdfOtfn--' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Z9Brr7AEwkknWmYi8U_KCYYMdfOtfn--" -O historicoJsonLicitaciones.zip && rm -rf /tmp/cookies.txt
sudo apt-get update
apt install python3-pip zip unzip -y &&
pip3 install --upgrade pip
pip3 install pandas
pip3 install xlsxwriter
python3 script.py
```
