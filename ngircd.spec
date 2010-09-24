%define build_zeroconf 0

%{?_with_zeroconf: %{expand: %%define build_zeroconf 1}}
%{?_without_zeroconf: %global build_zeroconf 0}

Summary:	Next Generation IRC Daemon
Name:		ngircd
Version:	16
Release:	%mkrel 1
Group:		System/Servers
License:	GPLv2+
URL:		http://ngircd.barton.de/
Source0:	ftp://ftp.berlios.de/pub/ngircd/ngircd-%{version}.tar.gz
Source1:	ngircd.init
Patch0:		ngircd-13-mdv_conf.diff
%if %{build_zeroconf}
BuildRequires:	avahi-compat-howl-devel
%endif
BuildRequires:	ident-devel
BuildRequires:	openssl-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	zlib-devel
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
%if %{build_zeroconf}
    --with-zeroconf \
%endif
    --with-ident 

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
%{_initrddir}/ngircd
%{_sbindir}/ngircd
%dir %attr(0775,root,ngircd) /var/run/ngircd
%{_mandir}/man5/ngircd.conf*
%{_mandir}/man8/ngircd.8*
