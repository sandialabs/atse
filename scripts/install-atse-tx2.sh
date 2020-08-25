yum clean all

# Misc. prereques for RedHat
#yum install --installroot=/opt/ohpc/admin/images/login_rhel7.6 \
yum install \
  man \
  glibc-static \
  libstdc++-static \
  iotop \
  iftop \
  psmisc \
  logrotate \
  nc \
  xorg-x11-xauth \
  xterm \
  xeyes \
  emacs \
  tcsh \
  screen \
  tmux \
  wireshark \
  iproute \
  dropwatch \
  systemtap \
  tuna \
  valgrind \
  oprofile \
  numactl \
  hwloc \
  ncurses-devel \
  ncurses-static \
  strace \
  lsof \
  nano \
  pciutils \
  tcl \
  tk \
  libyaml-devel \
  zlib-static \
  zlib-devel \
  which \
  perl \
  libmnl \
  deltarpm \
  ethtool \
  gcc-gfortran \
  libarchive-devel \
  libnl3 \
  lzo-devel \
  qemu-kvm \
  libvirt \
  virt-install \
  libvirt-python \
  virt-manager \
  virt-install \
  libvirt-client \
  yum-utils \
  createrepo \
  python-devel \
  vim \
  vim-X11 \
  cmake \
  kernel-devel \
  binutils-devel \
  systemd-devel \
  numactl-devel \
  automake \
  autoconf \
  libtool \
  gcc \
  gcc-c++ \
  gcc-gfortran

# Install base programming environment
#yum install --installroot=/opt/ohpc/admin/images/login_rhel7.6 \
yum install \
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
  pmix-atse \
  spack-atse \
  singularity-atse \
  charliecloud-atse \
  gdb-atse \
  valgrind-atse \
  tx2mon-atse \
  arm-tools-modulefiles-atse

# Install SLURM
#yum install --installroot=/opt/ohpc/admin/images/login_rhel7.6 \
yum install \
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
  slurm-contribs-atse

# Install GNU7 third-party libs
#yum install --installroot=/opt/ohpc/admin/images/login_rhel7.6 \
yum install \
  zlib-gnu7-atse \
  bzip2-gnu7-atse \
  xz-gnu7-tx2-atse \
  numactl-gnu7-atse \
  hwloc-gnu7-atse \
  papi-gnu7-atse \
  openucx-gnu7-atse \
  openmpi3-gnu7-tx2-atse \
  armpl-gnu7-tx2-atse \
  openblas-gnu7-tx2-atse \
  boost-gnu7-openmpi3-tx2-atse \
  hdf5-gnu7-atse \
  phdf5-gnu7-openmpi3-atse \
  netcdf-gnu7-openmpi3-atse \
  pnetcdf-gnu7-openmpi3-atse \
  fftw-gnu7-openmpi3-atse \
  metis-gnu7-atse \
  scotch-gnu7-atse \
  ptscotch-gnu7-openmpi3-atse \
  superlu-gnu7-atse \
  superlu_dist-gnu7-openmpi3-atse \
  imb-gnu7-openmpi3-tx2-atse \
  qthreads-gnu7-tx2-atse \
  hello-gnu7-openmpi3-tx2-atse

# Install ARM third-party libs
# This should mirror exactly the GNU7 set above, changing gnu7 -> arm
#yum install --installroot=/opt/ohpc/admin/images/login_rhel7.6 \
yum install \
  zlib-arm-atse \
  bzip2-arm-atse \
  xz-arm-tx2-atse \
  numactl-arm-atse \
  hwloc-arm-atse \
  papi-arm-atse \
  openucx-arm-atse \
  openmpi3-arm-tx2-atse \
  armpl-arm-tx2-atse \
  openblas-arm-tx2-atse \
  boost-arm-openmpi3-tx2-atse \
  hdf5-arm-atse \
  phdf5-arm-openmpi3-atse \
  netcdf-arm-openmpi3-atse \
  pnetcdf-arm-openmpi3-atse \
  fftw-arm-openmpi3-atse \
  metis-arm-atse \
  scotch-arm-atse \
  ptscotch-arm-openmpi3-atse \
  superlu-arm-atse \
  superlu_dist-arm-openmpi3-atse \
  imb-arm-openmpi3-tx2-atse \
  qthreads-arm-tx2-atse \
  hello-arm-openmpi3-tx2-atse

