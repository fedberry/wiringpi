%global _hardened_build 1
%global commit_long     8d188fa0e00bb8c6ff6eddd07bf92857e9bd533a
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})

Name:       wiringpi
Version:    2.46
Release:    3%{?dist}
Summary:    PIN based GPIO access library for BCM283x SoC devices
License:    LGPLv3
URL:        http://wiringpi.com
Source0:    https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_long};sf=tgz#/wiringPi-%{commit_short}.tar.gz
Patch0:     0001-Makefiles.patch
ExclusiveArch: %{arm}
Obsoletes:  %{name}-libs
Conflicts:  %{name}-libs


%description
WiringPi is a PIN based GPIO access library for the BCM2835, BCM2836 and
BCM2837 SoC devices (Raspberry Pi devices). It is usable from C,
C++ and RTB (BASIC) as well as many other languages with suitable
wrappers.


%package tools
Summary:    Utility tools for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description tools
The wiringPi gpio utility is used for command line GPIO access. It be used in
scripts to manipulate the GPIO pins, set outputs and read inputs.


%package devel
Summary:    Development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
WiringPi development libraries to allow GPIO access on a Raspberry Pi from C
and C++ programs.


%prep
%autosetup -p1 -n wiringPi-%{commit_short}


%build
# Build libraries
for i in wiringPi devLib; do
    pushd $i
    make %{?_smp_mflags} DEBUG="%{optflags}" LDFLAGS="%{__global_ldflags}"
    popd
done

# Build GPIO utility
pushd gpio
make %{?_smp_mflags} DEBUG="%{optflags}" \
LDFLAGS="-L../wiringPi -L../devLib %{__global_ldflags}"
popd

# Create pkgconfig files
%{__cat} << EOF > wiringPi.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: wiringPi
Description: wiringPi library
Version: %{version}
Libs: -L%{_libdir} -lwiringPi -lpthread
Cflags: -I%{_includedir}/wiringPi
EOF

%{__cat} << EOF > wiringPiDev.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: wiringPiDev
Description: wiringPi device library
Version: %{version}
Libs: -L%{_libdir} -lwiringPi -lwiringPiDev -lpthread
Cflags: -I%{_includedir}/wiringPi
EOF

# Fix spurious executable perm
chmod -x examples/PiFace/ladder.c


%install
# Install libraries & GPIO utility
for i in wiringPi devLib gpio; do
    pushd $i
    make install-fedora DESTDIR=%{buildroot} PREFIX=%{_prefix} LIBDIR=%{_libdir}
    popd
done

# Install pkgconfig files
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig
%{__install} -p -m 0644 *.pc %{buildroot}%{_libdir}/pkgconfig/


%ldconfig_scriptlets


%files devel
%defattr(-,root,root)
%doc examples
%dir %{_includedir}/wiringPi
%{_libdir}/pkgconfig/*.pc
%{_includedir}/wiringPi/*.h


%files tools
%defattr(-,root,root)
%{_bindir}/gpio
%{_mandir}/man1/*.1.*


%files
%defattr(-,root,root)
%doc People README.TXT pins/pins.pdf
%license COPYING.LESSER
%{_libdir}/libwiringPi.so.*
%{_libdir}/libwiringPiDev.so.*


%changelog
* Mon Jul 30 2018 Vaughan Agrez <devel@agrez.net> - 2.46-3
- Add conflicts/obsoletes for old wiringpi-libs package

* Sat Jul 07 2018 Vaughan Agrez <devel@agrez.net> - 2.46-2
- Major refactor of spec file
- Update Patch0 (Makefiles.patch)
- Bump release for f28 release

* Mon May 07 2018 Vaughan <devel at agrez.net> - 2.46-1.8d188fa
- New release 2.46 (git commit: 8d188fa0e00bb8c6ff6eddd07bf92857e9bd533a)
- Clean up & refactor spec file
- Update Patch0

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
