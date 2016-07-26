#!/usr/bin/env python
# coding: utf-8

from fabric.api import run, sudo, cd, task, env
from fabric.contrib import files

from .apt import install as apt_install, build_dep as apt_build_dep
import re

@task
def init():
  u'''開発に必要なコマンド一式ほか'''
  pkg = """
  vim
  build-essential
  git
  exuberant-ctags
  curl
  wget
  w3m
  zsh
  tree
  trash-cli
  mosh
  parallel
  renameutils
  p7zip-full
  unzip
  libmysqlclient-dev
  libsqlite3-dev
  sqlite3
  """
  apt_install(pkg)
  sudo('chsh -s /bin/zsh %s' % env.user)

  git()
  ag()
  pt()
  jq()
  tmux()
  tig()
  cf()
  direnv()
  vim_latest()
  massren()
  dotfiles()


def ag():
  if not files.exists('/usr/local/bin/ag'):
    pkg = """
    automake
    pkg-config
    libpcre3-dev
    zlib1g-dev
    liblzma-dev
    """
    apt_install(pkg)

    with cd('/tmp'):
      run('git clone https://github.com/ggreer/the_silver_searcher.git')

      with cd('the_silver_searcher'):
        run('./build.sh')
        sudo('make install')


def pt():
  if not files.exists('/usr/local/bin/pt'):
    with cd('/tmp'):
      run('wget https://github.com/monochromegane/the_platinum_searcher/releases/download/v2.1.3/pt_linux_amd64.tar.gz')
      run('tar zxvf pt_linux_amd64.tar.gz')
      sudo('cp pt_linux_amd64/pt /usr/local/bin')


def jq():
  if not files.exists('/usr/local/bin/jq'):
    with cd('/tmp'):
      run('wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -O jq')
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


def git():
  if not files.exists('/usr/local/bin/git'):
    pkg = """
    tcl
    gettext
    libcurl4-openssl-dev
    """
    apt_install(pkg)

    with cd('/tmp'):
      run('wget https://www.kernel.org/pub/software/scm/git/git-2.9.2.tar.gz')
      run('tar zxvf git-2.9.2.tar.gz')

      with cd('git-2.9.2'):
        run('./configure')
        run('make')
        sudo('make install')


def tmux():
  if not files.exists('/usr/local/bin/tmux'):
    pkg = """
    libevent-dev
    libncurses5-dev
    """
    apt_install(pkg)

    with cd('/tmp'):
      run('wget https://github.com/tmux/tmux/releases/download/2.2/tmux-2.2.tar.gz')
      run('tar zxvf tmux-2.2.tar.gz')

      with cd('tmux-2.2'):
        run('./configure')
        run('make')
        sudo('make install')


def tig():
  if not files.exists('/usr/local/bin/tig'):
    pkg = """
    libncursesw5
    libncursesw5-dev
    """
    apt_install(pkg)

    with cd('/tmp'):
      run('wget https://github.com/jonas/tig/archive/tig-2.1.1.tar.gz')
      run('tar zxvf tig-2.1.1.tar.gz')

      # tigはリリースのフォルダ名がおかしい
      with cd('tig-tig-2.1.1'):
        run('make configure')
        run('LDLIBS=-lncursesw CFLAGS=-I/usr/include/ncursesw ./configure --prefix=/usr/local')
        run('make')
        sudo('make install')


def vim_latest():
  if not files.exists('/usr/local/bin/vim'):
    pkg = '''
    python-dev
    ruby-dev
    luajit
    liblua5.2-dev
    '''
    apt_install(pkg)
    apt_build_dep('vim')

    with cd('/tmp'):
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

def cf():
  if not files.exists('/usr/local/bin/cf'):
    with cd('/tmp'):
      run('curl -L "https://cli.run.pivotal.io/stable?release=linux64-binary&source=github" | tar -zx')
      sudo('mv cf /usr/local/bin')

def direnv():
  if not files.exists('/usr/local/bin/direnv'):
    with cd('/tmp'):
      run('wget https://github.com/direnv/direnv/releases/download/v2.9.0/direnv.linux-amd64 -O direnv')
      run('chmod +x direnv')
      sudo('mv direnv /usr/local/bin')

    files.append('~/.shenv_local', re.sub(r'\n\s+', '\n', '''
                                      eval "$(direnv hook zsh)"
                                      '''))

def massren():
  u'''エディタ経由のリネームツール(renamer.vimは古くて使えなくなった)'''
  if not files.exists('/usr/local/bin/massren'):
    with cd('/tmp'):
      run('curl -L "https://github.com/laurent22/massren/releases/download/v1.3.0/massren.linux-amd64.tar.gz" | tar zx')
      sudo('mv massren /usr/local/bin')
