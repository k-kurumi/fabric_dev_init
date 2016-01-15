#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, task

@task
def gitconfig():
  u'''git config --globaを設定する'''
  run('git config --global user.name k-kurumi')
  run('git config --global user.email "optpia.kurumi@gmail.com"')
  run('git config --global core.excludesfile "~/.gitignore_global"')
