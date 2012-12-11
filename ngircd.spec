Summary:	Next Generation IRC Daemon
Name:		ngircd
Version:	19.1
Release:	%mkrel 1
Group:		System/Servers
License:	GPLv2+
URL:		http://ngircd.barton.de/
Source0:	ftp://ftp.berlios.de/pub/ngircd/ngircd-%{version}.tar.gz
Source1:	ngircd.init
Patch0:		ngircd-13-mdv_conf.diff
BuildRequires:	ident-devel
BuildRequires:	openssl-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	zlib-devel
BuildRequires:	pam-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ngIRCd is a free open source daemon for Internet Relay Chat (IRC), developed
under the GNU General Public License (GPL). It's written from scratch and is
not based upon the original IRCd like many others.

%prep

%setup -q
%patch0 -p0

cp %{SOURCE1} ngircd.init

%build
%serverbuild

# to prevent nasty ipv6 surprises
export CFLAGS="$CFLAGS -D_GNU_SOURCE"

%configure2_5x \
    --enable-ipv6 \
    --with-syslog \
    --with-zlib \
    --with-epoll \
    --with-openssl \
    --with-tcp-wrappers \
    --with-ident \
    --with-pam

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/ngircd

%makeinstall_std

install -m0755 ngircd.init %{buildroot}%{_initrddir}/ngircd
install -m0660 doc/sample-ngircd.conf %{buildroot}%{_sysconfdir}/ngircd.conf

touch  %{buildroot}%{_sysconfdir}/ngircd.motd
rm -rf %{buildroot}%{_docdir}/ngircd

# pam file
install -d %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/ngircd <<EOF
#%PAM-1.0
auth       required     pam_permit.so
auth       include      system-auth
account    include      system-auth
EOF

%pre
%_pre_useradd ngircd /tmp /sbin/nologin

%post
%_post_service ngircd

%preun
%_preun_service ngircd

%postun
%_postun_userdel ngircd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README doc/*
%attr(0660,root,ngircd) %config(noreplace) %{_sysconfdir}/ngircd.conf
%attr(0660,root,ngircd) %ghost %config(noreplace) %{_sysconfdir}/ngircd.motd
%config(noreplace) %{_sysconfdir}/pam.d/ngircd
%{_initrddir}/ngircd
%{_sbindir}/ngircd
%dir %attr(0775,root,ngircd) /var/run/ngircd
%{_mandir}/man5/ngircd.conf*
%{_mandir}/man8/ngircd.8*


%changelog
* Sun Apr 29 2012 Oden Eriksson <oeriksson@mandriva.com> 19.1-1mdv2012.0
+ Revision: 794426
- 19.1

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 18-1
+ Revision: 696499
- 18

* Thu Dec 23 2010 Oden Eriksson <oeriksson@mandriva.com> 17.1-1mdv2011.0
+ Revision: 624175
- 17.1

* Mon Nov 08 2010 Oden Eriksson <oeriksson@mandriva.com> 17-1mdv2011.0
+ Revision: 595030
- 17

* Fri Sep 24 2010 Oden Eriksson <oeriksson@mandriva.com> 16-1mdv2011.0
+ Revision: 580908
- 16

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 15-2mdv2010.1
+ Revision: 535274
- rebuild

* Fri Nov 13 2009 Oden Eriksson <oeriksson@mandriva.com> 15-1mdv2010.1
+ Revision: 465755
- 15

* Mon Jun 01 2009 Oden Eriksson <oeriksson@mandriva.com> 14.1-1mdv2010.0
+ Revision: 382004
- rediff one patch
- 14.1

* Fri Jan 30 2009 Oden Eriksson <oeriksson@mandriva.com> 13-2mdv2009.1
+ Revision: 335418
- disable avahi/zeroconf support per default (conditional switch)

* Fri Jan 23 2009 Oden Eriksson <oeriksson@mandriva.com> 13-1mdv2009.1
+ Revision: 332815
- import ngircd


* Fri Jan 23 2009 Oden Eriksson <oeriksson@mandriva.com> 13-1mdv2009.1
- initial Mandriva package (fedora import)

* Thu Oct 23 2008 Andreas Thienemann <andreas@bawue.net> 0.12.1-1
- Updated to 0.12.1
- Updated configuration sample

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11.0-2
- fix license tag

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> 0.11.0-1
- Updated to 0.11.0

* Tue Nov 20 2007 Andreas Thienemann <andreas@bawue.net> 0.10.3-1
- Rebased to 0.10.3
- Incorporated patches from fw@strlen.de

* Thu Apr 26 2007 Andreas Thienemann <andreas@bawue.net> 0.10.1-3
- Removed libident requirement
- Added patch from fw fixing server connections

* Mon Apr 02 2007 Andreas Thienemann <andreas@bawue.net> 0.10.1-2
- Added ngirc user

* Sat Mar 31 2007 Andreas Thienemann <andreas@bawue.net> 0.10.1-1
- Initial package
