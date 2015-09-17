#!/bin/bash

PWD=`pwd`
RPM_SPEC="gradle.spec"
BUILD_ROOT="${PWD}/rpmbuild-root"

# create build space
BUILD_ROOT="${PWD}/rpmbuild-root"
for DIR in BUILD BUILDROOT RPMS SOURCE SOURCES SPECS SRPMS tmp ; do
	if [ -d "${BUILD_ROOT}/${DIR}" ]; then
		rm -rf --preserve-root "${BUILD_ROOT}/${DIR}" || \
			exit 1
	fi
	mkdir -p "${BUILD_ROOT}/${DIR}" || \
		exit 1
done
cp -fv "${PWD}/${RPM_SPEC}" "${BUILD_ROOT}/SPECS/" \
	|| exit 1

rpmbuild -bb \
	--define="_topdir ${BUILD_ROOT}" \
	--define="_tmppath ${BUILD_ROOT}/tmp" \
	--define="_rpmdir ${PWD}/target" \
	"${BUILD_ROOT}/SPECS/${RPM_SPEC}" \
		|| exit 1
