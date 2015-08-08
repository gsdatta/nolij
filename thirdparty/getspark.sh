#!/bin/bash -ex

cd "${BASH_SOURCE%/*}" || exit
mkdir -p spark
pushd spark

# TODO - Make the port go away
# TODO - Make it datacenter agnostic
BASE_VERSION="1.4.0-URX-01"
FILE_NAME="spark-${BASE_VERSION}-bin-2.5.0-cdh5.3.1"

wget -nc http://artifacts.us-east-1.urx.internal:10000/artifact/spark/releases/v${BASE_VERSION}/${FILE_NAME}.tgz || true

if [[ ! -d $FILE_NAME ]]; then
    tar -xf $FILE_NAME.tgz

    case $(uname -s) in
	Darwin) ln -fsv ./$FILE_NAME ./spark ;;
	*) ln -fsv -T ./$FILE_NAME spark ;;
    esac
fi
popd 
