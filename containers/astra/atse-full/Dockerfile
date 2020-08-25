FROM centos:7
 
MAINTAINER Sandia ATSE Team <atse-help@sandia.gov>

# Avoid "TERM environment variable not set" warnings
ARG TERM=dumb

# All run commands will use /tmp as their current working dir
WORKDIR /tmp

# Install minimum set of dependencies, keep in alphabetical order
RUN sed -i 's/override_install_langs.*/override_install_langs=en_US.utf8/' /etc/yum.conf
RUN yum install -y epel-release
RUN yum update -y
RUN yum install -y \
	cscope \
	deltarpm \
	environment-modules \
	ethtool \
	gcc-gfortran \
	glibc-devel \
	glibc-static \
	info \
	libarchive-devel \
	libmnl \
	libnl3 \
	libstdc++-static \
	lzo-devel \
	logrotate \
	lsof \
	nano \
	numactl-libs \
	pciutils \
	perl \
	psmisc \
	python \
	strace \
	sudo \
	tcl \
	tcsh \
	tk \
	wget \
	libyaml-devel \
	tcp_wrappers-libs \
	vim \
	which \
	zlib-static \
	zlib-devel \
	deltarpm \
	perf \
	python-perf \
	jsoncpp

# Uncomment this if need a container with the ability to build kernel modules.
# Install packages needed to build Linux kernel drivers and rpms
#RUN yum install -y \
#	createrepo \
#	python-devel \
#	make \
#	redhat-rpm-config \
#	rpm-build \
#	kernel \
#	kernel-tools \
#	kernel-tools-libs \
#	kernel-devel

# Install Mellanox OFED, user-level only
ADD http://atse.sandia.gov/mirror/mellanox/MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64.tgz .
RUN tar -zxvf MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64.tgz
RUN MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64/mlnxofedinstall --user-space-only --without-fw-update --all -q --skip-distro-check
# Use this instead of above RUN command if need a container with the ability to build kernel modules.
#RUN RPM_BUILD_NCPUS=8 MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64/mlnxofedinstall --add-kernel-support --without-fw-update --all -q --skip-distro-check --kernel 4.18.0-80.7.2.el7.aarch64
RUN yum install -y MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64/RPMS/COMMON/knem-1.1.3.90mlnx1-OFED.4.7.2.0.7.1.gec1f2f8.rhel7u6alternate.aarch64.rpm
RUN rm -rf MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64
RUN rm -rf MLNX_OFED_LINUX.1.logs
RUN rm MLNX_OFED_LINUX-4.7-3.2.9.0-rhel7.6alternate-aarch64.tgz
RUN rm ofed.conf

# Install Arm Compiler for HPC and Arm Math Libraries
ADD http://atse.sandia.gov/mirror/arm/Arm-Compiler-for-Linux_20.0_RHEL_7_aarch64.tar .
RUN tar -xvf Arm-Compiler-for-Linux_20.0_RHEL_7_aarch64.tar
RUN Arm-Compiler-for-linux_20.0_AArch64_RHEL_7_aarch64/arm-compiler-for-linux-20.0_Generic-AArch64_RHEL-7_aarch64-linux-rpm.sh -a
RUN rm -rf Arm-Compiler-for-linux_20.0_AArch64_RHEL_7_aarch64
RUN rm -rf Arm-Compiler-for-Linux_20.0_RHEL_7_aarch64.tar

# Install Arm Forge
ADD http://atse.sandia.gov/mirror/arm/arm-forge-20.0.2-Redhat-7.6-aarch64.tar .
RUN tar -xvf arm-forge-20.0.2-Redhat-7.6-aarch64.tar
RUN arm-forge-20.0.2-Redhat-7.6-aarch64/textinstall.sh --accept-licence /opt/arm/forge/20.0.2
RUN rm -rf arm-forge-20.0.2-Redhat-7.6-aarch64
RUN rm -rf arm-forge-20.0.2-Redhat-7.6-aarch64.tar

