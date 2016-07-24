# layer-puppet-base

This layer facilitates the installation of puppet pkgs.

## Usage
To use this layer, include `puppet-base` in your layer's layer.yaml
```yaml
---
includes:
  - layer:puppet-base

...
```

Then you can react when the configured puppet services become available in consuming layers.

### States
**puppet.master.available** - This state is emitted once the desired puppet packages have been installed.
**puppet.agent.available** - This state is emitted once the desired puppet packages have been installed.
**puppet.db.available** - This state is emitted once the desired puppet packages have been installed.
**puppet.ca.available** - This state is emitted once the desired puppet packages have been installed.

### Contact
* [Puppet](https://puppet.com/)

### Copyright

Copyright &copy; 2016 James Beedy <jamesbeedy@gmail.com>

### License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
