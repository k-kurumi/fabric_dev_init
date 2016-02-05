#!/usr/bin/env python
# coding: utf-8

from fabric.api import sudo, task

@task
def jst():
  u'''JSTに変更'''
  sudo('ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime')

@task
def utc():
  u'''UTCに変更'''
  sudo('ln -sf /usr/share/zoneinfo/UTC /etc/localtime')
