#!/usr/bin/python3
# Author Stephen Kennedy
# script to create new wordpress folder
import os
import sys
import pwd
import grp

def wp_get_latest():
  path = os.getcwd() # get the current directory for a base path

  #need to check if folder exits

  #get latest version of wordpress and extract
  os.system('curl -O https://wordpress.org/latest.tar.gz')
  os.system('tar xzvf latest.tar.gz' )

  # copy sample folders for wp-config and prep for moving to /var/www/html/
  tmp_path = ('%s/wordpress' % path)
  os.system('cp %s/wp-config-sample.php %s/wp-config.php' % (tmp_path, tmp_path))
  upgrade_folder = ('%s/wp-content/upgrade' % path)
  os.system('chown -R stitched:www-data wordpress/')

def create_site():
  # get new site name
  new_site = input("What is the new Wordpress site name: ")

  # need to check if folder exists
  new_site = str.strip(new_site)
  full_site = ('/var/www/html/%s' % new_site)
  os.system("cp -a wordpress/. %s" %  full_site)

  # set gid bit on each directory to ensure new files inherit permissions
  os.system('find %s -type d -exec chmod 755 {} \;' % full_site)

  # Change file structure to be a bit more restrictive
  os.system('find %s -type f -exec chmod 664 {} \;' % full_site)

  # add group write to wp-content. Make is recursive to promote file updating
  os.system('chmod -R 775 %s/wp-content' % full_site)

  # give server write access to plugins and themes
  os.system('chmod -R g+w %s/wp-content/themes' % full_site)
  os.system('chmod -R g+w %s/wp-content/plugins' % full_site)

  # update root permissions of wordpress directory
  os.system('chmod 750 %s' % full_site)

wp_get_latest()
create_site()
