#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, task, prefix
from fabric.contrib import files

from .apt import install as apt_install

import re

def rbenv():
  if not files.exists('~/.rbenv'):
    pkg = """
    autoconf
    bison
    build-essential
    libssl-dev
    libyaml-dev
    libreadline6-dev
    zlib1g-dev
    libncurses5-dev
    libffi-dev
    libgdbm3
    libgdbm-dev
    """
    apt_install(pkg)

    run('git clone https://github.com/sstephenson/rbenv.git ~/.rbenv')
    run('git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build')

    files.append('~/.shenv_local', re.sub(r'\n\s+', '\n', '''
                                      export PATH="$HOME/.rbenv/bin:$PATH"
                                      eval "$(rbenv init -)"
                                      '''))
  else:
    print "rbenv: already installed"


@task
def list():
  u'''インストール可能なバージョン一覧'''
  rbenv()
  with prefix('source ~/.shenv_local'):
    run('rbenv install -l')


@task
def install(version):
  u'''指定バージョンをインストール'''
  rbenv()
  # 時間がかかり止まったように見えるため --verbose する
  with prefix('source ~/.shenv_local'):
    run('rbenv install --verbose %s' % version)
    run('rbenv global %s' % version)
    run('gem install bundler pry pry-doc --no-ri --no-rdoc')
