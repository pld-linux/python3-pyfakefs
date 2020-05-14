#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Fake file system that mocks the Python 2 file system modules
Summary(pl.UTF-8):	Fałszywy system plików będący atrapą modułów systemowych Pythona 2 dla plików
Name:		python-pyfakefs
Version:	3.7.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/jmcgeheeiv/pyfakefs/releases
Source0:	https://github.com/jmcgeheeiv/pyfakefs/archive/v%{version}/pyfakefs-%{version}.tar.gz
# Source0-md5:	e34234db867202b035d48a77d1c78d82
URL:		http://pyfakefs.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.0}
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pathlib2 >= 2.3.2
BuildRequires:	python-pytest >= 2.8.6
BuildRequires:	python-scandir >= 1.8
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 2.8.6
%if "%{py3_ver}" < "3.6"
BuildRequires:	python3-pathlib2 >= 2.3.2
BuildRequires:	python3-scandir >= 1.8
%endif
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyfakefs implements a fake file system that mocks the Python file
system modules. Using pyfakefs, your tests operate on a fake file
system in memory without touching the real disk. The software under
test requires no modification to work with pyfakefs.

%description -l pl.UTF-8
pyfakefs implementuje fałszywy system plików, będący atrapą dla
modułów systemowych Pythona dla plików. Przy użyciu pyfakefs testy
operują na fałszywym systemie plików w pamięci, bez dotykania
prawdziwego dysku. Testowane oprogramowanie nie wymaga modyfikacji,
aby działało z pyfakefs.

%package -n python3-pyfakefs
Summary:	Fake file system that mocks the Python 3 file system modules
Summary(pl.UTF-8):	Fałszywy system plików będący atrapą modułów systemowych Pythona 3 dla plików
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pyfakefs
pyfakefs implements a fake file system that mocks the Python file
system modules. Using pyfakefs, your tests operate on a fake file
system in memory without touching the real disk. The software under
test requires no modification to work with pyfakefs.

%description -n python3-pyfakefs -l pl.UTF-8
pyfakefs implementuje fałszywy system plików, będący atrapą dla
modułów systemowych Pythona dla plików. Przy użyciu pyfakefs testy
operują na fałszywym systemie plików w pamięci, bez dotykania
prawdziwego dysku. Testowane oprogramowanie nie wymaga modyfikacji,
aby działało z pyfakefs.

%package apidocs
Summary:	API documentation for Python pyfakefs module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyfakefs
Group:		Documentation

%description apidocs
API documentation for Pythona pyfakefs module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyfakefs.

%prep
%setup -q -n pyfakefs-%{version}

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pyfakefs.tests.all_tests
# fails on pathlib
#%{__python} -m pyfakefs.tests.all_tests_without_extra_packages

PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pyfakefs.pytest_plugin \
%{__python} -m pytest \
	pyfakefs/pytest_tests/pytest_plugin_test.py
# fails with python2 (any < 3.6?)
#pyfakefs/pytest_tests/pytest_fixture_test.py

PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pyfakefs.pytest_plugin \
%{__python} -m pytest \
	pyfakefs/pytest_tests/pytest_plugin_failing_test.py > testresult.txt || :
%{__python} -m pytest \
	pyfakefs/pytest_tests/pytest_check_failed_plugin_test.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pyfakefs.tests.all_tests
%{__python3} -m pyfakefs.tests.all_tests_without_extra_packages

PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pyfakefs.pytest_plugin \
%{__python3} -m pytest \
	pyfakefs/pytest_tests/pytest_fixture_test.py \
	pyfakefs/pytest_tests/pytest_plugin_test.py

PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pyfakefs.pytest_plugin \
%{__python3} -m pytest \
	pyfakefs/pytest_tests/pytest_plugin_failing_test.py > testresult.txt || :
%{__python3} -m pytest \
	pyfakefs/pytest_tests/pytest_check_failed_plugin_test.py
%endif
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%{py_sitescriptdir}/pyfakefs
%{py_sitescriptdir}/pyfakefs-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pyfakefs
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%{py3_sitescriptdir}/pyfakefs
%{py3_sitescriptdir}/pyfakefs-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc gh-pages/{_static,*.html,*.js}
%endif
