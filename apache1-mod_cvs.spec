%define		mod_name	cvs
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Automatically updates files in a CVS-based webtree
Summary(pl):	Modu³ do apache: Automatyczne uaktualnianie plików z drzewa CVS
Name:		apache-mod_%{mod_name}
Version:	0.5
Release:	4
License:	GPL
Group:		Networking/Daemons
# working URL: http://www.sub.nu/mod_cvs/src/
# (but only separate files here, no tarball)
Source0:	ftp://ftp.sub.nu/pub/mod_cvs/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e2cfe7818337915e6cbaffa45852012f
URL:		http://www.sub.nu/mod_cvs/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	zlib-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
Apache module: Automatically updates files in a CVS-based webtree.

%description -l pl
Modu³ do apache: Automatyczne uaktualnianie plików z drzewa CVS.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
