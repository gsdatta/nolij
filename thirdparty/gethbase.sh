#!/bin/bash -ex

cd "${BASH_SOURCE%/*}" || exit
mkdir -p hbase
pushd hbase

VERSION='1.0.1.1'
TAR_NAME=hbase-${VERSION}

wget -nc http://mirrors.advancedhosters.com/apache/hbase/${VERSION}/${TAR_NAME}-bin.tar.gz || true

if [[ ! -d ${TAR_NAME} ]]; then
    tar -xf ${TAR_NAME}-bin.tar.gz

    case $(uname -s) in
	Darwin) ln -fsv ./${TAR_NAME} ./hbase ;;
	*) ln -fsv -T ./${TAR_NAME} hbase ;;
    esac
fi
popd 
