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
Version:	1.6.1
Release:	3
# libs are LGPLv2+ applications GPLv2+
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	330120e045183413bca371b295c6a1df
Patch0:		no-xdg-menu-prefix.patch
Patch1:		use-libwnck.patch
URL:		http://wiki.mate-desktop.org/mate-panel
BuildRequires:	dbus-glib-devel
BuildRequires:	dconf-devel
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+2-devel >= 2:2.19.7
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libmateweather-devel >= 1.5.0
BuildRequires:	librsvg-devel
BuildRequires:	libwnck2-devel >= 2.30.7-2
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.5.0
%{?with_apidocs:BuildRequires:	mate-doc-utils}
BuildRequires:	mate-menus-devel
BuildRequires:	pango-devel >= 1:1.15.4
BuildRequires:	popt-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	libwnck2 >= 2.30.7-2
Requires:	mate-window-manager
Suggests:	mate-settings-daemon
# for fish
Requires:	fortune-mod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop panel applets

%package libs
Summary:	Shared libraries for %{name}
License:	LGPL v2+
Group:		Libraries

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for %{name}

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{name}
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
%{name} API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
# libexecdir needed for gnome conflicts
%configure \
	--disable-silent-rules \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-compile \
	--with-x \
	--enable-network-manager \
	--libexecdir=%{_libdir}/%{name} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-panel.convert

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

desktop-file-install \
        --remove-category="MATE" \
        --add-category="X-Mate" \
        --dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

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
%{_mandir}/man1/mate-desktop-item-edit.1*
%{_mandir}/man1/mate-panel-test-applets.1*
%{_mandir}/man1/mate-panel.1*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/clock-applet
%attr(755,root,root) %{_libdir}/%{name}/fish-applet
%attr(755,root,root) %{_libdir}/%{name}/notification-area-applet
%attr(755,root,root) %{_libdir}/%{name}/wnck-applet
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/dbus-1/services/org.mate.panel.*.service
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*.*
%{_desktopdir}/%{name}.desktop

%files libs
%defattr(644,root,root,755)
%doc COPYING.LIB
%attr(755,root,root) %{_libdir}/lib%{name}-applet-4.so.*.*.*
%ghost %{_libdir}/lib%{name}-applet-4.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib%{name}-applet-4.so
%{_includedir}/%{name}-4.0
%{_pkgconfigdir}/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}-applet
%endif
