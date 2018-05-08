%ifarch x86_64
%define bitmark	()(64bit)
%else
%define bitmark %nil
%endif

# same as upstream Adobe RPM
%define flash_libdir %{_libdir}/chromium-browser/PepperFlash

%define debug_package %{nil}

Summary:	Flash Player plugin for browsers
Name:		flash-player-plugin
Version:	29.0.0.140
Release:	2%{?dist}
License:	Proprietary
Group:		Networking/WWW
URL:		http://www.adobe.com/products/flashplayer/
# Use this script to download the RPMs and compute their sha256sum to paste below
Source0:	get-rpms.sh
ExclusiveArch:	%ix86 x86_64

Requires:	freshplayerplugin

# package fetching
Requires(pre):	curl

# helper for getting requires:
# for i in $(objdump -p libpepflashplayer.so  | grep NEEDED | awk '{ print $2 }' | grep -v ld-linux); do echo "Requires: $i%{bitmark}"; done | sort
Requires: libc.so.6%{bitmark}
Requires: libdl.so.2%{bitmark}
Requires: libgcc_s.so.1%{bitmark}
Requires: libm.so.6%{bitmark}
Requires: libpthread.so.0%{bitmark}
Requires: librt.so.1%{bitmark}
Requires: libstdc++.so.6%{bitmark}
# end of helper produced requires

Conflicts:	FlashPlayer < 9.0.115.0-5
Conflicts:	flash-plugin FlashPlayer-plugin flashplayer-plugin
Conflicts:	flash-player-npapi flash-player-ppapi
# Conflict with free plugins to avoid user confusion as to which one is
# actually used:
Conflicts:	gnash-firefox-plugin
Conflicts:	swfdec-mozilla
Conflicts:	lightspark-mozilla-plugin
Conflicts:	libflashsupport < 0.20080000.1
Obsoletes:	flash-player-plugin10.2 < 10.2.152
Provides:	flash-player-plugin11
Obsoletes:	flash-player-plugin11
Obsoletes:	flash-player-plugin-kde < 12
Obsoletes:	flash-player-plugin11-kde
BuildRoot:	%{_tmppath}/%{name}-root

%description
Adobe Flash Player plugin for browsers.

This package installs the PPAPI version and a freshplayerplugin wrapper
so that it will work on NPAPI browsers as well.

NOTE: This package does not contain the Flash Player itself. The
software will be automatically downloaded from Adobe during package
installation.

Installing this package indicates acceptance of the Flash Player EULA,
available at http://www.adobe.com/products/eulas/players/flash/
and at %{flash_libdir}/doc/license.pdf after installation.

%prep
%setup -q -c -T

# Always prefer versioned archives instead of unversioned ones, so that when
# Adobe updates the Flash Player, the old sha256sum continues to work until
# this package is updated for the new version.

# The linuxdownload.adobe.com rpm usually stays up longer, but fpdownload.macromedia.com is faster.
# Their sha256sums usually differ.

# IMPORTANT NOTES regarding the downurls and tsha256sums:
#
# - The downurls and tsha256sums are processed in sequence until %nil is encountered.
#   Therefore downurl3 is *not* processed if downurl2 is %nil!
#
# - downurls and tsha256sums are NOT correlated - there can be more urls than tsha256sums!
#   The download is considered validated if it matches *any* tsha256sum.

%ifarch %ix86
%define downurl1	http://fpdownload.adobe.com/get/flashplayer/pdc/%{version}/flash-player-ppapi-%{version}-release.i386.rpm
# (Anssi) this was up faster (i.e. at the time of writing it was up but downurl1 was not), but does not stay up very long, same sha256 as url1:
# %%define downurl2	http://fpdownload.adobe.com/get/flashplayer/current/licensing/linux/flash-player-ppapi-%{version}-release.i386.rpm
#define downurl2	%{nil}
# can be temporarily disabled by %nilling if not yet available at the time of updating:
%define downurl2	http://linuxdownload.adobe.com/linux/i386/flash-player-ppapi-%{version}-release.i386.rpm
%define downurl3	http://linuxdownload.adobe.com/linux/i386/flash-player-ppapi-%{version}-release.i386.rpm

# sha256sum:filesize
%define tsha256sum1	cfd7466f9f277476727438f3b7874788c632013be3e8cc7dcdeaff674afeb350:8534955
%define tsha256sum2	%{nil}
%define tsha256sum3	8ca45879d97a3e94afe56771c3c8905658df18835f0ec164945bc4177ee4320b:8535131