# Install ARM Reports
ADD http://atse.sandia.gov/mirror/arm/arm-reports-20.0.2-Redhat-7.6-aarch64.tar .
RUN tar -xvf arm-reports-20.0.2-Redhat-7.6-aarch64.tar
RUN arm-reports-20.0.2-Redhat-7.6-aarch64/textinstall.sh --accept-license /opt/arm/reports/20.0.2
RUN rm -rf arm-reports-20.0.2-Redhat-7.6-aarch64
RUN rm -rf arm-reports-20.0.2-Redhat-7.6-aarch64.tar

# Install HPE MPI
ADD http://atse.sandia.gov/mirror/hpe/HPE-MPI-1.4-RPMS.tar .
RUN tar -xvf HPE-MPI-1.4-RPMS.tar
COPY config-mgmt/etc/yum.repos.d/hpempi.repo /etc/yum.repos.d/
RUN yum install -y \
	hpe-build-key \
	hpe-mpi-release \
	MPInside \
	cpuset-utils \
	hpe-mpi-docs \
	libFFIO \
	numatools \
	sgi-arraysvcs \
	sgi-mpt \
	sgi-mpt-hmpt \
	sgi-mpt-shmem \
	sgi-mpt-shmem-hmpt \
	sgi-procset \
	xpmem
RUN rm -rf /etc/yum.repos.d/hpempi.repo
RUN rm -rf /etc/yum.repos.d/mpi.repo
RUN rm -rf HPE-MPI-1.4-RPMS

