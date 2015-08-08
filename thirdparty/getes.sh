#!/bin/bash -ex

cd "${BASH_SOURCE%/*}" || exit
mkdir -p es
pushd es

VERSION="1.6.0"
wget -nc https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-${VERSION}.tar.gz

if [[ ! -d elasticsearch-${VERSION} ]]; then
    tar -xf elasticsearch-${VERSION}.tar.gz

    case $(uname -s) in
	Darwin) ln -fsv ./elasticsearch-${VERSION} ./es ;;
	*) ln -fsv -T elasticsearch-${VERSION} es ;;
    esac
fi
popd 
