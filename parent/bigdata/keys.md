ssh team@176.109.91.18

HVE)Lf%@3I!P

sudo adduser hadoop

sudo -i -u hadoop

hadoop:zxc456


ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKS9bVv2F0zbzGCQY2GIDucwq/KOgm3aK6P0iKVvi8qw team@team-16-jn

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJqTe1JX5coRuI5pZZD+Fj0hCu4oFIqc9b/ego2jfYdp hadoop@team-16-jn
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKNu2eFd/eaEHn4ueb5jYdWTGfA/GK7Jp67dYPzX9GGo hadoop@team-16-nn
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM5k3gYpryctURKhfIhe4rcyR+7vLBa1m1Rpa/1FV1MF hadoop@team-16-dn-00
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMdydKttTlpcORAhznN2NH1YbWSemcgqXTmJA+tWZtnU hadoop@team-16-dn-01




/etc/hosts
192.168.1.66 team-16-jn
192.168.1.67 team-16-nn
192.168.1.68 team-16-dn-0
192.168.1.69 team-16-dn-1


tar -xvzf hadoop-3.4.0.tar.gz


sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/nn
sudo ln -s /etc/nginx/sites-available/nn /etc/nginx/sites-enabled/nn


