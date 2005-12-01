
%define peardir %{_datadir}/pear

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.4.5
Release: 1
Epoch: 1
License: PHP
Group: System
URL: http://pear.php.net/package/PEAR
Source0: install-pear-nozlib-%{version}.phar
Source1: pear.sh
Source2: relocate.php
Source3: XML_RPC-1.4.4.tgz
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php >= 5.1.0-1

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cTn pear-%{version}

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=`pwd`

%{_bindir}/php -n -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
        %{SOURCE0} -d $RPM_BUILD_ROOT%{peardir}\
                   -b $RPM_BUILD_ROOT%{_bindir} \
                   %{SOURCE3}

# Replace /usr/bin/pear with something simple:
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/pear

install -d $RPM_BUILD_ROOT%{_sysconfdir}

# Relocate everything:
sed -si "s,$RPM_BUILD_ROOT,,g" \
         $RPM_BUILD_ROOT%{peardir}/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*.php \
         $RPM_BUILD_ROOT%{peardir}/*/*/*.php

%{_bindir}/php -n %{SOURCE2} pear.conf $RPM_BUILD_ROOT > $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

for f in $RPM_BUILD_ROOT%{peardir}/.registry/*.reg; do
   %{_bindir}/php -n %{SOURCE2} ${f} $RPM_BUILD_ROOT > ${f}.new
   mv ${f}.new ${f}
done

%check
# Check that no buildroot-relative paths are left in the pear.conf
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1

%clean
rm -rf $RPM_BUILD_ROOT
rm pear.conf

%files
%defattr(-,root,root,-)
%{peardir}
%{_bindir}/*
%config %{_sysconfdir}/pear.conf

%changelog
* Wed Nov 23 2005 Joe Orton <jorton@redhat.com> 1.4.5-1
- initial build (Epoch: 1 to allow upgrade from php-pear-5.x)
