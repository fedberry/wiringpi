%global commit_long     96344ff7125182989f98d3be8d111952a8f74e15
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})

Name:		wiringpi
Version:	2.44
Release:	1.%{commit_short}%{dist}
Summary:	WiringPi is a Wiring library written in C and should be usable from C++.

License:	GPLv3
URL:		https://git.drogon.net/?p=wiringPi
#Source0:	https://git.drogon.net/?p=wiringPi;a=snapshot;h=refs/heads/master;sf=tgz
Source0:	https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_long};sf=tgz#/wiringPi-%{commit_short}.tar.gz
Patch0:		wiringPi-make.patch
ExclusiveArch: %{arm}

%description
WiringPi is a Wiring library written in C and should be usable from C++.

%prep
%setup -q -n wiringPi-%{commit_short}
%patch0 -p1 -b .orig

%build
%{?__global_ldflags:LDFLAGS="%__global_ldflags"}

echo "Build WiringPi library"
pushd wiringPi
make %{?_smp_mflags} DEBUG="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS"
popd

echo "Build WiringPi Devices Library"
pushd devLib
make %{?_smp_mflags} DEBUG="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS"
popd

echo "Build GPIO Utility"
pushd gpio
make %{?_smp_mflags} DEBUG="$RPM_OPT_FLAGS"\
 LDFLAGS="-L../wiringPi -L../devLib $LDFLAGS"\
 C_INCLUDE_PATH=../wiringPi:../devLib:$C_INCLUDE_PATH
popd

%install
rm -rf %{buildroot}

echo "Install WiringPi library"
pushd wiringPi
make install-fedora DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
popd

echo "Install WiringPi Devices Library"
pushd devLib
make install-fedora DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
popd

echo "Install GPIO Utility"
pushd gpio
make install-fedora DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
popd

pushd $RPM_BUILD_ROOT/%{_libdir}
ln -sf libwiringPi.so.%{version} libwiringPi.so
ln -sf libwiringPiDev.so.%{version} libwiringPiDev.so
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.LESSER INSTALL People README.TXT VERSION
%attr(4755,root,root) %{_bindir}/gpio
%{_includedir}/wiringPi
%{_libdir}/libwiringPi.so*
%{_libdir}/libwiringPiDev.so*
%{_mandir}/man1/*.1.*

%changelog
* Thu Jul 13 2017 Vaughan <devel at agrez.net> - 2.44-1.96344ff
- New release 2.44 (git snapshot: 96344ff7125182989f98d3be8d111952a8f74e15)

* Mon Jan 02 2017 Vaughan <devel at agrez.net> - 2.36-1.b1dfc18
- New release 2.36 (git snapshot: b1dfc186efe327aa1d59de43ef631a2fa24e7c95)
- Don't limit Exclusive arch to just armv7hl

* Mon Mar 07 2016 Vaughan <devel at agrez.net> - 2.32-1.b0a60c3
- New release 2.32 (git snapshot: b0a60c3302973ca1878d149d61f2f612c8f27fac)

* Sat Nov 21 2015 Vaughan <devel at agrez.net> - 2.29-1.d795066
- New release / git snapshot: d79506694d7ba1c3da865d095238289d6175057d
- Drop commit date tag used in rpm release.
- Fix wiringPi-make.patch

* Tue Sep 08 2015 Clive Messer <clive.messer@squeezecommunity.org> - 2.25-1.20150908git5edd177
- Update to latest git.

* Tue Mar 11 2014 markieta <markietachristopher@gmail.com> - 1-4.20130207git98bcb20.rpfr20
- Initial build for Pidora 2014

* Mon May 13 2013 Chris Tyler <chris@tylers.info> - 1-3.20130207git98bcd20.rpfr18
- Added scriptlets

* Fri Nov 16 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1-1
- Updated packaged version and release tags for rpfr18

* Wed Sep 17 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-4
- Package updated to include new files gerthboard.h, piNes.h and wiringSerial.h

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-3
- changed the rpm name of from raspberrypi-wiringpi to wiringpi

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-2
- fixed the missing file lcd.h with the correct path for the examples make

* Wed Jul 11 2012 Andrew Greene <agreene@learn.senecac.on.ca> - 1.0-1
- basic install instructions copied some files to /usr/bin and /usr/lib
- added a quick hack to fix the examples make error lcd.h file not in the right location
