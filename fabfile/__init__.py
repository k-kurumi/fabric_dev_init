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

env.use_ssh_config = True
env.colorize_errors = True

# 環境変数SSH_CONFIG_PATHがなければ~/.ssh/configが使われる
if os.environ.has_key("SSH_CONFIG_PATH"):
  env.ssh_config_path = os.environ["SSH_CONFIG_PATH"]
