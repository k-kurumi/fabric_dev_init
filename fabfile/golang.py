#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, task, prefix
from fabric.contrib import files

from .apt import install as apt_install

import re

def gvm():
  if not files.exists('~/.gvm'):
    pkg = """
    curl
    git
    mercurial
    make
    binutils
    bison
    gcc
    build-essential
    libcurl4-openssl-dev
    """
    apt_install(pkg)

    run('rm -rf ~/.gvm')
    run('bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)')
    run("""echo '[[ -s "$HOME/.gvm/scripts/gvm" ]] && source "$HOME/.gvm/scripts/gvm"' >> .shenv_local""")

    files.append('~/.shenv_local', re.sub(r'\n\s+', '\n', '''
                                      [[ -s "$HOME/.gvm/scripts/gvm" ]] && source "$HOME/.gvm/scripts/gvm"
                                      '''))

  else:
    print "gvm: already installed"


@task
def list():
  gvm()
  with prefix('source ~/.shenv_local'):
    run('gvm listall')


# NOTE 古いgitではgvm installに失敗する(ubuntu1204のgitは1.7)
@task
def install(version):
  gvm()
  with prefix('source ~/.shenv_local'):
    run('gvm install %s' % version)
    run('gvm use %s --default' % version)
