# ubnt-unifi-diy

# UBNT UniFi Controller - DIY Package Updater

### What does it do?
This project is a simple update script to retrieve the DIY package for the Ubiquiti Networks UniFi Controller. At some point, UBNT stopped publishing the links to the DIY version of the package with the rest of the new releases; however, the releases are still available if you know where to look.

They use a consistent version string in the download link, which is in lockstep with the standard release downloads.

What this script does is - checks the version numbers of the “Stable” and “LTS” versions of the Controller as reported by UBNT, - generates the download links, - - compares the filenames to files already stored locally, and - retrieves the new files, if they’re not locally available.

### Why?
Because it is tedious to do this manually for each release cycle, and if you’re a good SE like me, you’re always looking for ways to offload tedius tasks to machines. They happen to be quite good at repetitive, tedious tasks and are also content to do so.
