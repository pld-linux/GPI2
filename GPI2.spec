# TODO: CUDA, MPI, Load Leveler(?)
#
# Conditional build:
%bcond_without	f90	# Fortran bindings
%bcond_without	logger	# gaspi_logger utility
#
%ifnarch %{x8664}
# no sources, only x86_64 binary included
%undefine	with_logger
%endif
Summary:	GPI-2 - API for asynchronous communication
Summary(pl.UTF-8):	GPI-2 - API do komunikacji asynchronicznej
Name:		GPI2
Version:	1.2.0
Release:	0.1
License:	GPL v3
Group:		Applications
Source0:	https://www.openfabrics.org/downloads/gpi2/%{name}-%{version}.tar.gz
# Source0-md5:	985ef97215563f5af5e71833a490ef97
Patch0:		%{name}-nosse.patch
Patch1:		%{name}-format.patch
URL:		http://www.gpi-site.com/gpi2/
BuildRequires:	doxygen
%{?with_f90:BuildRequires:	gcc-fortran >= 5:4.0}
BuildRequires:	libibverbs-devel >= 1.1.6
Requires:	libibverbs >= 1.1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GPI-2 is the second generation of GPI (http://www.gpi-site.com/). GPI-2
implements the GASPI specification (http://www.gaspi.de/), an API
specification which originates from the ideas and concepts of GPI.

GPI-2 is an API for asynchronous communication. It provides a
flexible, scalable and fault tolerant interface for parallel
applications.

%description -l pl.UTF-8
GPI-2 to druga generacja GPI (http://www.gpi-site.com/). GPI-2
jest implementacją specyfikacji GASPI (http://www.gaspi.de/) - API
wywodzącego się z idei GPI.

GPI-2 to API do komunikacji asynchronicznej. Zapewnia elastyczny,
skalowalny i odporny na awarie interfejs do aplikacji równoległych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%if %{without logger}
# precompiled binaries
# FIXME: sources are missing
%{__rm} bin/gaspi_logger
%endif

%build
%{__make} clean
%{__make} -C src depend
%{__make} gpi \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -D_GNU_SOURCE"
%if %{with f90}
%{__make} fortran
%endif

%if %{with tests}
%{__make} tests
%endif

%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

install bin/gaspi_run.ssh $RPM_BUILD_ROOT%{_bindir}/gaspi_run
install bin/ssh.spawner bin/gaspi_cleanup $RPM_BUILD_ROOT%{_bindir}
%if %{with logger}
install bin/gaspi_logger $RPM_BUILD_ROOT%{_bindir}
%endif
cp -pr include $RPM_BUILD_ROOT%{_includedir}
cp -p lib64/lib* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/html
%attr(755,root,root) %{_bindir}/gaspi_cleanup
%if %{with logger}
%attr(755,root,root) %{_bindir}/gaspi_logger
%endif
%attr(755,root,root) %{_bindir}/gaspi_run
%attr(755,root,root) %{_bindir}/ssh.spawner
%{_libdir}/libGPI2.a
%{_libdir}/libGPI2-dbg.a
%{_includedir}/GASPI.h
%{_includedir}/GASPI_Ext.h
%{_includedir}/GASPI_GPU.h
%{_includedir}/GASPI_Threads.h
%{_includedir}/PGASPI.h
%{_includedir}/gaspi.mod
%{_includedir}/gaspi_types.mod
