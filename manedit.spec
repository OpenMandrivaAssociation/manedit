Summary:	UNIX manual pages editor
Name:		manedit
Version:	1.2.1
Release:	6
License:	GPLv2+
Group:		Editors
Url:		https://www.battlefieldlinux.com/wolfpack/ManEdit/
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.6.1.lib64.patch
Patch1:		manedit-1.2.1-no-strip.patch
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(gtk+)
BuildRequires:	pkgconfig(zlib)

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

%files
%doc AUTHORS LICENSE README
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
export CFLAGS="%{optflags}"
%ifarch x86_64
./configure Linux64 -v --libdir=-L%{_libdir}
%else
./configure Linux -v --disable=arch-i686 --libdir=-L%{_libdir}
%endif
make

%install
make PREFIX=%{buildroot}%{_prefix} MAN_DIR=%{buildroot}%{_mandir}/man1 install

# icons
convert %{name}/%{name}.xpm -resize 16x16 %{name}-16.png
convert %{name}/%{name}.xpm -resize 32x32 %{name}-32.png
convert %{name}/%{name}.xpm %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png 

# menu entry
install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=ManEdit
Comment=UNIX manual pages editor
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=TextEditor;
EOF

rm %{buildroot}%{_iconsdir}/*.xpm

