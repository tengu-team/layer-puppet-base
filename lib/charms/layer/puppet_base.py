#!/usr/bin/python3
# Copyright (c) 2016, James Beedy <jamesbeedy@gmail.com>

import os
from subprocess import call

from charms import layer
from charmhelpers.core.templating import render
from charmhelpers.core import hookenv
from charmhelpers.core.host import lsb_release

import charms.apt


config = hookenv.config()


class Puppet:
    def __init__(self):
        self.options = layer.options('puppet-base')
        self.puppet_pkg = self.options.get('puppet-srvc')
        self.puppet_base_url = 'http://apt.puppetlabs.com'
        self.puppet_gpg_key = config['puppet-gpg-key']
        self.puppet_exe = '/opt/puppetlabs/bin/puppet'
        self.puppet_conf_dir = '/etc/puppetlabs/puppet'
        self.puppet_apt_src = 'deb %s xenial PC1' % self.puppet_base_url
        # Determine puppet apt package
        if self.puppet_pkg == 'master':
            self.puppet_apt_pkg = 'puppetserver'
            self.puppet_srvc = self.puppet_apt_pkg
        elif self.puppet_pkg == 'agent':
            self.puppet_apt_pkg = 'puppet-agent'
            self.puppet_srvc = 'puppet'
        elif self.puppet_pkg == 'db':
            self.puppet_apt_pkg = 'puppetdb'
            self.puppet_srvc = self.puppet_apt_pkg
        elif self.puppet_pkg == 'ca':
            self.puppet_apt_pkg = 'puppetserver'
            self.puppet_srvc = self.puppet_apt_pkg
        else:
            hookenv.status_set('blocked',
                               'Puppet pkg non-existent.'
                               'Please reconfigure puppet-base options.')
            exit(1)
        # Ensure service running cmd
        self.enable_puppet_cmd = \
            ('%s resource service %s ensure=running '
             'enable=true' % (self.puppet_exe, self.puppet_srvc))


    def install_puppet_apt_src(self):
        '''Fetch and install the puppet gpg key and puppet deb source
        '''
        hookenv.status_set('maintenance',
                           'Configuring Puppetlabs apt sources')
        # Add puppet gpg id and apt source
        charms.apt.add_source(self.puppet_apt_src, key=self.puppet_gpg_key)
        # Apt update to pick up the sources
        charms.apt.update()


    def install_puppet_apt_pkg(self):
        '''Install puppet pkg/enable srvc
        '''
        hookenv.status_set('maintenance',
                           'Installing %s' % self.puppet_srvc)
        self.install_puppet_apt_src()
        # Queue the installation of appropriate puppet pkgs
        charms.apt.queue_install(self.puppet_apt_pkg)
        charms.apt.install_queued()
        call(self.enable_puppet_cmd.split(), shell=False)
