# layer-puppet-base

This layer facilitates the installation of Puppet 4 services and modules on Ubuntu 14.04 and 16.04. It also provides handy functions for running Puppet scripts in standalone mode and parsing `facter` output.

## Usage

To use this layer, include `puppet-base`, and add an `options` for puppet-srvc in your layer's `layer.yaml`.

```yaml
# layer.yaml
---
includes:
  - layer:puppet-base

options:
  puppet-base:
    puppet-srvc: db

...
```

`puppet-srvc` is the Puppet service to install. Possible values:

- `standalone` installs the `puppet-agent` package without starting the service,
- `master` and `ca` install and start the `puppetserver` service,
- `agent` installs and starts the `puppet-agent` service,
- `db` installs and starts the `puppetdb` service.

Then you can react when the configured puppet services become available in consuming layers.

**Puppet DB example**

```python
import os
from charms.reactive import when, when_not, set_state
from charmhelpers.core.templating import render

PUPPET_DB_CONF = '/etc/puppetlabs/puppetdb/conf.d/puppet.conf'


@when('puppet.db.available', 'postgresql.available')
@when_not('puppet.db.configured')
def configure_pgsql(pgsql):

    '''Write out puppetdb config
    '''
    if os.path.exists(PUPPET_DB_CONF):
        os.remove(PUPPET_DB_CONF)
    render(source='puppet.conf',
           target=PUPPET_DB_CONF,
           perms=0o644,
           owner='root'
           ctxt={'PG_CONN': psql.connection_string()})

    set_state('puppet.db.configured')
```

**Puppet Standalone example**

```python
@when('puppet.standalone.installed')
def install_something_using_puppet():
    puppet = Puppet()
    facter = puppet.facter('networking')
    ipaddress = facter['ipaddress']
    templating.render(
        source='init.pp',
        target='/opt/my-app/init.pp',
        context={
          'address': ipaddress,
        }
    )
    puppet.apply('/opt/my-app/init.pp')
```

For an example of how to use this layer in standalone mode, see the [openvpn layer](https://github.com/IBCNServices/layer-openvpn).

### States

- **puppet.master.installed** - This state is emitted once the `puppetserver` package has been installed.
- **puppet.agent.installed** - This state is emitted once the `puppet-agent` package has been installed.
- **puppet.standalone.installed** - This state is emitted once the `puppet-agent` package has been installed in standalone mode.
- **puppet.db.installed** - This state is emitted once the `puppetdb` package has been installed.
- **puppet.ca.installed** - This state is emitted once the `puppetserver` package has been installed.

### More info on Puppet
* [Puppetlabs](https://puppet.com/)

### Copyright

- Copyright &copy; 2016 James Beedy <jamesbeedy@gmail.com>
- Copyright &copy; 2016 Merlijn Sebrechts <merlijn.sebrechts@gmail.com>

### License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
