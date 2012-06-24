%define		mod_name	cvs
Summary:	Apache module: Automatically updates files in a CVS-based webtree
Summary(pl):	Modu� do apache: Automatyczne uaktualnianie plik�w z drzewa CVS
Name:		apache-mod_%{mod_name}
Version:	0.4
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.sub.nu/pub/mod_cvs/mod_%{mod_name}-%{version}.tar.gz
URL:		http://www.sub.nu/mod_cvs/
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache-devel
BuildRequires:	zlib-devel
Prereq:		/usr/sbin/apxs
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
Apache module: Automatically updates files in a CVS-based webtree.

%description -l pl
Modu� do apache: Automatyczne uaktualnianie plik�w z drzewa CVS.

%prep 
%setup -q -n mod_%{mod_name}-%{version}

%build
/usr/sbin/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
