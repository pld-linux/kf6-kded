#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.2
%define		qtver		5.15.2
%define		kfname		kded

Summary:	Central daemon of KDE work spaces
Summary(pl.UTF-8):	Centralny demon przestrzeni roboczych KDE
Name:		kf6-%{kfname}
Version:	6.2.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	87cba7e4ba0993050df899600fef9473
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kcrash-devel >= %{version}
BuildRequires:	kf6-kdbusaddons-devel >= %{version}
BuildRequires:	kf6-kdoctools-devel >= %{version}
BuildRequires:	kf6-kservice-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kcrash >= %{version}
Requires:	kf6-kdbusaddons >= %{version}
Requires:	kf6-kservice >= %{version}
Requires:	systemd-units >= 1:250.1
Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDED stands for KDE Daemon which isn't very descriptive. KDED runs in
the background and performs a number of small tasks. Some of these
tasks are built in, others are started on demand.

%description -l pl.UTF-8
KDED to skrót od KDE Daemon, co nie mówi zbyt wiele. KDED działa w tle
i wykonuje wiele małych zadań. Niektóre są wbudowane, inne uruchamiane
w razie potrzeby.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_user_post plasma-kded.service

%preun
%systemd_user_preun plasma-kded.service

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kded6
%{_datadir}/dbus-1/interfaces/org.kde.kded6.xml
%{_datadir}/dbus-1/services/org.kde.kded6.service
%{_datadir}/qlogging-categories6/kded.categories
%{_desktopdir}/org.kde.kded6.desktop
%{_datadir}/qlogging-categories6/kded.renamecategories
%{systemduserunitdir}/plasma-kded6.service
%{_mandir}/ca/man8/kded6.8*
%{_mandir}/es/man8/kded6.8*
%{_mandir}/fr/man8/kded6.8*
%{_mandir}/it/man8/kded6.8*
%{_mandir}/man8/kded6.8*
%{_mandir}/nl/man8/kded6.8*
%{_mandir}/tr/man8/kded6.8*
%{_mandir}/uk/man8/kded6.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/KF6KDED
