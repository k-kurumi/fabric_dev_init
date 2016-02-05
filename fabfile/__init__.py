#!/usr/bin/env python
# coding: utf-8

import os
from fabric.api import env

import apt
import tool
import ruby
import python
import golang
import node
import timezone
import gitconfig

env.use_ssh_config = True
env.colorize_errors = True

# カレントにssh_configがなければ~/.ssh/configが使われる
if os.path.exists("ssh_config"):
  env.ssh_config_path = "ssh_config"
