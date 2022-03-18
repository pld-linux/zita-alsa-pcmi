Summary:	C++ library for easy access to ALSA PCM devices
Summary(pl.UTF-8):	Biblioteka C++ do łatwego dostępu do urządzeń ALSA PCM
Name:		zita-alsa-pcmi
Version:	0.4.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	aae5416f40d8d149e6d6a41610ecaace
Patch0:		makefile.patch
URL:		http://kokkinizita.linuxaudio.org/linuxaudio/
BuildRequires:	alsa-lib-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zita-alsa-pcmi is the successor of clalsadrv. It provides easy access
to ALSA PCM devices, taking care of the many functions required to
open, initialise and use a hw: device in mmap mode, and providing
floating point audio data.

%description -l pl.UTF-8
Zita-alsa-pcmi to następca clalsadrv. Zapewnia łatwy dostęp do
urządzeń ALSA PCM, biorąc na siebie wiele funkcji wymaganych do
otwarcia, zainicjowania i użycia urządzeń hw: w trybie mmap, oraz
obsługując zmiennoprzecinkowe dane dźwiękowe.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib-devel
Requires:	libstdc++-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apps
Summary:	Sample applications files for %{name} library
Summary(pl.UTF-8):	Przykładowe aplikacje do biblioteki %{name}
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description apps
Sample applications files for %{name} library.

%description devel -l pl.UTF-8
Przykładowe aplikacje do biblioteki %{name}.

%prep
%setup -q
%patch0 -p1

%build
cd source
CXX="%{__cxx}" \
CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make}
ln -sf libzita-alsa-pcmi.so.* libzita-alsa-pcmi.so
cd ..

CXX="%{__cxx}" \
CXXFLAGS="%{rpmcxxflags}" \
CPPFLAGS="%{rpmcppflags} -I../source" \
LDFLAGS="%{rpmldflags} -L../source" \
%{__make} -C apps

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C source install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

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
%attr(755,root,root) %{_libdir}/libzita-alsa-pcmi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzita-alsa-pcmi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzita-alsa-pcmi.so
%{_includedir}/zita-alsa-pcmi.h

%files apps
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/alsa_delay
%attr(755,root,root) %{_bindir}/alsa_loopback
