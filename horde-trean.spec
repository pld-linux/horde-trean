%define	_hordeapp trean
%define	_snap	2005-09-03
#define	_rc		rc1
%define	_rel	2.1
#
%include	/usr/lib/rpm/macros.php
Summary:	Horde Bookmarks application
Summary(pl):	Aplikacja zak³adek dla Horde
Name:		%{_hordeapp}
Version:	0.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	BSD
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	f2d09422cd0059f5e74bf4485cb84db4
Source1:	%{_hordeapp}.conf
URL:		http://www.horde.org/trean/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
# docs say it requires 3.1, but seems work in 3.0 too
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc	CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}

%description
The Trean (Bookmarks) application allows you to store, organize and
manage, and most importantly access your web browser bookmarks on-line
and in one central place accessible from any web browser.

By storing your bookmarks here, you can access them from any browser
on any machine that can access the Horde applications. This means you
can easily access your bookmarks from multiple browsers, multiple
machines, remote locations, etc. And if you upgrade, switch, or test
out browsers, you don't have to worry about what happens to your
bookmarks or how to import them into the new browser.

%description -l pl
Aplikacja Tream (zak³adki) pozwala na przechowywanie, organizowanie i
zarz±dzanie, a co najwa¿niejsze, dostêp do zak³adek przegl±darki WWW
on-line w jednym centralnym miejscu dostêpnym z ka¿dej przegl±darki.

Poprzez przechowywanie w niej zak³adek mo¿na mieæ do nich dostêp z
dowolnej przegl±darki na dowolnym komputerze maj±cej dostêp do
aplikacji Horde. Oznacza to, ¿e mo¿na ³atwo dostaæ siê do zak³adek z
wielu przegl±darek, wielu komputerów, ró¿nych miejsc itp. I po
uaktualnieniu, zmianie lub przy testowaniu przegl±darek nie trzeba siê
martwiæ co siê stanie z zak³adkami, albo jak zaimportowaæ je do nowej
przegl±darki.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

rm -f config/.htaccess

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR locale/*			$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR themes/*			$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
You need DataTree configured in Horde for Bookmarks to work. You can
find horde_datatree.mysql.sql from Horde documentation.
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
