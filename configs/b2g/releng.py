#!/usr/bin/env python
import os
config = {
    "default_actions": [
        'clobber',
        'checkout-sources',
        'get-blobs',
        'update-source-manifest',
        'build',
        'build-symbols',
        'make-updates',
        'make-socorro-json',
        'prep-upload',
        'upload',
        'upload-source-manifest',
    ],
    "ssh_key": os.path.expanduser("~/.ssh/b2gbld_dsa"),
    "ssh_user": "b2gbld",
    "upload_remote_host": "pvtbuilds2.dmz.scl3.mozilla.com",
    "upload_remote_basepath": "/pub/mozilla.org/b2g/tinderbox-builds",
    "upload_remote_nightly_basepath": "/pub/mozilla.org/b2g/nightly",
    "upload_dep_target_exclusions": ["unagi", "otoro"],
    "tooltool_servers": ["http://runtime-binaries.pvt.build.mozilla.org/tooltool/"],
    "gittool_share_base": "/builds/git-shared/git",
    "gittool_base_mirror_urls": [],
    "hgtool_share_base": "/builds/hg-shared",
    "hgtool_base_mirror_urls": ["http://hg-internal.dmz.scl3.mozilla.com"],
    "hgtool_base_bundle_urls": ["http://ftp.mozilla.org/pub/mozilla.org/firefox/bundles"],
    "sendchange_masters": ["buildbot-master36.build.mozilla.org:9301"],
    "exes": {
        "tooltool.py": "/tools/tooltool.py",
        "buildbot": "/tools/buildbot/bin/buildbot",
    },
    "manifest": {
        "upload_remote_host": "stage.mozilla.org",
        "upload_remote_basepath": "/pub/mozilla.org/b2g/manifests/%(version)s",
        "ssh_key": os.path.expanduser("~/.ssh/b2gbld_dsa"),
        "ssh_user": "b2gbld",
        "branches": {
            'mozilla-b2g18_v1_0_0': '1.0.0',
            'mozilla-b2g18_v1_0_1': '1.0.1',
            'mozilla-b2g18': '1.1.0',
            'mozilla-central': '2.0.0',
        },
        "translate_hg_to_git": True,
        "translate_base_url": "http://cruncher.build.mozilla.org/mapper",
    },
    "env": {
        "CCACHE_DIR": "/builds/ccache",
        "CCACHE_COMPRESS": "1",
        "CCACHE_UMASK": "002",
        "PRODUCTION": "1",
        "GAIA_OPTIMIZE": "1",
        "SYMBOL_SERVER_HOST": "symbolpush.mozilla.org",
        "SYMBOL_SERVER_USER": "b2gbld",
        "SYMBOL_SERVER_SSH_KEY": "/home/mock_mozilla/.ssh/b2gbld_dsa",
        "SYMBOL_SERVER_PATH": "/mnt/netapp/breakpad/symbols_b2g/",
        "POST_SYMBOL_UPLOAD_CMD": "/usr/local/bin/post-symbol-upload.py",
    },
    "purge_minsize": 15,
    "clobberer_url": "http://clobberer.pvt.build.mozilla.org/index.php",
    "is_automation": True,
    "repo_mirror_dir": "/builds/git-shared/repo",
    "repo_remote_mappings": {
        'https://android.googlesource.com/': 'https://git.mozilla.org/external/aosp',
        'git://codeaurora.org/': 'https://git.mozilla.org/external/caf',
        'https://git.mozilla.org/b2g': 'https://git.mozilla.org/b2g',
        'git://github.com/mozilla-b2g/': 'https://git.mozilla.org/b2g',
        'git://github.com/mozilla/': 'https://git.mozilla.org/b2g',
        'https://git.mozilla.org/releases': 'https://git.mozilla.org/releases',
        'http://android.git.linaro.org/git-ro/': 'https://git.mozilla.org/external/linaro',
        'git://github.com/apitrace/': 'https://git.mozilla.org/external/apitrace',
    },
}
