#
# Conditional build:
%bcond_without	apidocs		# gtk-doc API documentation

Summary:	MATE Desktop panel applets
Summary(pl.UTF-8):	Aplety panelu dla środowiska MATE Desktop
Name:		mate-panel
Version:	1.28.4
Release:	1
License:	LGPL v2+ (library), GPL v2+ (applets)
Group:		X11/Applications
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	20d4bf601a5ab66f912d63a5ba59853d
URL:		https://wiki.mate-desktop.org/mate-desktop/components/mate-panel/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.26.0
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtk-layer-shell-devel
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libmateweather-devel >= 1.17.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libwnck-devel >= 3.32.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.28.2
BuildRequires:	mate-menus-devel >= 1.21.0
BuildRequires:	pango-devel >= 1:1.15.4
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.1.2
Requires:	dconf >= 0.13.4
Requires:	desktop-file-utils
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	libmateweather >= 1.17.0
Requires:	libwnck >= 3.32.0
Requires:	marco
Requires:	mate-desktop >= 1.28.2
Requires:	mate-menus >= 1.21.0
Suggests:	mate-settings-daemon
# for fish
Requires:	fortune-mod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# use package subdir to avoid conflicts with GNOME
%define		pkglibexecdir	%{_libexecdir}/%{name}

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
Requires:	gdk-pixbuf2 >= 2.26.0
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22
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
Requires:	glib2-devel >= 1:2.50.0
Requires:	gtk+3-devel >= 3.22

%description devel
Development files for libmate-panel-applet library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libmate-panel-applet.

%package apidocs
Summary:	API documentation for libmate-panel-applet library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmate-panel-applet
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for libmate-panel-applet library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmate-panel-applet.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libexecdir=%{pkglibexecdir} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/mate-panel/ui

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# es_ES,ku_IQ are outdated versions of es,ku
# the rest not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,pms}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/help/{es_ES,frp,ie,jv,ku_IQ,pms,ur_PK,zh-Hans}

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
%dir %{pkglibexecdir}
%attr(755,root,root) %{pkglibexecdir}/clock-applet
%attr(755,root,root) %{pkglibexecdir}/fish-applet
%attr(755,root,root) %{pkglibexecdir}/notification-area-applet
%attr(755,root,root) %{pkglibexecdir}/wnck-applet
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
