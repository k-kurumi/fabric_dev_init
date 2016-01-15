#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, task, prefix
from fabric.contrib import files

from .apt import install as apt_install

import re

def pyenv():
  if not files.exists('~/.pyenv'):
    pkg = """
    make
    build-essential
    libssl-dev
    zlib1g-dev
    libbz2-dev
    libreadline-dev
    libsqlite3-dev
    wget
    curl
    llvm
    """
    apt_install(pkg)

    run('git clone https://github.com/yyuu/pyenv.git ~/.pyenv')
    run('git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv')

    files.append('~/.shenv_local', re.sub(r'\n\s+', '\n', '''
                                      export PYENV_ROOT=$HOME/.pyenv
                                      export PATH=$PYENV_ROOT/bin:$PATH
                                      eval "$(pyenv init -)"
                                      eval "$(pyenv virtualenv-init -)"
                                      '''))

  else:
    print "pyenv: already installed"


@task
def list():
  u'''インストール可能なバージョン一覧'''
  pyenv()
  with prefix('source ~/.shenv_local'):
    run('pyenv install -l')



@task
def install(version):
  u'''指定バージョンをインストール'''
  pyenv()
  with prefix('source ~/.shenv_local'):
    run('pyenv install %s' % version)
