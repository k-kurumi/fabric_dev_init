#!/usr/bin/env python
# coding: utf-8

from fabric.api import env

import apt
import tool
import ruby
import python
import golang
import node

env.use_ssh_config = True
env.ssh_config_path = "ssh_config"
env.colorize_errors = True
