
%define peardir %{_datadir}/pear

%define xmlrpcver 1.4.4

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.4.5
Release: 6
Epoch: 1
License: PHP
Group: System
URL: http://pear.php.net/package/PEAR
Source0: install-pear-nozlib-%{version}.phar
Source2: relocate.php
Source3: strip.php
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source20: XML_RPC-%{xmlrpcver}.tgz
Patch0: php-pear-1.4.5-template-fixes.patch
Patch1: php-pear-1.4.5-template-postun.patch
Patch2: php-pear-1.4.5-makerpm-cleanup.patch
Patch3: php-pear-1.4.5-makerpm-rh-namingconvs.patch
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php >= 5.1.0-1
Provides: php-pear(Archive_Tar) = 1.3.1 
Provides: php-pear(Console_Getopt) = 1.2
Provides: php-pear(PEAR) = %{version}
Provides: php-pear(XML_RPC) = %{xmlrpcver}

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cTn pear-%{version}

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=`pwd`
export PHP_PEAR_SIG_KEYDIR=/etc/pearkeys

%{_bindir}/php -n -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
      %{SOURCE0} -d $RPM_BUILD_ROOT%{peardir} \
                 -b $RPM_BUILD_ROOT%{_bindir} \
                 %{SOURCE20}

pushd %{buildroot}%{peardir}
%{__patch} -p0 data/PEAR/template.spec %{PATCH0}
%{__patch} -p1 data/PEAR/template.spec %{PATCH1}
%{__patch} -p0 < %{PATCH2}
%{__patch} -p0 < %{PATCH3}
popd

# Replace /usr/bin/* with simple scripts:
for f in pecl pear peardev; do 
   install -m 755 $RPM_SOURCE_DIR/${f}.sh $RPM_BUILD_ROOT%{_bindir}/${f}
done

install -d $RPM_BUILD_ROOT%{_sysconfdir}

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

%check
# Check that no buildroot-relative or arch-specific paths are left in the pear.conf
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1

%clean
rm -rf $RPM_BUILD_ROOT
rm pear.conf

%files
%defattr(-,root,root,-)
%{peardir}
%{_bindir}/*
%config %{_sysconfdir}/pear.conf

%changelog
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
