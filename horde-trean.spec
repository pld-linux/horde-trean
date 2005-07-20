
%define	_snap	2005-05-11
%define	_rel	1.1

%include	/usr/lib/rpm/macros.php
Summary:	Horde Bookmarks application
Summary(pl):	Aplikacja zak³adek dla Horde
Name:		trean
Version:	0.1
Release:	%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.horde.org/pub/snaps/%{_snap}/%{name}-HEAD-%{_snap}.tar.gz
# NoSource0-md5:	20f5a96682d04444d48f9307ebb08515
# don't put snapshots to df
NoSource:	0
Source1:	%{name}.conf
URL:		http://www.horde.org/trean/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
# docs say it requires 3.1, but seems work in 3.0 too
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc	CREDITS
%define		_noautoreq		'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org

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

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Trean) please visit <http://www.horde.org/>.

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

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
Genral Public License. Wiêcej informacji (w³±cznie z pomoc± dla
Treana) mo¿na znale¼æ na stronie <http://www.horde.org/>.

%prep
%setup -q -n %{name}

rm -f config/.htaccess

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -p config/conf.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR locale/*			$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR themes/*			$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
IMPORTANT:
You need DataTree configured in Horde for Bookmarks to work. You can
find horde_datatree.mysql.sql from Horde documentation.
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
