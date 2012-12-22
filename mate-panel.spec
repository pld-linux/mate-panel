# TODO
# - docs broken, like mate-desktop
#   fix gtk-doc building (probably missing some dtd's)
#xsltproc -o mate-applet-clock-C.omf --stringparam db2omf.basename mate-applet-clock --stringparam db2omf.format 'docbook' --stringparam db2omf.dtd "-//OASIS//DTD DocBook XML V4.1.2//EN" --stringparam db2omf.lang C --stringparam db2omf.omf_dir "/usr/share/omf" --stringparam db2omf.help_dir "/usr/share/mate/help" --stringparam db2omf.omf_in "/home/users/glen/rpm/packages/BUILD.i686-linux/mate-panel-1.5.3/help/clock/mate-applet-clock.omf.in"  `/usr/bin/pkg-config --variable db2omf mate-doc-utils` C/mate-applet-clock.xml || { rm -f "mate-applet-clock-C.omf"; exit 1; }
#if ! test -d ar/; then mkdir ar/; fi
#if [ -f "C/mate-applet-clock.xml" ]; then d="../"; else d="/home/users/glen/rpm/packages/BUILD.i686-linux/mate-panel-1.5.3/help/clock/"; fi; \
#mo="ar/ar.mo"; \
#if [ -f "${mo}" ]; then mo="../${mo}"; else mo="/home/users/glen/rpm/packages/BUILD.i686-linux/mate-panel-1.5.3/help/clock/${mo}"; fi; \
#(cd ar/ && \
#  `which xml2po` -m docbook -e -t "${mo}" \
#    "${d}C/mate-applet-clock.xml" > mate-applet-clock.xml.tmp && \
#    cp mate-applet-clock.xml.tmp mate-applet-clock.xml && rm -f mate-applet-clock.xml.tmp)
#runtime error
#xsltApplyStylesheet: saving to mate-applet-clock-C.omf may not be possible
#make[3]: *** [mate-applet-clock-C.omf] Error 1
#make[3]: *** Waiting for unfinished jobs....
#Making all in mate-panel-applet
#make[4]: Entering directory `/home/users/glen/rpm/BUILD/i686-linux/mate-panel-1.5.3/doc/reference/mate-panel-applet'
#  DOC   Scanning header files
#  DOC   Introspecting gobjects
#libtool: link: cannot find the library `../../../libmate-panel-applet/libmate-panel-applet-3.la' or unhandled argument `../../../libmate-panel-applet/libmate-panel-applet-3.la'
#Linking of scanner failed:
#make[4]: *** [scan-build.stamp] Error 1
#make[4]: Leaving directory `/home/users/
# - check direct deps:
#mate-panel-1.5.3-0.1.i686 marks mate-menus-libs-1.5.0-1.i686 (cap libmate-menu.so.2)
#mate-panel-1.5.3-0.1.i686 marks mate-panel-libs-1.5.3-0.1.i686 (cap libmate-panel-applet-4.so.1)
#mate-panel-1.5.3-0.1.i686 marks libmateweather-1.5.0-1.i686 (cap libmateweather.so.1)
#mate-panel-1.5.3-0.1.i686 marks libmatewnck-1.5.0-1.i686 (cap libmatewnck.so.0)
# - panel does not start:
#(mate-panel:7862): GLib-GIO-ERROR **: Settings schema 'org.mate.caja.desktop' is not installed

# Conditional build:
%bcond_with	apidocs		# disable gtk-doc

Summary:	MATE Desktop panel applets
Name:		mate-panel
Version:	1.5.3
Release:	0.2
# libs are LGPLv2+ applications GPLv2+
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	72029cbcd38bee447df92c8774452bf3
URL:		http://mate-desktop.org/
BuildRequires:	desktop-file-utils
BuildRequires:	icon-naming-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(libmatewnck)
BuildRequires:	pkgconfig(libnm-gtk)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
%{?with_apidoc:BuildRequires:	pkgconfig(mate-doc-utils)}
BuildRequires:	pkgconfig(mateweather)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	popt-devel
BuildRequires:	tar >= 1:1.22
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
Requires:	%{name} = %{version}-%{release}

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
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}} \

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

%find_lang %{name}

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
%{_mandir}/man1/*
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib
%{_libexecdir}/mate-panel
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_desktopdir}/mate-panel.desktop
%{_datadir}/dbus-1/services/org.mate.panel.*.service
%{_datadir}/omf/mate-applet-fish
%{_datadir}/omf/mate-applet-clock
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/mate/help/mate-applet-clock
%{_datadir}/mate/help/mate-applet-fish
%{_datadir}/mate-panel
%{_datadir}/mate-panelrc

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
