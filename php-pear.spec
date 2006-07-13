
%define peardir %{_datadir}/pear

%define xmlrpcver 1.4.8

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.4.9
Release: 3
Epoch: 1
License: The PHP License 3.0
Group: System
URL: http://pear.php.net/package/PEAR
Source0: install-pear-nozlib-%{version}.phar
Source2: relocate.php
Source3: strip.php
Source4: LICENSE
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear
Source20: http://pear.php.net/get/XML_RPC-%{xmlrpcver}.tgz
Patch0: php-pear-1.4.8-template.patch
Patch1: php-pear-1.4.8-package.patch
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php >= 5.1.0-1
Provides: php-pear(Archive_Tar) = 1.3.1 
Provides: php-pear(Console_Getopt) = 1.2
Provides: php-pear(PEAR) = %{version}
Provides: php-pear(XML_RPC) = %{xmlrpcver}
Requires: php >= 5.1.0-1, php-cli

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cTn pear-%{version}

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=`pwd`
export PHP_PEAR_SIG_KEYDIR=/etc/pearkeys
export PHP_PEAR_CACHE_DIR=%{_localstatedir}/cache/php-pear

%{_bindir}/php -n -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
      %{SOURCE0} -d $RPM_BUILD_ROOT%{peardir} \
                 -b $RPM_BUILD_ROOT%{_bindir} \
                 %{SOURCE20}

pushd %{buildroot}%{peardir}
%{__patch} -p0 < %{PATCH0}
%{__patch} -p0 < %{PATCH1}
popd

# Replace /usr/bin/* with simple scripts:
for f in pecl pear peardev; do 
   install -m 755 $RPM_SOURCE_DIR/${f}.sh $RPM_BUILD_ROOT%{_bindir}/${f}
done

install -d $RPM_BUILD_ROOT%{_sysconfdir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{peardir}/.pkgxml

# Relocate everything:
sed -si "s,$RPM_BUILD_ROOT,,g" \
         $RPM_BUILD_ROOT%{peardir}/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*/*.php

# Sanitize the pear.conf
%{_bindir}/php -n %{SOURCE2} pear.conf $RPM_BUILD_ROOT > new-pear.conf
%{_bindir}/php -n %{SOURCE3} new-pear.conf ext_dir > $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

for f in $RPM_BUILD_ROOT%{peardir}/.registry/*.reg; do
   %{_bindir}/php -n %{SOURCE2} ${f} $RPM_BUILD_ROOT > ${f}.new
   mv ${f}.new ${f}
done

install -m 644 -c $RPM_SOURCE_DIR/LICENSE .

install -m 644 -c $RPM_SOURCE_DIR/macros.pear \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.pear        

%check
# Check that no buildroot-relative or arch-specific paths are left in the pear.conf
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep /tmp $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1

%clean
rm -rf $RPM_BUILD_ROOT
rm pear.conf

%files
%defattr(-,root,root,-)
%{peardir}
%{_bindir}/*
%config %{_sysconfdir}/pear.conf
%dir %{_localstatedir}/cache/php-pear
%doc LICENSE

%changelog
* Thu Jul 13 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-3
- require php-cli
- add /etc/rpm/macros.pear (Christopher Stone)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.9-2.1
- rebuild

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-2
- update to 1.4.9 (thanks to Remi Collet, #183359)
- package /usr/share/pear/.pkgxml (#190252)
- update to XML_RPC-1.4.8
- bundle the v3.0 LICENSE file

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-2
- set cache_dir directory, own /var/cache/php-pear

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-1
- update to 1.4.6
- require php >= 5.1.0 (#178821)

* Fri Dec 30 2005 Tim Jackson <tim@timj.co.uk> 1:1.4.5-6
- Patches to fix "pear makerpm"

* Wed Dec 14 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-5
- set default sig_keydir to /etc/pearkeys
- remove ext_dir setting from /etc/pear.conf (#175673)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-4
- fix virtual provide for PEAR package (#175074)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-3
- fix /usr/bin/{pecl,peardev} (#174882)

* Thu Dec  1 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-2
- add virtual provides (#173806) 

* Wed Nov 23 2005 Joe Orton <jorton@redhat.com> 1.4.5-1
- initial build (Epoch: 1 to allow upgrade from php-pear-5.x)
