#!/usr/bin/env python3
"""Generate a Bubblewrap twa-manifest.json for the Master or Agent app.

Usage:
    make_twa_manifest.py <base_url> <owner> <repo> <master|agent>

Example:
    make_twa_manifest.py https://johnzayar.github.io/myrepo johnzayar myrepo master

Writes the JSON to stdout.
"""
import json
import re
import sys

def safe(s):
    s = re.sub(r'[^a-z0-9]', '', s.lower()) or 'app'
    # Android package segments must start with a LETTER (aapt2 rejects
    # digit- or underscore-leading segments), so prefix with 'a'.
    if not s[0].isalpha():
        s = 'a' + s
    return s

def main():
    base_url = sys.argv[1].rstrip('/')
    owner = sys.argv[2]
    repo = sys.argv[3]
    which = sys.argv[4]  # master | agent

    page = 'index.html' if which == 'master' else 'agent.html'
    name = '2D Master Pro' if which == 'master' else '2D Agent Pro'
    short = '2D Master' if which == 'master' else '2D Agent'

    manifest = {
        "packageId": "io.github.{}.{}.{}".format(safe(owner), safe(repo), which),
        "host": "{}.github.io".format(safe(owner)),
        "name": name,
        "launcherName": short,
        "display": "standalone",
        "orientation": "portrait",
        "themeColor": "#121622",
        "themeColorDark": "#121622",
        "navigationColor": "#121622",
        "navigationColorDark": "#121622",
        "navigationDividerColor": "#121622",
        "navigationDividerColorDark": "#121622",
        "backgroundColor": "#050505",
        "enableNotifications": False,
        "startUrl": "/{}/{}".format(repo, page),
        "iconUrl": "{}/icon-512.png".format(base_url),
        "splashScreenFadeOutDuration": 300,
        "signingKey": {
            "path": "android.keystore",
            "alias": "android"
        },
        "appVersion": "1.0.0",
        "appVersionCode": 1,
        "shortcuts": [],
        "generatorApp": "bubblewrap-cli",
        "webManifestUrl": "{}/manifest-{}.json".format(base_url, which),
        "fullScopeUrl": "{}/".format(base_url),
        "fallbackType": "customtabs",
        "features": {},
        "alphaDependencies": {"enabled": False},
        "enableSiteSettingsShortcut": True,
        "isChromeOSOnly": False,
        "isMetaQuest": False,
        "fingerprints": [],
        "additionalTrustedOrigins": [],
    }
    json.dump(manifest, sys.stdout, indent=2)
    sys.stdout.write("\n")

if __name__ == '__main__':
    main()
