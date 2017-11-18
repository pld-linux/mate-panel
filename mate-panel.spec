#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	MATE Desktop panel applets
Summary(pl.UTF-8):	Aplety panelu dla środowiska MATE Desktop
Name:		mate-panel
Version:	1.18.6
Release:	1
License:	LGPL v2+ (library), GPL v2+ (applets)
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.18/%{name}-%{version}.tar.xz
# Source0-md5:	f71cd80e5bf00ac48e0258a906b5a541
Patch0:		no-xdg-menu-prefix.patch
URL:		http://wiki.mate-desktop.org/mate-panel
BuildRequires:	NetworkManager-devel >= 0.6
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.7.1
BuildRequires:	gettext-tools >= 0.12
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+3-devel >= 3.14
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libmateweather-devel >= 1.17.0
BuildRequires:	librsvg-devel >= 2.36.2
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libwnck-devel >= 3.0.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.17.0
BuildRequires:	mate-menus-devel >= 1.10.0
BuildRequires:	pango-devel >= 1:1.15.4
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.1.2
Requires:	dbus-glib >= 0.80
Requires:	dconf >= 0.13.4
Requires:	desktop-file-utils
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	libmateweather >= 1.17.0
Requires:	librsvg >= 2.36.2
Requires:	libwnck >= 3.0.0
Requires:	marco
Requires:	mate-desktop >= 1.17.0
Requires:	mate-menus >= 1.10.0
Suggests:	mate-settings-daemon
# for fish
Requires:	fortune-mod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop panel applets.

%description -l pl.UTF-8
Aplety panelu dla środowiska MATE Desktop.

%package libs
Summary:	Shared library for MATE panel applets
Summary(pl.UTF-8):	Biblitoteka współdzielona dla apletów panelu MATE
License:	LGPL v2+
Group:		Libraries
Requires:	cairo >= 1.0.0
Requires:	gdk-pixbuf2 >= 2.7.1
Requires:	glib2 >= 1:2.36
Requires:	gtk+3 >= 3.14
Requires:	pango >= 1:1.15.4
Requires:	xorg-lib-libXrandr >= 1.3.0

%description libs
Shared library for MATE panel applets.

%description libs -l pl.UTF-8
Biblitoteka współdzielona dla apletów panelu MATE.

%package devel
Summary:	Development files for libmate-panel-applet library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libmate-panel-applet
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36
Requires:	gtk+3-devel >= 3.14

%description devel
Development files for libmate-panel-applet library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libmate-panel-applet.

%package apidocs
Summary:	API documentation for libmate-panel-applet library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmate-panel-applet
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libmate-panel-applet library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmate-panel-applet.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# libexecdir needed for gnome conflicts
%configure \
	--libexecdir=%{_libdir}/%{name} \
	--enable-network-manager \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir} \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

desktop-file-install \
        --remove-category="MATE" \
        --add-category="X-Mate" \
        --dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,jv,ku_IQ,pms}

%find_lang %{name} --with-mate --all-name

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
%doc AUTHORS ChangeLog NEWS README
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
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/dbus-1/services/org.mate.panel.*.service
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/mate-panel*.*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-panel-applet-4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-panel-applet-4.so.1
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_pkgconfigdir}/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-panel-applet
%endif
