%define		mod_name	cvs
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: Automatically updates files in a CVS-based webtree
Summary(pl):	Modu³ do apache: Automatyczne uaktualnianie plików z drzewa CVS
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	2
License:	GPL
Group:		Networking/Daemons
# working URL: http://www.sub.nu/mod_cvs/src/
# (but only separate files here, no tarball)
Source0:	ftp://ftp.sub.nu/pub/mod_cvs/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e2cfe7818337915e6cbaffa45852012f
URL:		http://www.sub.nu/mod_cvs/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_cvs <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

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
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 0.5-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
