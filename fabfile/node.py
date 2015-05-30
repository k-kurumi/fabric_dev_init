#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, task, prefix
from fabric.contrib import files

import re

def ndenv():
  if not files.exists('~/.ndenv'):
    run('git clone https://github.com/riywo/ndenv.git ~/.ndenv')
    run('git clone https://github.com/riywo/node-build.git ~/.ndenv/plugins/node-build')

    files.append('~/.shenv_local', re.sub(r'\n\s+', '\n', '''
                                      export PATH="$HOME/.ndenv/bin:$PATH"
                                      eval "$(ndenv init -)"
                                      '''))

  else:
    print "ndenv: already installed"


@task
def list():
  ndenv()
  with prefix('source ~/.shenv_local'):
    run('ndenv install -l')


@task
def install(version):
  ndenv()
  with prefix('source ~/.shenv_local'):
    run('ndenv install --verbose %s' % version)
    run('ndenv global %s' % version)
    run('npm install -g coffee-script coffeelint jshint underscore')
