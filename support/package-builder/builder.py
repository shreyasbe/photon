#!/usr/bin/env python

from optparse import OptionParser
import os.path
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager 
import json
import sys

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = OptionParser(usage)
    parser.add_option("-s",  "--spec-path",  dest="specPath",  default="/workspace1/myrepos/photon/SPECS")
    parser.add_option("-x",  "--source-path",  dest="sourcePath",  default="/workspace1/mysources")
    parser.add_option("-r",  "--rpm-path",  dest="rpmPath",  default="/workspace1/mystage/RPMS")
    parser.add_option("-i",  "--install-package", dest="installPackage",  default=False,  action ="store_true")
    parser.add_option("-p",  "--publish-RPMS-path", dest="publishRPMSPath",  default="/workspace1/testTP1RPMS/RPMS")
    parser.add_option("-l",  "--log-path", dest="logPath",  default="/workspace1/LOGS")
    parser.add_option("-o",  "--build-option", dest="buildOption",  default="full")
    parser.add_option("-z",  "--top-dir-path", dest="topDirPath",  default="/usr/src/photon")
    parser.add_option("-j",  "--json-file", dest="inputJSONFile",  default="input.json")
    parser.add_option("-b",  "--build-root-path", dest="buildRootPath",  default="/mnt")
    parser.add_option("-e",  "--parallel-build", dest="parallelBuild",  default=False)
    
    
    (options,  args) = parser.parse_args()
    cmdUtils=CommandUtils()
    if not os.path.isdir(options.logPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.logPath)
    
    if options.parallelBuild in ["TRUE", "True", "true"]:
        parallelBuild = True
    else:
        parallelBuild = False

    logger=Logger.getLogger(options.logPath+"/Main")
    
    errorFlag=False
    package = None
    if not os.path.isdir(options.sourcePath):
        logger.error("Given Sources Path is not a directory:"+options.sourcePath)
        errorFlag = True
    if not os.path.isdir(options.specPath):
        logger.error("Given Specs Path is not a directory:"+options.specPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath):
        logger.error("Given RPMS Path is not a directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/x86_64"):
        logger.error("Given RPMS Path is missing x86_64 sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/noarch"):
        logger.error("Given RPMS Path is missing noarch sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    
    if not os.path.isfile(options.inputJSONFile) and not options.installPackage:
        logger.error("Given JSON File is not a file:"+options.inputJSONFile)
        errorFlag = True
        
    if options.installPackage :
        if len(args) != 1:
            logger.error("Please provide package name")
            errorFlag = True
        else:
            package=args[0]
        
    if errorFlag:
        logger.error("Found some errors. Please fix input options and re-run it.")
        return False
    
    
    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")
    
    if not os.path.isdir(options.buildRootPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.buildRootPath)
    
    logger.info("Source Path :"+options.sourcePath)
    logger.info("Spec Path :" + options.specPath)
    logger.info("Rpm Path :" + options.rpmPath)
    logger.info("Log Path :" + options.logPath)
    logger.info("Top Dir Path :" + options.topDirPath)
    logger.info("Publish RPMS Path :" + options.publishRPMSPath)
    if not options.installPackage:
        logger.info("JSON File :" + options.inputJSONFile)
    else:
        logger.info("Package to build:"+package)

    '''    
    listPackages=["acl","attr","autoconf","automake","bash","bc","bindutils","binutils","bison","boost","btrfs-progs","bzip2","ca-certificates","cdrkit","check",
                  "cloud-init","cmake","coreutils","cpio","cracklib","createrepo","curl","cyrus-sasl","db","dbus","deltarpm","diffutils","docbook-xml","docbook-xsl",
                  "docker","dparted","dracut","e2fsprogs","elfutils","etcd","expat","file","filesystem","findutils","flex","gawk","gcc","gdb","gdbm","gettext","git",
                  "glib","glibc","glibmm","gmp","go","gobject-introspection","google-daemon","google-startup-scripts","gperf","gpgme","gptfdisk","grep","groff",
                  "grub","gtk-doc","gzip","haveged","hawkey","iana-etc","inetutils","intltool","iproute2","iptables","itstool","json-glib","kbd","kmod","krb5",
                  "kubernetes","less","libaio","libassuan","libcap","libdnet","libffi","libgpg-error","libgsystem","libhif","libmspack","libpcap","libpipeline",
                  "librepo","libselinux","libsepol","libsigc++","libsolv","libtool","libxml2","libxslt","libyaml","linux","linux-api-headers","Linux-PAM","lua",
                  "lvm2","lzo","m4","make","man-db","man-pages","mercurial","mpc","mpfr","nano","ncurses","nspr","nss","ntp","openldap","openssh","openssl",
                  "open-vm-tools","ostree","parted","patch","pcre","perl","perl-common-sense","perl-Config-IniFiles","perl-DBD-SQLite","perl-DBI","perl-DBIx-Simple",
                  "perl-Exporter-Tiny","perl-JSON-XS","perl-libintl","perl-List-MoreUtils","perl-Module-Install","perl-Module-ScanDeps","perl-Types-Serialiser",
                  "perl-WWW-Curl","perl-YAML","perl-YAML-Tiny","photon-release","pkg-config","popt","procps-ng","psmisc","pycurl","pygobject","python2",
                  "python-configobj","python-iniparse","python-jsonpatch","python-jsonpointer","python-prettytable","python-requests","python-setuptools",
                  "python-six","PyYAML","readline","rocket","rpm","rpm-ostree","rpm-ostree-toolbox","ruby","sed","shadow","sqlite-autoconf","strace","sudo",
                  "swig","systemd","tar","tcpdump","tcsh","tdnf","texinfo","thin-provisioning-tools","tzdata","unzip","urlgrabber","util-linux","vim","wget",
                  "which","xerces-c","XML-Parser","xml-security-c","xz","yum","yum-metadata-parser","zlib"]
    '''
    try:
        constants.initialize(options)
        if options.installPackage:
            buildAPackage(package, parallelBuild)
        else:
            buildPackagesFromGivenJSONFile(options.inputJSONFile, options.buildOption,logger, parallelBuild)
    except Exception as e:
        logger.error("Caught an exception")
        logger.error(str(e))
        sys.exit(1)
    
    sys.exit(0)

def buildAPackage(package, parallelBuild):
    listPackages=[]
    listPackages.append(package)
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackages, parallelBuild)

def buildPackagesFromGivenJSONFile(inputJSONFile,buildOption,logger, parallelBuild):
    listPackages = get_all_package_names(inputJSONFile)

    listPackagesToBuild=[]
    for pkg in listPackages:
        p =  pkg.encode('utf-8')
        listPackagesToBuild.append(str(p))
    logger.info("List of packages to build:")
    logger.info(listPackagesToBuild)
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackagesToBuild, parallelBuild)
    
def get_all_package_names(build_install_option):
    base_path = os.path.dirname(build_install_option)
    jsonData = open(build_install_option)
    option_list_json = json.load(jsonData)
    jsonData.close()
    options_sorted = sorted(option_list_json.items(), key=lambda item: item[1]['order'])
    packages = []

    for install_option in options_sorted:
        filename = os.path.join(base_path, install_option[1]["file"])
        jsonData=open(filename)
        package_list_json = json.load(jsonData)
        jsonData.close()
        packages = packages + package_list_json["packages"]

    return packages

if __name__=="__main__":
    main()