%define tarname		flash-player-ppapi-%{version}-release.i386.rpm

%define warn_on_missing_files 1
%endif

%ifarch x86_64
%define downurl1	http://fpdownload.adobe.com/get/flashplayer/pdc/%{version}/flash-player-ppapi-%{version}-release.x86_64.rpm
# %%define downurl2	http://fpdownload.adobe.com/get/flashplayer/current/licensing/linux/flash-player-ppapi-%{version}-release.x86_64.rpm
#define downurl2	%{nil}
%define downurl2	http://linuxdownload.adobe.com/linux/x86_64/flash-player-ppapi-%{version}-release.x86_64.rpm
%define downurl3	http://linuxdownload.adobe.com/linux/x86_64/flash-player-ppapi-%{version}-release.x86_64.rpm

%define tsha256sum1	452789d18faec80991b0348d9a64beebceb25b3d2bee466b4924daa5ea4fa407:9439972
%define tsha256sum2	%{nil}
%define tsha256sum3	b5e0bb3d6b58e5b8c1dc8541a007f020cd0ffc2f8f0313dfb7b66ebd12043fda:9440148

%define tarname		flash-player-ppapi-%{version}-release.x86_64.rpm

%define warn_on_missing_files 1
%endif

%define file %{_localstatedir}/lib/%{name}/%{tarname}

cat > README.%_real_vendor <<EOF
This package does not contain the Flash Player itself. The software is
automatically downloaded from Adobe during package installation.

This package requires the freshplayerplugin wrapper in
%{_libdir}/mozilla/plugins/libfreshwrapper-flashplayer.so which allows
the PPAPI plugin to be used on NPAPI browsers (e.g. Firefox) as well.
EOF

%build

%install
install -d -m755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m755 %{buildroot}%{flash_libdir}/doc

touch %{buildroot}%{flash_libdir}/libpepflashplayer.so
touch %{buildroot}%{flash_libdir}/manifest.json
touch %{buildroot}%{flash_libdir}/doc/LGPL.txt
touch %{buildroot}%{flash_libdir}/doc/readme.txt
touch %{buildroot}%{flash_libdir}/doc/notice.txt
touch %{buildroot}%{flash_libdir}/doc/license.pdf
touch %{buildroot}%{_localstatedir}/lib/%{name}/%{tarname}

install -d -m755 %{buildroot}%{_datadir}/%{name}
cat > %{buildroot}%{_datadir}/%{name}/functions << EOF
next_file() {
	FILENUM=\$((FILENUM+1))
	eval FILE_SRC="\\\$FILE\${FILENUM}_SRC"
	eval FILE_DST="\\\$FILE\${FILENUM}_DST"
	eval FILE_PRM="\\\$FILE\${FILENUM}_PRM"
	[ -n "\$FILE_SRC" ]
}

tar_extract() {
        extractdir=\$(mktemp -d --tmpdir=/tmp)
	if [ -z "\$extractdir" ]; then
		echo "Error during extraction." >&2
		exit 1
	fi

	cd "\$extractdir" || exit 1

	if [ "\$(head -c4 "%file")" = \$'\\xED\\xAB\\xEE\\xDB' ]; then
		rpm2cpio "%file" | cpio -i --quiet -d -R root:root
	else
		tar -xzf "%file" --no-same-owner --no-same-permissions
	fi

	# Avoid leaving old files in case of failure below
	FILENUM=0
	while next_file; do
		rm -f "\$FILE_DST"
	done

	FILENUM=0
	while next_file; do
		if [ ! -f "\$FILE_SRC" ]; then
%if %warn_on_missing_files
			echo "Warning: \$FILE_SRC not found in the Flash Player archive," >&2
			echo "         skipping installation of \$FILE_DST." >&2
			echo "         Please file a bug report at https://bugs.mageia.org/ ." >&2
%endif
			continue
		fi
			
		chmod "\$FILE_PRM" "\$FILE_SRC"
		mv -f "\$FILE_SRC" "\$FILE_DST"
	done
	rm -rf "\$extractdir"
}
EOF

%clean
rm -rf %{buildroot}

%pre
checksha256sum() {
	[ -e "$1" ] || return 1
	FILESHA256="$(sha256sum $1 | cut -d" " -f1)"
	FILESIZE="$(stat -c%%s "$1")"
	[ -n "$FILESHA256" ] || return 1
	[ -n "$FILESIZE" ] || return 1
	SHA256NUM=1
	eval SHA256SUM="\$SHA256SUM$SHA256NUM"
	while [ "$SHA256SUM" ]; do
		[ "${SHA256SUM%:*}" = "$FILESHA256" ] && [ "${SHA256SUM#*:}" = "$FILESIZE" ] && return 0
		SHA256NUM=$((SHA256NUM+1))
		eval SHA256SUM="\$SHA256SUM$SHA256NUM"
	done
	return 1
}

