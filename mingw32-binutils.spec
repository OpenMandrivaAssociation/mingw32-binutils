%define Werror_cflags %nil

%define binutils_version 2.19.1
#define mingw32_binutils_version 20080109-2
#define mingw32_binutils_rpmvers %{expand:%(echo %{mingw32_binutils_version} | tr - _)}

Name:           mingw32-binutils
Version:        %{binutils_version}
Release:        %mkrel 3
Summary:        MinGW Windows binutils

License:        GPLv2+ and LGPLv2+ and GPLv3+ and LGPLv3+
Group:          Development/Other
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/binutils-%{binutils_version}-mingw32-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 38

# NB: This must be left in.
Requires:       mingw32-filesystem >= 38


%description
MinGW Windows binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.


%prep
%setup -q -n binutils-%{binutils_version}


%build
mkdir -p build
cd build
CFLAGS="$RPM_OPT_FLAGS" \
../configure \
  --build=%_build --host=%_host \
  --target=%{_mingw32_target} \
  --verbose --disable-nls \
  --without-included-gettext \
  --disable-win32-registry \
  --disable-werror \
  --with-sysroot=%{_mingw32_sysroot} \
  --prefix=%{_prefix} --bindir=%{_bindir} \
  --includedir=%{_includedir} --libdir=%{_libdir} \
  --mandir=%{_mandir} --infodir=%{_infodir}

make all


%install
rm -rf $RPM_BUILD_ROOT

cd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with ordinary binutils.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_bindir}/i586-pc-mingw32-*
%{_prefix}/i586-pc-mingw32/bin
%{_prefix}/i586-pc-mingw32/lib/ldscripts
