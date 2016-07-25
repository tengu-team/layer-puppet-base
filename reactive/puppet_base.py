from charms import layer
from charms.reactive import when_not
from charms.reactive import set_state

from charmhelpers.core import hookenv

from charms.layer.puppet_base import Puppet


options = layer.options('puppet-base')
puppet_service = options.get('puppet-srvc')

PUPPET_SERVICE_INSTALLED = "puppet.%s.installed" % puppet_service


@when_not(PUPPET_SERVICE_INSTALLED)
def install_puppet_agent():

    '''Install puppet pkg
    '''
    hookenv.status_set('maintenance',
                       'Installing puppet %s' % puppet_service)
    p = Puppet()
    p.install_puppet_apt_pkg()
    set_state(PUPPET_SERVICE_INSTALLED)
