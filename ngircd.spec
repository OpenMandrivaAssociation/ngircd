Summary:	Next Generation IRC Daemon

Name:		ngircd
Version:	21.1
Release:	2
Group:		System/Servers
License:	GPLv2+
URL:		http://ngircd.barton.de/
Source0:	ftp://ftp.berlios.de/pub/ngircd/ngircd-%{version}.tar.gz
Source1:	ftp://ftp.berlios.de/pub/ngircd/ngircd-%{version}.tar.gz.sig
Source2:	ngircd.service
Source3:	ngircd.pam
Patch0:		ngircd-21.1-default_config.diff
BuildRequires:	openssl-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	zlib-devel
BuildRequires:	pam-devel
Requires(post):  systemd
Requires(post):  rpm-helper
Requires(preun): rpm-helper

%description
ngIRCd is a free open source daemon for Internet Relay Chat (IRC), developed
under the GNU General Public License (GPL). It's written from scratch and is
not based upon the original IRCd like many others.

%prep

%setup -q
%patch0 -p1

cp %{SOURCE2} ngircd.service
cp %{SOURCE3} ngircd.pam

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
    --with-pam

%make

%install

install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/pam.d

%makeinstall_std

install -m0755 ngircd.service %{buildroot}%{_unitdir}/
install -m0660 doc/sample-ngircd.conf %{buildroot}%{_sysconfdir}/ngircd.conf
install -m644 ngircd.pam %{buildroot}%{_sysconfdir}/pam.d/ngircd

echo "%{name}-%{version}-%{release}"  %{buildroot}%{_sysconfdir}/ngircd.motd
rm -rf %{buildroot}%{_docdir}/ngircd

mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/%{name}.conf
d /run/ngircd 0775 root ngircd
EOF

touch %{buildroot}%{_sysconfdir}/ngircd.motd

%pre
%_pre_useradd ngircd /tmp /sbin/nologin

%post
%systemd_post ngircd.service

%preun
%systemd_preun ngircd.service

%postun
%systemd_postun_with_restart ngircd.service
%_postun_userdel ngircd

%files
%doc AUTHORS COPYING ChangeLog NEWS README doc/*
%attr(0660,root,ngircd) %config(noreplace) %{_sysconfdir}/ngircd.conf
%attr(0660,root,ngircd) %ghost %config(noreplace) %{_sysconfdir}/ngircd.motd
%config(noreplace) %{_sysconfdir}/pam.d/ngircd
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/ngircd.service
%{_sbindir}/ngircd
%{_mandir}/man5/ngircd.conf*
%{_mandir}/man8/ngircd.8*


