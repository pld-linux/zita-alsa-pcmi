Summary:	C++ library for easy access to ALSA PCM devices
Name:		zita-alsa-pcmi
Version:	0.2.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	0ba4d59abce231056e2628d081124114
Patch0:		ldconfig.patch
URL:		http://kokkinizita.linuxaudio.org/linuxaudio/
BuildRequires:	alsa-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zita-alsa-pcmi is the successor of clalsadrv. It provides easy access
to ALSA PCM devices, taking care of the many functions required to
open, initialise and use a hw: device in mmap mode, and providing
floating point audio data.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apps
Summary:	Sample applications files for %{name} library
Summary(pl.UTF-8):	Przykładowe aplikacje biblioteki %{name}
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description apps
Sample applications files for %{name} library.

%description devel -l pl.UTF-8
Przykładowe aplikacje biblioteki %{name}.

%prep
%setup -q
%patch0 -p1

%build
cd libs
%{__make} \
	CXXFLAGS="%{rpmcxxflags}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"
ln -sf libzita-alsa-pcmi.so.* libzita-alsa-pcmi.so
cd ..

cd apps
%{__make} \
	CXXFLAGS="%{rpmcxxflags}" \
	CPPFLAGS="%{rpmcppflags} -I../libs" \
	LDFLAGS="%{rpmldflags} -L../libs"
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libs install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib}

%{__make} -C apps install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h

%files apps
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/alsa_delay
%attr(755,root,root) %{_bindir}/alsa_loopback
