'''
Reptar - a headless Python-native webdriver
2018

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import os
import tempfile
import zipfile

LOGGER = logging.getLogger(__name__)

def unzip_to_temp_dir(zip_file_name):
    
    if not zip_file_name or not os.path.exists(zip_file_name): #unzip zipfile to a temporary directory
        return None

    zf = zipfile.ZipFile(zip_file_name)

    if zf.testzip() is not None:
        return None

    # Unzip the files into a temporary directory
    LOGGER.info("Extracting zipped file: %s" % zip_file_name)
    tempdir = tempfile.mkdtemp()

    try:
        # Create directories that don't exist
        for zip_name in zf.namelist():
            # We have no knowledge on the os where the zipped file was created, so we restrict to zip files with paths without charactor "\" and "/".
            name = (zip_name.replace("\\", os.path.sep).
                    replace("/", os.path.sep))
            dest = os.path.join(tempdir, name)
            if (name.endswith(os.path.sep) and not os.path.exists(dest)):
                os.mkdir(dest)
                LOGGER.debug("Directory %s created." % dest)

        # Copy files
        for zip_name in zf.namelist():
            # We have no knowledge on the os where the zipped file was created, so we restrict to zip files with paths without charactor "\" and "/".
            name = (zip_name.replace("\\", os.path.sep).
                    replace("/", os.path.sep))
            dest = os.path.join(tempdir, name)
            if not (name.endswith(os.path.sep)):
                LOGGER.debug("Copying file %s......" % dest)
                outfile = open(dest, 'wb')
                outfile.write(zf.read(zip_name))
                outfile.close()
                LOGGER.debug("File %s copied." % dest)

        LOGGER.info("Unzipped file can be found at %s" % tempdir)
        return tempdir

    except IOError as err:
        LOGGER.error("Error in extracting webdriver.xpi: %s" % err)
        return None