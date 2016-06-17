#!/bin/bash
sudo rm /etc/nginx/sites-enabled/wildbook_nginx.conf
sudo ln -s /home/ubuntu/project/wildbook/deport/szk/wildbook_nginx.conf /etc/nginx/sites-enabled/wildbook_nginx.confsudo service nginx restart
