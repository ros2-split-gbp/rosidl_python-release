%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-rosidl-generator-py
Version:        0.18.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rosidl_generator_py package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Requires:       ros-rolling-ament-cmake-devel
Requires:       ros-rolling-ament-index-python-devel
Requires:       ros-rolling-python-cmake-module-devel
Requires:       ros-rolling-rmw-devel
Requires:       ros-rolling-rosidl-generator-c-devel
Requires:       ros-rolling-rosidl-pycommon-devel
Requires:       ros-rolling-rosidl-typesupport-c-devel
Requires:       ros-rolling-rosidl-typesupport-interface-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       ros-rolling-rosidl-generator-packages(member)

%description
Generate the ROS interfaces in Python.

%package runtime
Summary:        Runtime-only files for rosidl_generator_py package
Requires:       python%{python3_pkgversion}-numpy
Requires:       ros-rolling-ament-index-python-runtime
Requires:       ros-rolling-rosidl-cli-runtime
Requires:       ros-rolling-rosidl-generator-c-runtime
Requires:       ros-rolling-rosidl-parser-runtime
Requires:       ros-rolling-rosidl-runtime-c-runtime
Requires:       ros-rolling-rpyutils-runtime
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  ros-rolling-ament-cmake-devel
BuildRequires:  ros-rolling-rosidl-runtime-c-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  ros-rolling-ament-cmake-pytest-devel
BuildRequires:  ros-rolling-ament-index-python-devel
BuildRequires:  ros-rolling-ament-lint-auto-devel
BuildRequires:  ros-rolling-ament-lint-common-devel
BuildRequires:  ros-rolling-python-cmake-module-devel
BuildRequires:  ros-rolling-rmw-devel
BuildRequires:  ros-rolling-rosidl-cmake-devel
BuildRequires:  ros-rolling-rosidl-generator-c-devel
BuildRequires:  ros-rolling-rosidl-generator-cpp-devel
BuildRequires:  ros-rolling-rosidl-parser-devel
BuildRequires:  ros-rolling-rosidl-typesupport-c-devel
BuildRequires:  ros-rolling-rosidl-typesupport-fastrtps-c-devel
BuildRequires:  ros-rolling-rosidl-typesupport-introspection-c-devel
BuildRequires:  ros-rolling-rpyutils-devel
BuildRequires:  ros-rolling-test-interface-files-devel
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-rolling-rosidl-generator-packages(all)
%endif

%description runtime
Runtime-only files for rosidl_generator_py package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/rosidl_generator_py/cmake/ \
    /opt/ros/rolling/share/rosidl_generator_py/package.dsv \
    /opt/ros/rolling/share/rosidl_generator_py/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/rosidl_generator_py/cmake
%exclude /opt/ros/rolling/share/rosidl_generator_py/package.dsv
%exclude /opt/ros/rolling/share/rosidl_generator_py/package.xml

%changelog
* Tue Apr 11 2023 Dharini Dutia <dharini@openrobotics.org> - 0.18.0-1
- Autogenerated by Bloom

* Tue Mar 21 2023 Dharini Dutia <dharini@openrobotics.org> - 0.17.0-2
- Autogenerated by Bloom