get_proxy_from_dnf() {
	if [ -e /etc/dnf/dnf.conf ]; then
		proxy="$(grep ^http_proxy= /etc/dnf/dnf.conf 2>/dev/null)"
		proxy_username="$(grep ^proxy_username= /etc/dnf/dnf.conf 2>/dev/null)"

		proxy="${proxy#http_proxy=}"
		proxy_username="${proxy_user#proxy_user=}"

		[ -n "$proxy" ] && echo "--proxy $proxy"
		[ -n "$proxy_username" ] && echo "--proxy-user $proxy_username"
	fi
}

SHA256SUM1="%{tsha256sum1}"
SHA256SUM2="%{tsha256sum2}"
SHA256SUM3="%{tsha256sum3}"
SHA256SUM4=
URL1="%{downurl1}"
URL2="%{downurl2}"
URL3="%{downurl3}"
URL4=

URLNUM=1

install -d -m 0755 %{_localstatedir}/lib/%{name}

echo "Note that by downloading the Adobe Flash Player you indicate your acceptance of"
echo "the EULA, available at http://www.adobe.com/products/eulas/players/flash/"
while ! checksha256sum "%file"; do
	eval URL="\$URL$URLNUM"
	if [ -z "$URL" ]; then
		echo "Error: Unable to download Flash Player. This is likely due to this package" >&2
		echo "       being too old. Please file a bug report at https://bugs.mageia.org" >&2
		echo "       so that the package gets updated. Thank you." >&2
		echo "" >&2
		echo "       In the meantime, you can download Flash Player manually from" >&2
		echo "       http://get.adobe.com/flashplayer/" >&2
		rm -f "%file"
		[ "$(ls -A "%{_localstatedir}/lib/%{name}")" ] && rm -rf "%{_localstatedir}/lib/%{name}"
		[[ -n $DURING_INSTALL ]] && exit 0 || exit 1
	fi
	URLNUM=$((URLNUM+1))
	echo "Downloading from $URL:"
	curl --connect-timeout 20 -m 10800 -L $(get_proxy_from_dnf) "$URL" > "%file"
done

%post
FILE1_SRC="usr/%{_lib}/flash-plugin/libpepflashplayer.so"
FILE1_DST="%{flash_libdir}/libpepflashplayer.so"
FILE1_PRM="0755"

FILE2_SRC="usr/share/doc/flash-player-ppapi-%{version}/license.pdf"
FILE2_DST="%{flash_libdir}/doc/license.pdf"
FILE2_PRM="0644"
FILE3_SRC="usr/share/doc/flash-player-ppapi-%{version}/readme.txt"
FILE3_DST="%{flash_libdir}/doc/readme.txt"
FILE3_PRM="0644"
FILE4_SRC="usr/share/doc/flash-player-ppapi-%{version}/notice.txt"
FILE4_DST="%{flash_libdir}/doc/notice.txt"
FILE4_PRM="0644"
FILE5_SRC="usr/share/doc/flash-player-ppapi-%{version}/LGPL.txt"
FILE5_DST="%{flash_libdir}/doc/LGPL.txt"
FILE5_PRM="0644"

FILE6_SRC="usr/%{_lib}/flash-plugin/manifest.json"
FILE6_DST="%{flash_libdir}/manifest.json"
FILE6_PRM="0644"

FILE7_SRC=

. %{_datadir}/%{name}/functions
tar_extract

# Make Firefox see that the plugin has been updated
# (this file has %verify(not mtime) set):
touch --no-create %{_libdir}/mozilla/plugins/libfreshwrapper-flashplayer.so

echo "Adobe Flash Player installation successful."

%files
%doc README.%_real_vendor

%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}/%{tarname}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/functions

%dir %{flash_libdir}
%dir %{flash_libdir}/doc
%ghost %{flash_libdir}/libpepflashplayer.so
%ghost %{flash_libdir}/manifest.json
%ghost %{flash_libdir}/doc/license.pdf
%ghost %{flash_libdir}/doc/readme.txt
%ghost %{flash_libdir}/doc/notice.txt
%ghost %{flash_libdir}/doc/LGPL.txt
