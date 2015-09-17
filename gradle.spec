Name            : gradle
Summary         : Auto install gradle
Version         : 2.7.0
Release         : 2
BuildArch       : noarch
Provides        : gradle
Requires        : java >= 1.8
Requires        : wget
Requires        : unzip
Prefix          : %{_bindir}/%{name}
%define _rpmfilename  %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define gradle_version 2.7
%define gradle_url https://services.gradle.org/distributions/gradle-%{gradle_version}-bin.zip
Group           : Development Tools
License         : Apache License 2.0
Packager        : PoiXson <support@poixson.com>
URL             : http://poixson.com/

%description
Gradle is a build tool with a focus on build automation and support for multi-language development.


# avoid centos 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

# disable debug info
# % define debug_package %{nil}



### Prep ###
%prep



### Build ###
%build



### Install ###
%install
echo
echo "Install.."
# delete existing rpm's
%{__rm} -fv "%{_rpmdir}/%{name}"*.noarch.rpm
# create directories
%{__install} -d -m 0755 \
	"${RPM_BUILD_ROOT}%{prefix}" \
	"${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d" \
		|| exit 1
printf "#!/bin/bash\n\nexport GRADLE_HOME=\"%{prefix}/latest/\"\nexport PATH=\"\$PATH:\$GRADLE_HOME/bin/\"\n" \
	> "${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/gradle.sh"
%{__chmod} 0755 \
	"${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/gradle.sh" \
		|| exit 1
echo "Downloading.."
wget -O "${RPM_BUILD_ROOT}%{prefix}/gradle-%{gradle_version}-bin.zip" \
	"%{gradle_url}"
%{__chmod} -c 0555 \
	"${RPM_BUILD_ROOT}%{prefix}/gradle-%{gradle_version}-bin.zip" \
		|| exit 1



%check



%clean
if [ -d "${RPM_BUILD_ROOT}" ] && [ ! -z "${RPM_BUILD_ROOT}" ]; then
	%{__rm} -rf --preserve-root "${RPM_BUILD_ROOT}" \
		|| echo "Failed to delete build root (probably fine..)"
fi



%post
echo
echo "Extracting.."
%{__unzip} -oq "${RPM_BUILD_ROOT}%{prefix}/gradle-%{gradle_version}-bin.zip" \
	-d "${RPM_BUILD_ROOT}%{prefix}/" \
		|| exit 1
%{__ln_s} -fnv "${RPM_BUILD_ROOT}%{prefix}/%{name}-%{gradle_version}/" \
	"${RPM_BUILD_ROOT}%{prefix}/latest" \
		|| exit 1
%{__chmod} -R 0755 \
	"${RPM_BUILD_ROOT}%{prefix}/%{name}-%{gradle_version}/" \
		|| exit 1
if [ -f "%{prefix}/gradle-%{gradle_version}-bin.zip" ]; then
	%{__rm} -f "%{prefix}/gradle-%{gradle_version}-bin.zip" \
		|| echo "Failed to delete build root (probably fine..)"
fi
hash -r && sync
source "${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/gradle.sh"
# check installation
gradle -v || exit 1



%postun
if [ ! -z "${RPM_BUILD_ROOT}" ] && [ ! -z "%{prefix}" ]; then
	%{__rm} -rf --preserve-root "${RPM_BUILD_ROOT}%{prefix}/" \
		|| echo "Failed to delete gradle files (probably fine..)"
fi



### Files ###
%files
%defattr(-,root,root,-)
%{prefix}/gradle-%{gradle_version}-bin.zip
%{_sysconfdir}/profile.d/gradle.sh
