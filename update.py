#!/usr/local/bin/python2

import os
import sys
import urllib2
from urllib2 import urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
from io import BytesIO

CURRENT_VERSIONS = "https://help.ubnt.com/hc/en-us/articles/115000441548-UniFi-Current-Controller-Versions"
DOWNLOAD_BASEURL = "https://www.ubnt.com/downloads/unifi/%%VER%%/UniFi.unix.zip"
REQUESTED_RELEASES = ['LTS', 'Stable']
EXCLUDE_RELEASES = ['Stable Candidate']
ARCHIVE_DIR = './archive'
REPO_DIR = './repo'

def checkPaths ():
  # Ensure that the required paths are valid and if not, create them
  paths = [ARCHIVE_DIR, REPO_DIR]
  for path in paths:
    try:
      if not os.path.exists(path):
        os.makedirs(path)
    except:
      print "Error creating directory %s" % (path)

def getVersions (releases):
  # Request the current versions page from UBNT, looking for the branches/releases in "REQUESTED_RELEASES"
  versions = {}
  url = CURRENT_VERSIONS
  html_page = urllib2.urlopen(url)
  soup = BeautifulSoup(html_page)
  for rel in releases:
    # Look through the HTML table and find the rows containing the desired branches/releases
    for tr in soup.findAll('tr'):
      spans = tr.findAll('span')
      for span in spans:
        if span.string and rel in span.string and span.string not in EXCLUDE_RELEASES:
          # If the branch/release string matches, and isn't in the exclude list, grab the label from the HREF in that row.
          # This text string is the version number we use to build the download link for the DIY tarball.
          for link in tr.findAll('a'):
            versions[span.string] = link.string
  return versions

def downloadVersion (rel, releases):
  # Get the version number of the branch/release
  ver = releases[rel]
  # Make sure destination paths are good before doing stuff with files
  checkPaths()
  # Set the output file based on the branch name and version
  outfile = "UniFi.%s-%s.unix.zip" % (rel, ver)
  outpath = "%s/%s" % (REPO_DIR, outfile)
  # Shim the version information into the download URL
  url = DOWNLOAD_BASEURL.replace('%%VER%%', ver)
  # Check to see if we already have these files. Bandwidth isn't free!
  # It would be better if this was a hashing mechanism, but I haven't found where UBNT keeps the hash values.
  for file in os.listdir(REPO_DIR):
    if file == ("%s" % outfile):
      print " - File already exists: %s/%s" % (REPO_DIR, outfile)
      return 1
  # If we don't have a file with a matching name, download the file from UBNT.
  if dlfile(url, "%s/.%s" % (REPO_DIR, outfile)):
    print " - Downloaded %s to %s" % (ver, outpath)
    # Once the download is complete, move it from .FILENAME to FILENAME.
    # This would also be a good place to compare a checksum, if we can find it.
    # Match = rename, no match = delete and error.
    os.rename("%s/.%s" % (REPO_DIR, outfile), "%s/%s" % (REPO_DIR, outfile))

def dlfile(url,outpath):
  try:
    # Attempt download using urrllib2
    f = urlopen(url)
    print " - Downloading from " + url
    with open(outpath, "wb") as local_file:
      local_file.write(f.read())
    # If successful, return to parent.
    return 1
  # Throw errors if we have problems
  except HTTPError, e:
    print "HTTP Error: ", e.code, url
    return 0
  except URLError, e:
    print "URL Error: ", e.reason, url
    return 0

sys.stdout.flush()
print ""
print "Requesting list of releases from UBNT..."
print " - (%s)" % CURRENT_VERSIONS
# Pull the current branch/release information into a dict for use later.
releases = getVersions(REQUESTED_RELEASES)
# Iterate through desired branches/releases and make sure we have the current version.
for rel in REQUESTED_RELEASES:
  print "Searching for %s version %s" % (rel, releases[rel])
  downloadVersion(rel, releases)
print ""
