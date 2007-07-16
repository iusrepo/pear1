
%define peardir %{_datadir}/pear

%define xmlrpcver 1.5.1

# Upstream only make the latest .phar available via the following URL,
# no archive of each version of the installer archives exists:
#   http://pear.php.net/install-pear-nozlib.phar

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.5.4
Release: 4
Epoch: 1
License: The PHP License v3.0
Group: Development/Languages
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
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-cli >= 5.1.0-1, gnupg
Provides: php-pear(Archive_Tar) = 1.3.2
Provides: php-pear(Console_Getopt) = 1.2.1
Provides: php-pear(PEAR) = %{version}
Provides: php-pear(Structures_Graph) = 1.0.2
Provides: php-pear(XML_RPC) = %{xmlrpcver}
Requires: php >= 5.1.0-1, php-cli

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cTn pear-%{version}

%build
# This is an empty build section.

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=`pwd`
export PHP_PEAR_SIG_KEYDIR=/etc/pearkeys
export PHP_PEAR_SIG_BIN=/usr/bin/gpg

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

%{_bindir}/php -n -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
      %{SOURCE0} -d $RPM_BUILD_ROOT%{peardir} \
                 -b $RPM_BUILD_ROOT%{_bindir} \
                 %{SOURCE20}

# Replace /usr/bin/* with simple scripts:
for f in pecl pear peardev; do 
   install -m 755 $RPM_SOURCE_DIR/${f}.sh $RPM_BUILD_ROOT%{_bindir}/${f}
done

install -d $RPM_BUILD_ROOT%{_sysconfdir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{peardir}/.pkgxml \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm

# Relocate everything:
sed -si "s,$RPM_BUILD_ROOT,,g" \
         $RPM_BUILD_ROOT%{peardir}/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*/*.php

# Sanitize the pear.conf
%{_bindir}/php -n %{SOURCE2} pear.conf $RPM_BUILD_ROOT | 
  %{_bindir}/php -n %{SOURCE2} php://stdin $PWD > new-pear.conf
%{_bindir}/php -n %{SOURCE3} new-pear.conf ext_dir > $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

for f in $RPM_BUILD_ROOT%{peardir}/.registry/*.reg; do
   %{_bindir}/php -n %{SOURCE2} ${f} $RPM_BUILD_ROOT > ${f}.new
   mv ${f}.new ${f}
done

install -m 644 -c $RPM_SOURCE_DIR/LICENSE .

install -m 644 -c $RPM_SOURCE_DIR/macros.pear \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.pear        

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1

%clean
rm -rf $RPM_BUILD_ROOT
rm pear.conf

%files
%defattr(-,root,root,-)
%{peardir}
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/pear.conf
%config %{_sysconfdir}/rpm/macros.pear
%dir %{_localstatedir}/cache/php-pear
%doc LICENSE

%changelog
* Mon Jul 16 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.5.4-4
- update macros.pear (without define)

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-3
- add pecl_{un,}install macros to macros.pear (from Remi)

* Fri May 11 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-2
- update to 1.5.4

* Tue Mar  6 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-3
- add redundant build section (#226295)
- BR php-cli not php (#226295)

* Mon Feb 19 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-2
- update builtin module provides (Remi Collet, #226295)
- drop patch 0

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-1
- update to 1.5.0

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-4
- fix Group, mark pear.conf noreplace (#226295)

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-3
- use BuildArch not BuildArchitectures (#226925)
- fix to use preferred BuildRoot (#226925)
- strip more buildroot-relative paths from *.reg
- force correct gpg path in default pear.conf

* Thu Jan  4 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-2
- update to 1.4.11

* Fri Jul 14 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-4
- update to XML_RPC-1.5.0
- really package macros.pear

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
