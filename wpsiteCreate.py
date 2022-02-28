#!/usr/bin/python3
# Author Stephen Kennedy
# script to create new wordpress folder
import os
import sys
import pwd
import grp

def prepare_for_install():
  # Define list of dependencies for Wordpress
  dependency_list = ['apache2',
                     'ghostscript',
                     'libapache2-mod-php',
                     'mysql-server',
                     'php',
                     'php-bcmath',
                     'php-curl',
                     'php-imagick',
                     'php-intl',
                     'php-json',
                     'php-mbstring',
                     'php-mysql',
                     'php-xml',
                     'php-zip'
  ]

  for dependency in dependency_list:
    os.system(f'apt install {dependency} -y')

def install_wordpress():
  # get latest version of wordpress and extract
  os.system('curl -O https://wordpress.org/latest.tar.gz')
  os.system('tar -zxvf latest.tar.gz')

  # define new site name
  site_name = input('What is the new WordPress site name? \n')
  full_site = (f'/var/www/html/{site_name}')
  os.system(f'cp -R wordpress {full_site}')

  # set gid bit on each directory to ensure new files inherit permissions
  os.system('find %s -type d -exec chmod 755 \{} \;' % full_site)

  # Change file structure to be a bit more restrictive
  os.system('find %s -type f -exec chmod 664 {} \;' % full_site)

  # add group write to wp-content. Make is recursive to promote file updating
  os.system(f'chmod -R 775 {full_site}/wp-content')

  # give server write access to plugins and themes
  os.system(f'chmod -R g+w {full_site}/wp-content/themes')
  os.system(f'chmod -R g+w {full_site}/wp-content/plugins')
  os.system(f'chown -R rykt3r:www-data {full_site}' )

  # update root permissions of wordpress directory
  os.system(f'chmod 750 {full_site}')

#prepare_for_intall()
install_wordpress()
