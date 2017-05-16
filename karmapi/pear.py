"""If a karma pi does not have the data it is asked for it has a
couple of choices.

If it has the stuff needed to build it then it can do just that.

If there is another karma pi that already has the data it can just
ask for a copy,

So any karma pi can have one or more peers that it gets and shares
data with.

These things tend to come in pairs.

So we have peer and pair, so lets call it pear.

For now, Pear's just try to retrieve the thing at path and save it
locally.

"""
from pathlib import Path
import shutil

from requests import get, put

from karmapi import base

import paramiko

class Pear:

    def __init__(self, url):

        self.url = url

    def get(self, path):

        path = Path(path)
        response = get(self.url + path.as_posix())
        if response.status_code != 200:
            raise AttributeError('Status code: {}'.format(
                response.status_code))

        return response.content


    def save(self, path, content):

        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_bytes(content)

        return content

    def mirror(self, path, overwrite=False):

        path = Path(path)

        if path.exists() and not overwrite:
            return False

        content = self.get(path)

        self.save(path, content)

        return True


class LocalPear:

    def __init__(self, folder):

        self.folder = Path(folder)

    def get(self, path):

        path = self.folder / path

        with path.open() as infile:
            content = infile.read()
        
        return content

    def mirror(self, path):

        shutil.copy(str(self.folder / path), str(path))



class SshPear:


    def __init__(self, host, folder, user=None):

        self.folder = Path(folder)
        self.client = paramiko.SSHClient()

        self.client.load_system_host_keys()
        #self.client.set_missing_host_key_policy(
        #    paramiko.client.WarningPolicy)
        self.client.connect(host, username=user)

    def get(self, path):

        path = self.folder / path

        with self.client.open_sftp() as sftp:
            
            content = sftp.get(path)
        
        return content

    def mirror(self, path):

        shutil.copy(str(self.folder / path), str(path))
        
