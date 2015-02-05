# This is a template config file for b2g emulator unittest testing
import platform

HG_SHARE_BASE_DIR = "/builds/hg-shared"

if platform.system().lower() == 'darwin':
    xre_url = "http://tooltool.pvt.build.mozilla.org/build/sha512/314a6b9e177307950461bf3dd13a92a9ae4ceb35acc865e5bdff58a860f617e7b9bfb9485ab276a0a4ac82b1ea6c9ec60652d2f46dc5a7769c4a5f5d04d6dbcd"
else:
    xre_url = "http://tooltool.pvt.build.mozilla.org/build/sha512/64b655694963a05b9cf8ac7f2e7480898e6613714c9bedafc3236ef633ce76e726585d0a76dbe4b428b5142ce85bebe877b70b5daaecf073e592cb505690839f"

config = {
    # mozharness script options
    "xre_url": xre_url,

    # mozharness configuration
    "tooltool_servers": ["http://tooltool.pvt.build.mozilla.org/build/"],

    "vcs_share_base": HG_SHARE_BASE_DIR,
    "exes": {
        'python': '/tools/buildbot/bin/python',
        'virtualenv': ['/tools/buildbot/bin/python', '/tools/misc-python/virtualenv.py'],
        'tooltool.py': "/tools/tooltool.py",
    },

    "find_links": [
        "http://pypi.pvt.build.mozilla.org/pub",
        "http://pypi.pub.build.mozilla.org/pub",
    ],
    "pip_index": False,

    "buildbot_json_path": "buildprops.json",

    "default_actions": [
        'clobber',
        'read-buildbot-config',
        'pull',
        'download-and-extract',
        'create-virtualenv',
        'install',
        'run-tests',
    ],
    "vcs_output_timeout": 1760,
}
