%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib /usr/lib/python2.7/site-packages}

Name:          nuage-ironic-nova
BuildArch:     noarch
Epoch:         1
Version:       4.2.4
Release:       %{build_number}
License:       Apache V2.0.
Group:         default
Summary:       Nuage Openstack nova patch for ironic support
Source0:       nuage-ironic-nova-%{version}.tar.gz
BuildRoot:     %{_tmppath}/nuage-ironic-nova--%{version}-buildroot
Prefix:        /


URL:           http://www.nuagenetworks.net/
Vendor:        Nuage Networks <info@nuagenetworks.com>

Provides:      nuage-ironic-nova
Requires:      openstack-nova-common
Requires:      /bin/sh

%description
Nuage Openstack nova patch for ironic support

%files
%{python2_sitelib}/nuage_ironic_nova*


%prep
%setup -q

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot} --prefix=/usr

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
