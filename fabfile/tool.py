#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, cd, task, env
from fabric.contrib import files

from .apt import install as apt_install, build_dep as apt_build_dep

@task
def init():
  # NOTE vagrantにmosh接続は表示がおかしくなる(udp関連かも)
  pkg = """
  vim
  build-essential
  git
  exuberant-ctags
  curl
  wget
  tmux
  zsh
  tree
  trash-cli
  silversearcher-ag
  mosh
  """
  apt_install(pkg)
  sudo('chsh -s /bin/zsh %s' % env.user)

  pt()
  jq()
  vim_latest()
  dotfiles()


def pt():
  if not files.exists('/usr/local/bin/pt'):
    with cd('/tmp'):
      run('wget https://github.com/monochromegane/the_platinum_searcher/releases/download/v1.7.6/pt_linux_amd64.tar.gz')
      run('tar zxvf pt_linux_amd64.tar.gz')
      sudo('cp pt_linux_amd64/pt /usr/local/bin')


def jq():
  if not files.exists('/usr/local/bin/jq'):
    with cd('/tmp'):
      run('wget http://stedolan.github.io/jq/download/linux64/jq')
      run('chmod +x jq')
      sudo('cp jq /usr/local/bin')


def dotfiles():
  if not files.exists('~/dotfiles'):
    run('git clone https://github.com/k-kurumi/dotfiles.git')

    with cd('dotfiles'):
      run('./replace.sh')

  if not files.exists('~/.vim'):
    # neobundle
    run('curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh')
    run('~/.vim/bundle/neobundle.vim/bin/neoinstall')


def mysqld():
  # noninteractiveを付けるとrootのパスワード問い合わせがなくなる
  sudo('DEBIAN_FRONTEND=noninteractive apt-get install -q -y mysql-server')


def vim_latest():
  pkg = '''
  python-dev
  ruby-dev
  luajit
  liblua5.2-dev
  '''
  apt_install(pkg)
  apt_build_dep('vim')

  if not files.exists('~/dotfiles'):
    run('git clone https://github.com/vim/vim.git')

    with cd('vim'):
      run('''./configure \
        --prefix=/usr/local \
        --with-features=huge \
        --enable-multibyte \
        --enable-pythoninterp=yes \
        --enable-rubyinterp=yes \
        --enable-luainterp=yes \
        --enable-cscope \
        --enable-gpm \
        --enable-cscope \
        --enable-fail-if-missing
        ''')
      run('make')
      sudo('make install')
