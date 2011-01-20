#!/usr/bin/env python
"""multi_locale_build.py

This should be a mostly generic multilocale build script.
"""

import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(sys.path[0])))

from mozharness.base.errors import SSHErrorList, PythonErrorList, MakefileErrorList
from mozharness.base.script import MercurialScript
from mozharness.l10n.locales import LocalesMixin



# MultiLocaleBuild {{{1
class MultiLocaleBuild(LocalesMixin, MercurialScript):
    config_options = [[
     ["--locale",],
     {"action": "extend",
      "dest": "locales",
      "type": "string",
      "help": "Specify the locale(s) to repack"
     }
    ],[
     ["--merge-locales",],
     {"action": "store_true",
      "dest": "merge_locales",
      "default": False,
      "help": "Use default [en-US] if there are missing strings"
     }
    ],[
     ["--no-merge-locales",],
     {"action": "store_false",
      "dest": "merge_locales",
      "help": "Do not allow missing strings"
     }
    ],[
     ["--objdir",],
     {"action": "store",
      "dest": "objdir",
      "type": "string",
      "default": "objdir",
      "help": "Specify the objdir"
     }
    ],[
     ["--l10n-base",],
     {"action": "store",
      "dest": "hg_l10n_base",
      "type": "string",
      "help": "Specify the L10n repo base directory"
     }
    ],[
     ["--l10n-tag",],
     {"action": "store",
      "dest": "hg_l10n_tag",
      "type": "string",
      "help": "Specify the L10n tag"
     }
    ],[
     ["--l10n-dir",],
     {"action": "store",
      "dest": "l10n_dir",
      "type": "string",
      "default": "l10n",
      "help": "Specify the l10n dir name"
     }
    ]]

    def __init__(self, require_config_file=True):
        LocalesMixin.__init__(self)
        MercurialScript.__init__(self, config_options=self.config_options,
                                 all_actions=['clobber', 'pull-build-source',
                                              'pull-locale-source',
                                              'build', 'package-en-US',
                                              'upload-en-US',
                                              'add-locales', 'package-multi',
                                              'upload-multi'],
                                 require_config_file=require_config_file)

    def clobber(self):
        c = self.config
        if c['work_dir'] != '.':
            path = os.path.join(c['base_work_dir'], c['work_dir'])
            if os.path.exists(path):
                self.rmtree(path, error_level='fatal')
        else:
            self.info("work_dir is '.'; skipping for now.")

    def pull_build_source(self):
        c = self.config
        dirs = self.query_abs_dirs()
        self.scm_checkout_repos(c['repos'])

    def pull_locale_source(self):
        self.mkdir_p(dirs['abs_l10n_dir'])
        locales = self.query_locales()
        locale_repos = []
        for locale in locales:
            locale_dict = {
                
            }
            tag = c['hg_l10n_tag']
            if hasattr(self, 'locale_dict'):
                tag = self.locale_dict[locale]
            locale_repos.append({
                'repo': "%s/%s" % (c['hg_l10n_base'], locale),
                'tag': tag
            })
        self.scm_checkout_repos(repo_list=locale_repos,
                                parent_dir=dirs['abs_l10n_dir'])

    def build(self):
        c = self.config
        dirs = self.query_abs_dirs()
        self.copyfile(os.path.join(dirs['abs_work_dir'], c['mozconfig']),
                      os.path.join(dirs['abs_mozilla_dir'], 'mozconfig'),
                      error_level='fatal')
        command = "make -f client.mk build"
        env = self.query_env()
        self._process_command(command=command, cwd=dirs['abs_mozilla_dir'],
                              env=env, error_list=MakefileErrorList,
                              halt_on_failure=True)

    def add_locales(self):
        if 'add-locales' not in self.actions:
            self.action_message("Skipping add-locales step.")
            return
        self.action_message("Adding locales to the apk.")
        c = self.config
        dirs = self.query_abs_dirs()
        locales = self.query_locales()

        for locale in locales:
            self.run_compare_locales(locale, halt_on_failure=True)
            command = 'make chrome-%s L10NBASEDIR=%s' % (locale, dirs['abs_l10n_dir'])
            if c['merge_locales']:
                command += " LOCALE_MERGEDIR=%s" % dirs['abs_merge_dir']
                self.run_command(command, cwd=dirs['abs_locales_dir'],
                                 error_list=MakefileErrorList,
                                 halt_on_failure=True)

    def package_en_US(self):
        self.package(package_type='en-US')

    def package_multi(self):
        self.package(package_type='multi')

    def package(self, package_type='en-US'):
        c = self.config
        dirs = self.query_abs_dirs()

        command = "make package"
        env = self.query_env()
        if package_type == 'multi':
            command += " AB_CD=multi"
            env['MOZ_CHROME_MULTILOCALE'] = "en-US " + \
                                            ' '.join(self.query_locales())
            self.info("MOZ_CHROME_MULTILOCALE is %s" % env['MOZ_CHROME_MULTILOCALE'])
        # TODO remove once bug 611648 fixed
        if 'jarsigner' in c:
            env['JARSIGNER'] = os.path.join(dirs['abs_work_dir'],
                                            c['jarsigner'])
        status = self.run_command(command, cwd=dirs['abs_objdir'], env=env,
                                  error_list=MakefileErrorList,
                                  halt_on_failure=True)
        command = "make package-tests"
        if package_type == 'multi':
            command += " AB_CD=multi"
        status = self.run_command(command, cwd=dirs['abs_objdir'], env=env,
                                  error_list=MakefileErrorList,
                                  halt_on_failure=True)

    def upload_en_US(self):
        # TODO
        self.info("Not written yet.")

    def upload_multi(self):
        # TODO
        self.info("Not written yet.")

    def _process_command(self, **kwargs):
        """Stub wrapper function that allows us to call scratchbox in
           MaemoMultiLocaleBuild.

        """
        return self.run_command(**kwargs)

# __main__ {{{1
if __name__ == '__main__':
    pass