# Install ATSE
COPY config-mgmt/etc/yum.repos.d/atse.repo /etc/yum.repos.d/
RUN rpm -e --nodeps environment-modules
RUN yum install -y \
	atse-filesystem \
	atse-buildroot \
	lmod-atse \
	autoconf-atse \
	automake-atse \
	libtool-atse \
	cmake-atse \
	ninja-atse \
	git-atse \
	binutils-atse \
	gnu7-compilers-atse \
	arm-compilers-devel-atse \
	arm-licenses-snl-atse \
	arm-tools-modulefiles-atse \
	pmix-atse \
	spack-atse \
	singularity-atse \
	charliecloud-atse \
	gdb-atse \
	valgrind-atse \
	tx2mon-atse \
	tx2pmu-atse \
	munge-atse \
	munge-libs-atse \
	munge-devel-atse \
	slurm-atse \
	slurm-slurmctld-atse \
	slurm-slurmd-atse \
	slurm-libpmi-atse \
	slurm-devel-atse \
	slurm-example-configs-atse \
	slurm-pam_slurm-atse \
	slurm-slurmdbd-atse \
	slurm-sview-atse \
	slurm-perlapi-atse \
	slurm-contribs-atse \
	\
	devpacks-atse \
	\
	numactl-gnu7-atse \
	hwloc-gnu7-atse \
	papi-gnu7-atse \
	pdtoolkit-gnu7-atse \
	zlib-gnu7-tx2-atse \
	bzip2-gnu7-tx2-atse \
	xz-gnu7-tx2-atse \
	openucx-gnu7-tx2-atse \
	armpl-gnu7-tx2-atse \
	openblas-gnu7-tx2-atse \
	metis-gnu7-tx2-atse \
	scotch-gnu7-tx2-atse \
	hdf5-gnu7-tx2-atse \
	superlu-gnu7-tx2-atse \
	qthreads-gnu7-tx2-atse \
	openmpi3-gnu7-tx2-atse \
	openmpi4-gnu7-tx2-atse \
	hpempi-gnu7-tx2-atse \
	yaml-cpp-gnu7-tx2-atse \
	powerapi-gnu7-tx2-atse \
	\
	boost-gnu7-openmpi3-tx2-atse \
	phdf5-gnu7-openmpi3-tx2-atse \
	netcdf-gnu7-openmpi3-tx2-atse \
	pnetcdf-gnu7-openmpi3-tx2-atse \
	fftw-gnu7-openmpi3-tx2-atse \
	ptscotch-gnu7-openmpi3-tx2-atse \
	superlu_dist-gnu7-openmpi3-tx2-atse \
	imb-gnu7-openmpi3-tx2-atse \
	hello-gnu7-openmpi3-tx2-atse \
	cgns-gnu7-openmpi3-tx2-atse \
	mpiP-gnu7-openmpi3-tx2-atse \
	netcdf-cxx-gnu7-openmpi3-tx2-atse \
	netcdf-fortran-gnu7-openmpi3-tx2-atse \
	omb-gnu7-openmpi3-tx2-atse \
	parmetis-gnu7-openmpi3-tx2-atse \
	tau-gnu7-openmpi3-tx2-atse \
	\
	boost-gnu7-hpempi-tx2-atse \
	phdf5-gnu7-hpempi-tx2-atse \
	netcdf-gnu7-hpempi-tx2-atse \
	pnetcdf-gnu7-hpempi-tx2-atse \
	fftw-gnu7-hpempi-tx2-atse \
	ptscotch-gnu7-hpempi-tx2-atse \
	superlu_dist-gnu7-hpempi-tx2-atse \
	imb-gnu7-hpempi-tx2-atse \
	hello-gnu7-hpempi-tx2-atse \
	cgns-gnu7-hpempi-tx2-atse \
	mpiP-gnu7-hpempi-tx2-atse \
	netcdf-cxx-gnu7-hpempi-tx2-atse \
	netcdf-fortran-gnu7-hpempi-tx2-atse \
	omb-gnu7-hpempi-tx2-atse \
	parmetis-gnu7-hpempi-tx2-atse \
	\
	numactl-arm-atse \
	hwloc-arm-atse \
	papi-arm-atse \
	pdtoolkit-arm-atse \
	zlib-arm-tx2-atse \
	bzip2-arm-tx2-atse \
	xz-arm-tx2-atse \
	openucx-arm-tx2-atse \
	armpl-arm-tx2-atse \
	openblas-arm-tx2-atse \
	metis-arm-tx2-atse \
	scotch-arm-tx2-atse \
	hdf5-arm-tx2-atse \
	superlu-arm-tx2-atse \
	qthreads-arm-tx2-atse \
	openmpi3-arm-tx2-atse \
	openmpi4-arm-tx2-atse \
	hpempi-arm-tx2-atse \
	yaml-cpp-arm-tx2-atse \
	powerapi-arm-tx2-atse \
	\
	boost-arm-openmpi3-tx2-atse \
	phdf5-arm-openmpi3-tx2-atse \
	netcdf-arm-openmpi3-tx2-atse \
	pnetcdf-arm-openmpi3-tx2-atse \
	fftw-arm-openmpi3-tx2-atse \
	ptscotch-arm-openmpi3-tx2-atse \
	superlu_dist-arm-openmpi3-tx2-atse \
	imb-arm-openmpi3-tx2-atse \
	hello-arm-openmpi3-tx2-atse \
	cgns-arm-openmpi3-tx2-atse \
	mpiP-arm-openmpi3-tx2-atse \
	netcdf-cxx-arm-openmpi3-tx2-atse \
	netcdf-fortran-arm-openmpi3-tx2-atse \
	omb-arm-openmpi3-tx2-atse \
	parmetis-arm-openmpi3-tx2-atse \
	tau-arm-openmpi3-tx2-atse \
	\
	boost-arm-hpempi-tx2-atse \
	phdf5-arm-hpempi-tx2-atse \
	netcdf-arm-hpempi-tx2-atse \
	pnetcdf-arm-hpempi-tx2-atse \
	fftw-arm-hpempi-tx2-atse \
	ptscotch-arm-hpempi-tx2-atse \
	superlu_dist-arm-hpempi-tx2-atse \
	imb-arm-hpempi-tx2-atse \
	hello-arm-hpempi-tx2-atse \
	cgns-arm-hpempi-tx2-atse \
	mpiP-arm-hpempi-tx2-atse \
	netcdf-cxx-arm-hpempi-tx2-atse \
	netcdf-fortran-arm-hpempi-tx2-atse \
	omb-arm-hpempi-tx2-atse \
	parmetis-arm-hpempi-tx2-atse \
	\
	boost-gnu7-openmpi4-tx2-atse \
	phdf5-gnu7-openmpi4-tx2-atse \
	netcdf-gnu7-openmpi4-tx2-atse \
	pnetcdf-gnu7-openmpi4-tx2-atse \
	fftw-gnu7-openmpi4-tx2-atse \
	ptscotch-gnu7-openmpi4-tx2-atse \
	superlu_dist-gnu7-openmpi4-tx2-atse \
	imb-gnu7-openmpi4-tx2-atse \
	hello-gnu7-openmpi4-tx2-atse \
	cgns-gnu7-openmpi4-tx2-atse \
	mpiP-gnu7-openmpi4-tx2-atse \
	netcdf-cxx-gnu7-openmpi4-tx2-atse \
	netcdf-fortran-gnu7-openmpi4-tx2-atse \
	omb-gnu7-openmpi4-tx2-atse \
	parmetis-gnu7-openmpi4-tx2-atse \
	tau-gnu7-openmpi4-tx2-atse \
	\
	boost-arm-openmpi4-tx2-atse \
	phdf5-arm-openmpi4-tx2-atse \
	netcdf-arm-openmpi4-tx2-atse \
	pnetcdf-arm-openmpi4-tx2-atse \
	fftw-arm-openmpi4-tx2-atse \
	ptscotch-arm-openmpi4-tx2-atse \
	superlu_dist-arm-openmpi4-tx2-atse \
	imb-arm-openmpi4-tx2-atse \
	hello-arm-openmpi4-tx2-atse \
	cgns-arm-openmpi4-tx2-atse \
	mpiP-arm-openmpi4-tx2-atse \
	netcdf-cxx-arm-openmpi4-tx2-atse \
	netcdf-fortran-arm-openmpi4-tx2-atse \
	omb-arm-openmpi4-tx2-atse \
	parmetis-arm-openmpi4-tx2-atse \
	tau-arm-openmpi4-tx2-atse \
	\
	darshan-runtime-hpempi-tx2-atse \
	darshan-util-atse \
	darshan-runtime-openmpi4-tx2-atse \
	darshan-runtime-openmpi3-tx2-atse

