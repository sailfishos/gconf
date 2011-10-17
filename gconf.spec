#
# Please submit bugfixes or comments via http://bugs.meego.com/
#

%define glib2_version 2.25.9
%define dbus_version 1.0.1
%define dbus_glib_version 0.74

Name:           gconf
Version:        3.1.3
Release:        1
License:        LGPLv2+
Summary:        A process-transparent configuration system
Url:            http://projects.gnome.org/gconf/
Group:          System Environment/Base
#VCS: git:git://git.gnome.org/gconf
Source0:        http://download.gnome.org/sources/GConf/3.1/GConf-%{version}.tar.bz2
Source1:        macros.gconf2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.14
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.8
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
#BuildRequires:  pkgconfig(gobject-introspection-no-export-1.0) >= 0.6.7
#BuildRequires:  pkgconfig(gtk+-3.0) >= 3.0.0
#BuildRequires:  pkgconfig(gtk-doc) >= 0.9
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(polkit-gobject-1) >= 0.92
# for patch0
Requires:       /usr/bin/killall
Requires:       dbus
Obsoletes:      GConf-dbus
Conflicts:      GConf-dbus
Provides:       GConf-dbus
Obsoletes:      GConf2
Conflicts:      GConf2
Provides:       GConf2

Patch0:         GConf-2.18.0.1-reload.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=568845
Patch1:         GConf-gettext.patch

%description
GConf is a process-transparent configuration database API used to
store user preferences. It has pluggable backends and features to
support workgroup administration.

%package devel
Summary:        Headers and libraries for GConf development
Group:          Development/Libraries
Requires:       %{name} = %{version}
# we install an automake macro
Requires:       automake
# we install a pc file
Requires:       pkgconfig
Requires:       pkgconfig(glib-2.0) >= %{glib2_version}
Obsoletes:      GConf-dbus-devel <= 2.29.1
Conflicts:      GConf-dbus-devel <= 2.29.1

%description devel
GConf development package. Contains files needed for doing
development using GConf.

#%package gtk
#Summary:        Graphical GConf utilities
#Group:          System Environment/Base
#Requires:       %{name} = %{version}
#Obsoletes:      GConf-dbus-gtk
#Conflicts:      GConf-dbus-gtk

#%description gtk
#The gconf-gtk package contains graphical GConf utilities
#which require GTK+.

%prep
%setup -q -n GConf-%{version}
%patch0 -p1 -b .reload
%patch1 -p1 -b .gettext

%build
%configure --disable-static --enable-defaults-service --with-gtk=3.0 --disable-orbit
make

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/gconf/schemas
mkdir -p %{buildroot}%{_sysconfdir}/gconf/gconf.xml.system
mkdir -p %{buildroot}%{_sysconfdir}/rpm/
mkdir -p %{buildroot}%{_localstatedir}/lib/rpm-state/gconf
mkdir -p %{buildroot}%{_datadir}/GConf/gsettings

install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/

mkdir -p %{buildroot}%{_datadir}/GConf/gsettings

%find_lang GConf2

%post
/sbin/ldconfig

if [ $1 -gt 1 ]; then
    if ! fgrep -q gconf.xml.system %{_sysconfdir}/gconf/2/path; then
        sed -i -e 's@xml:readwrite:$(HOME)/.gconf@&\n\n# Location for system-wide settings.\nxml:readonly:/etc/gconf/gconf.xml.system@' %{_sysconfdir}/gconf/2/path
    fi
fi

%postun -p /sbin/ldconfig


%docs_package

%files -f GConf2.lang
%defattr(-, root, root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/gconf/2/path
%dir %{_sysconfdir}/gconf
%dir %{_sysconfdir}/gconf/2
%dir %{_sysconfdir}/gconf/gconf.xml.defaults
%dir %{_sysconfdir}/gconf/gconf.xml.mandatory
%dir %{_sysconfdir}/gconf/gconf.xml.system
%dir %{_sysconfdir}/gconf/schemas
%{_bindir}/gconf-merge-tree
%{_bindir}/gconftool-2
%{_bindir}/gsettings-data-convert
%{_sysconfdir}/xdg/autostart/gsettings-data-convert.desktop
%{_libexecdir}/gconfd-2
%{_libdir}/*.so.*
%{_libdir}/GConf/2/*.so
%dir %{_datadir}/sgml
%{_datadir}/sgml/gconf
%{_datadir}/GConf
%dir %{_libdir}/GConf
%dir %{_libdir}/GConf/2
%{_sysconfdir}/rpm/macros.gconf2
%{_sysconfdir}/dbus-1/system.d/org.gnome.GConf.Defaults.conf
%{_libexecdir}/gconf-defaults-mechanism
%{_datadir}/polkit-1/actions/org.gnome.gconf.defaults.policy
%{_datadir}/dbus-1/system-services/org.gnome.GConf.Defaults.service
%{_datadir}/dbus-1/services/org.gnome.GConf.service
# Something else should probably own this, but I'm not sure what.
%dir %{_localstatedir}/lib/rpm-state/
%{_localstatedir}/lib/rpm-state/gconf/
%{_libdir}/gio/modules/libgsettingsgconfbackend.so
#%{_libdir}/girepository-1.0

#%files gtk
#%defattr(-, root, root)
#%{_libexecdir}/gconf-sanity-check-2

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/gconf
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/gconf
%{_libdir}/pkgconfig/*
#%{_datadir}/gir-1.0
%{_bindir}/gsettings-schema-convert

