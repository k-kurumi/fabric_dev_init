#!/usr/bin/env python
# coding: utf-8

from fabric.api import sudo, task

@task
def jst():
  u'''JSTに変更'''
  sudo('ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime')
