%global security_hardening none
%global debug_package %{nil}
Summary:        U-Boot EFI firmware
Name:		u-boot
Version:	2020.07
Release:	3%{?dist}
License:	GPLv2
Url:            http://www.denx.de/wiki/U-Boot
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
%define sha1 u-boot=1b59dd6875b0ceeb5202ef027f26bf3c99a8d91b
Source1:        rpi_3_photon_defconfig
Source2:        fw_env.config
Patch0:		0001-XXX-openSUSE-XXX-Load-dtb-from-part.patch
Patch1:		0004-Fix-MMC1-external-SD-slot-on-Samsun.patch
Patch2:		0005-Fix-no-usb.patch
Patch3:         add-saveenv-in-bootcmd.patch

Group:          Development/Tools
BuildArch:      aarch64

%description
U-Boot is Open Source Firmware.

%package -n     u-boot-utils
Summary:        U Boot Utilitiy for rpi3

%description -n u-boot-utils
This utility will provide the binary to modify the u boot
env variables from linux shell prompt.

%prep
%setup -q -n u-boot-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp %{SOURCE1} configs/
make %{?_smp_mflags} CROSS_COMPILE= rpi_3_photon_defconfig
make %{?_smp_mflags} CROSS_COMPILE= USE_PRIVATE_LIBGG=yes
make %{?_smp_mflags} CROSS_COMPILE= USE_PRIVATE_LIBGG=yes envtools

%install
install -D -m 0644 u-boot.bin %{buildroot}/boot/efi/u-boot.bin
install -D -m 0744 tools/env/fw_printenv %{buildroot}/usr/bin/fw_setenv
install -D -m 0644 %{SOURCE2} %{buildroot}/etc/fw_env.config

%files
%defattr(-,root,root)
/boot/efi/*

%files -n u-boot-utils
/etc/fw_env.config
/usr/bin/fw_setenv

%changelog
*   Thu Aug 06 2020 Sujay G <gsujay@vmware.com> 2020.07-3
-   Removed add_tcp_wget_support.patch, not compatible with 2020.07 version
*   Tue Jul 28 2020 Sujay G <gsujay@vmware.com> 2020.07-2
-   Update checksum value
*   Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2020.07-1
-   Automatic Version Bump
*   Thu Oct 31 2019 Alexey Makhalov <amakhalov@vmware.com> 2019.10-2
-   Move /boot/esp/u-boot.bin to /boot/efi/u-boot.bin.
*   Thu Oct 10 2019 Ajay Kaher <akaher@vmware.com> 2019.10-1
-   Updating to 2019.10
*   Thu Aug 22 2019 Ajay Kaher <akaher@vmware.com> 2019.01-4
-   Fix CVE-2019-13104, CVE-2019-13106
*   Wed Aug 07 2019 Kuladeep Rayalla <krayalla@vmware.com> 2019.01-3
-   Fix CVE-2019-13103: disk: stop infinite recursion in DOS Partitions
*   Wed May 15 2019 Ajay Kaher <akaher@vmware.com> 2019.01-2
-   Fix CVE-2019-11059
*   Fri Feb 22 2019 Tapas Kundu <tkundu@vmware.com> 2019.01-1
-   Updating to 2019.01
-   Added patch for tcp and wget support
-   Added u-boot-utils as subpackage
*   Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 2018.09-7
-   Renamed package from u-boot-rpi3 to u-boot.
*   Fri Nov 23 2018 Ajay Kaher <akaher@vmware.com> 2018.09-6
-   Enable USB_KEYBAORD which has CONTROL_EP
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 2018.09-5
-   Adding BuildArch
*   Mon Oct 22 2018 Alexey Makhalov <amakhalov@vmware.com> 2018.09-4
-   Remove bc, swig, python, openssl buildrequires.
-   Remove doc subpackage.
*   Mon Oct 15 2018 Ajay Kaher <akaher@vmware.com> 2018.09-3
-   Set bootdelay to zero in rpi_3_photon_defconfig
*   Mon Oct 08 2018 Ajay Kaher <akaher@vmware.com> 2018.09-2
-   Disable USB to improve boot time.
*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 2018.09-1
-   Version update to 2018.09
*   Wed Jul 25 2018 Ajay Kaher <akaher@vmware.com> 2018.07-1
-   Version update to u-boot-rpi3-2018.07-1
*   Fri Dec 15 2017 Alexey Makhalov <amakhalov@vmware.com> 2017.11-1
-   Based on OpenSuse u-boot-rpi3-2017.11-266.2 from Thu Nov 16 2017
    by guillaume@opensuse.org
