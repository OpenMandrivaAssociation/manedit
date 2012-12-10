%define name		manedit
%define version		1.2.1
%define release		%mkrel 4
%define title		ManEdit
%define longtitle	UNIX manual pages editor

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        UNIX manual pages editor
License:        GPLv2
Group:          Editors
Url:            http://www.battlefieldlinux.com/wolfpack/ManEdit/
Source0:        http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.6.1.lib64.patch
BuildRequires:  imagemagick
BuildRequires:  gtk+1.2-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
ManEdit was created due to a lack of editors for UNIX manual pages,
since users expect each UNIX program/configuration/api/etc to have a
manual page the lack of an editor and the high demand for what it
should create eventually lead to this (long overdue) application. 

Although most resourced developers can create a source document using a
much more advanced editor and then export to multiple file formats, the
average UNIX contributor isn't up to that. Even the creators of this
application were intimidated at the UNIX manual page creation process. 

So to make computers and life simpler, we created ManEdit, the Manual
Page Editor and Viewer. It features: 
- XML Interface and Multiple Sectional Editing 
- Instant preview feature and stand-alone viewer/browser 
- Drag and Drop system and templates for easy mass production 

%prep
%setup -q
%patch0 -p0

%build
export CFLAGS=$RPM_OPT_FLAGS
%ifarch x86_64
./configure Linux64 -v --libdir=-L%{_libdir}
%else
./configure Linux -v --disable=arch-i686 --libdir=-L%{_libdir}
%endif
make

%install
rm -rf %{buildroot}
make PREFIX=%{buildroot}%_prefix MAN_DIR=%{buildroot}%{_mandir}/man1 install

# icons
convert %{name}/%{name}.xpm -resize 16x16 %{name}-16.png
convert %{name}/%{name}.xpm -resize 32x32 %{name}-32.png
convert %{name}/%{name}.xpm %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png 

# menu entry
install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=TextEditor;
EOF

rm %{buildroot}%_iconsdir/*.xpm

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files 
%defattr(-,root,root)
%doc AUTHORS INSTALL LICENSE README
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png




%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-4mdv2011.0
+ Revision: 612810
- the mass rebuild of 2010.1 packages

* Mon Feb 08 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.2.1-3mdv2010.1
+ Revision: 502444
- Fix tag licence
- Clean spec file
- fix all rpmlint warning
- fix patching (%%patch -p 0 to %%patch0 -p0)

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.2.1-2mdv2010.0
+ Revision: 439736
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Oct 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 293695
- new version

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 1.1.1-2mdv2009.0
+ Revision: 268136
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Apr 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-1mdv2009.0
+ Revision: 194352
- update to new version 1.1.1

* Wed Feb 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.3-1mdv2008.1
+ Revision: 162997
- new version

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 0.8.1-1mdv2008.1
+ Revision: 140944
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sun Jul 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.1-1mdv2008.0
+ Revision: 46505
- update to new version 0.8.1


* Wed Nov 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.7.1-1mdv2007.0
+ Revision: 88626
- new version
  drop gcc patch, merged upstream
  dropped old debian menu
- Import manedit

* Wed Aug 02 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.6.1-4mdv2007.0
- xdg menu
- clean buildroot before install
- fix build

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.6.1-3mdk
- Rebuild

* Wed Mar 30 2005 Guillaume Rousse <guillomovitch@mandrake.org> 0.6.1-2mdk
- fix amd64 build (fix bug #15077)

* Sat Mar 19 2005 Austin Acton <austin@mandrake.org> 0.6.1-1mdk
- 0.6.1

* Tue Nov 16 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.5.12-2mdk 
- fix menu entry

* Tue Nov 16 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 0.5.12-1mdk
- New release 0.5.12

* Fri Jul 23 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.5.11-3mdk 
- explicit requires

* Wed Jun 16 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.5.11-2mdk 
- rebuild

* Mon Apr 19 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.5.11-1mdk
- new version
- fixed menu

