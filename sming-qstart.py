import os
import sys
import shutil
import argparse
import urllib
import zipfile
import tempfile
import subprocess


def make_argparser():
    parser = argparse.ArgumentParser(description='Sming project quickstart')
    # positional - project name
    parser.add_argument('name',
        help='project directory name, may be relative or absolute path')
    # optional
    # verbosity control
    verbosity_control_group = parser.add_mutually_exclusive_group()
    verbosity_control_group.add_argument('-v', '--verbose',
        action='store_true', default=False,
        help='run in verbose mode [default: %(default)s]')
    verbosity_control_group.add_argument('-s', '--silent',
        action='store_true', default=False,
        help='run in silent mode [default: %(default)s]')
    parser.add_argument('--skip-sanity-check',
        action='store_true',
        help='skip environment sanity check')
    parser.add_argument('--skip-git-init',
        action='store_true',
        help='skip local git repository initialization')
    parser.add_argument('--skip-git-commit',
        action='store_true',
        help='skip initial git commit')
    parser.add_argument('--skip-license',
        action='store_true',
        help='skip adding file with MIT license')
    return parser


class Quickstart(object):

    SKEL_ZIP_URL = 'https://github.com/zgoda/sming-skel/archive/master.zip'
    SKEL_DIR_NAME = 'sming-skel-master'

    def __init__(self, config):
        self.config = config
        if os.path.isabs(config.name):
            self.project_dir = config.name
        else:
            self.project_dir = os.path.abspath(config.name)
        self.has_git = subprocess.call('type git', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
        self.repo_created = False

    def run(self):
        self._sanity_check()
        self._download_skeleton()
        self._clean_skeleton()
        self._git_init()
        self._git_commit()

    def _sanity_check(self):
        if not self.config.skip_sanity_check:
            has_esphome = bool(os.environ.get('ESP_HOME'))
            has_sminghome = bool(os.environ.get('SMING_HOME'))
            if not has_esphome:
                print('ESP_HOME variable not found in environment')
            if not has_sminghome:
                print('SMING_HOME variable not found in environment')
            if not (has_esphome and has_sminghome):
                msg = 'One or more required variables not found in environment, continue anyway? [yY/nN] '
                try:
                    # python2
                    cont = raw_input(msg)  # noqa
                except AttributeError:
                    # python3
                    cont = input(msg)
                if not cont.lower() == 'y':
                    sys.exit(0)

    def _download_skeleton(self):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w'):
                urllib.urlretrieve(self.SKEL_ZIP_URL, path)
            tmp_dir = tempfile.mkdtemp()
            try:
                with zipfile.ZipFile(path, 'r') as archive:
                    archive.extractall(tmp_dir)
                if os.path.isdir(self.project_dir):
                    shutil.rmtree(self.project_dir)
                shutil.move(os.path.join(tmp_dir, self.SKEL_DIR_NAME), self.project_dir)
            finally:
                shutil.rmtree(tmp_dir)
        finally:
            os.remove(path)

    def _clean_skeleton(self):
        vscode_workspace = os.path.join(self.project_dir, '.vscode')
        shutil.rmtree(vscode_workspace)
        shutil.move(os.path.join(self.project_dir, 'vscode-project'), vscode_workspace)
        gitignore = os.path.join(self.project_dir, '.gitignore')
        shutil.move(os.path.join(self.project_dir, 'gitignore-project'), gitignore)
        if self.config.skip_license:
            os.remove(os.path.join(self.project_dir, 'LICENSE'))
        with open(os.path.join(self.project_dir, 'README.md'), 'w') as fp:
            fp.write('# %s' % self.config.name)

    def _git_init(self):
        if not self.config.skip_git_init:
            if not self.has_git:
                print('Git executable not present in $PATH')
                return
            cwd = os.getcwd()
            os.chdir(self.project_dir)
            try:
                subprocess.call('git init', shell=True)
                self.repo_created = True
            finally:
                os.chdir(cwd)

    def _git_commit(self):
        if self.repo_created and not self.config.skip_git_commit:
            cwd = os.getcwd()
            os.chdir(self.project_dir)
            try:
                subprocess.call('git add .', shell=True)
                subprocess.call('git commit -m"Initial commit"', shell=True)
            finally:
                os.chdir(cwd)


def main():
    arg_parser = make_argparser()
    config = arg_parser.parse_args()
    quickstart = Quickstart(config)
    quickstart.run()


if __name__ == '__main__':
    main()
