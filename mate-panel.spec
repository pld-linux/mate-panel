# TODO
# - check direct deps:
#mate-panel-1.5.3-0.1.i686 marks mate-menus-libs-1.5.0-1.i686 (cap libmate-menu.so.2)
#mate-panel-1.5.3-0.1.i686 marks mate-panel-libs-1.5.3-0.1.i686 (cap libmate-panel-applet-4.so.1)
#mate-panel-1.5.3-0.1.i686 marks libmateweather-1.5.0-1.i686 (cap libmateweather.so.1)
#mate-panel-1.5.3-0.1.i686 marks libmatewnck-1.5.0-1.i686 (cap libmatewnck.so.0)

# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	MATE Desktop panel applets
Name:		mate-panel
Version:	1.5.3
Release:	1
# libs are LGPLv2+ applications GPLv2+
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	72029cbcd38bee447df92c8774452bf3
URL:		http://wiki.mate-desktop.org/mate-panel
BuildRequires:	NetworkManager-gtk-lib-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	dconf-devel
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.25.12
BuildRequires:	gobject-introspection-devel
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+2-devel >= 2:2.19.7
BuildRequires:	icon-naming-utils
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-devel
BuildRequires:	libmateweather-devel
BuildRequires:	libmatewnck-devel
BuildRequires:	librsvg-devel
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel
%{?with_apidocs:BuildRequires:	mate-doc-utils}
BuildRequires:	mate-menus-devel
BuildRequires:	pango-devel >= 1:1.15.4
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
# needed as nothing else requires it
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	mate-session-manager
Suggests:	mate-settings-daemon
# for fish
Requires:	fortune-mod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop panel applets

%package libs
Summary:	Shared libraries for mate-panel
License:	LGPL v2+
Group:		Libraries

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:	Development files for mate-panel
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for mate-panel

%package apidocs
Summary:	mate-panel API documentation
Summary(pl.UTF-8):	Dokumentacja API mate-panel
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mate-panel API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API mate-panel.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
# libexecdir needed for gnome conflicts
%configure \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-compile \
	--with-x \
	--enable-network-manager \
	--libexecdir=%{_libexecdir}/mate-panel \
	--with-html-dir=%{_gtkdocdir}

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

desktop-file-install \
        --remove-category="MATE" \
        --add-category="X-Mate" \
        --dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-panel.desktop

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/mate-desktop-item-edit
%attr(755,root,root) %{_bindir}/mate-panel
%attr(755,root,root) %{_bindir}/mate-panel-test-applets
%{_mandir}/man1/mate-panel.1*
%dir %{_libdir}/mate-panel
%attr(755,root,root) %{_libdir}/mate-panel/clock-applet
%attr(755,root,root) %{_libdir}/mate-panel/fish-applet
%attr(755,root,root) %{_libdir}/mate-panel/mate-panel-add
%attr(755,root,root) %{_libdir}/mate-panel/notification-area-applet
%attr(755,root,root) %{_libdir}/mate-panel/wnck-applet
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/dbus-1/services/org.mate.panel.*.service
%{_datadir}/mate-panel
%{_datadir}/mate-panelrc
%{_iconsdir}/hicolor/*/*/*
%{_desktopdir}/mate-panel.desktop

%files libs
%defattr(644,root,root,755)
%doc COPYING.LIB
%attr(755,root,root) %{_libdir}/libmate-panel-applet-4.so.*.*.*
%ghost %{_libdir}/libmate-panel-applet-4.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_pkgconfigdir}/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-panel-applet
%endif
