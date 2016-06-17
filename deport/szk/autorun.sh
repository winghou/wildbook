#########################################################################
# File Name: autorun.sh
# Author: bovenson
# Email:  szhkai@126.com
# Created Time: 2016-06-17 18:55:49
#########################################################################
#!/bin/bash
uwsgi --ini ./wildbook_uwsgi.ini -d error.log
