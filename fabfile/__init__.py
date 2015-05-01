#!/usr/bin/env python
# coding: utf-8

from fabric.api import env

import apt
import tool
import ruby
import python
import golang

env.use_ssh_config = True
env.colorize_errors = True