# Make a symlink to /lustre to store the system-wide Darshan logs.
# This needs to go to a shared high performance parallel file system.
RUN ln -s /lustre/darshan-logs /opt/atse/darshan-logs

# Fixup BOOST for backwards compatibility... this enables apps linked against the old image that used BOOST 1.68.0 to work with the new image's BOOST 1.72.0
RUN /bin/bash -c "cd /opt/atse/libs/arm/openmpi4/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/arm/openmpi4/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/openmpi4/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/openmpi4/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"

RUN /bin/bash -c "cd /opt/atse/libs/arm/openmpi3/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/arm/openmpi3/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/openmpi3/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/openmpi3/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"

RUN /bin/bash -c "cd /opt/atse/libs/arm/hpempi/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/arm/hpempi/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/hpempi/boost/1.72.0/lib; ln -s libboost_program_options.so.1.72.0 libboost_program_options.so.1.68.0"
RUN /bin/bash -c "cd /opt/atse/libs/gnu7/hpempi/boost/1.72.0/lib; ln -s libboost_system.so.1.72.0 libboost_system.so.1.68.0"

# Install ATSE one-off packages
COPY atse_one_offs/cmake-atse-3.9.2-7.1.atse.1.2.4.aarch64.rpm /tmp
COPY atse_one_offs/cmake-atse-3.14.5-4.1.atse.1.2.4.aarch64.rpm /tmp
RUN  rpm --install --force /tmp/cmake-atse-3.9.2-7.1.atse.1.2.4.aarch64.rpm
RUN  rpm --install --force /tmp/cmake-atse-3.14.5-4.1.atse.1.2.4.aarch64.rpm

# Apply config management
COPY config-mgmt /tmp/config-mgmt
RUN rsync -av /tmp/config-mgmt/ /

# Cleanup
RUN yum clean all
RUN rm -rf /var/cache/yum
RUN mkdir -p --mode=0755 /var/cache/yum
RUN rm -rf /tmp/*
RUN rm -rf /etc/yum.repos.d/hpempi.repo

# Setup default user environment
#RUN useradd -ms /bin/bash -c "Generic ATSE User Account" -G wheel atse
#RUN echo "atse ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
#USER atse
#WORKDIR /home/atse
ENTRYPOINT ["/bin/bash"]
