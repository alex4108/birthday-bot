#!/usr/bin/env bash
set -e

getSitePackagesDir() { 
    version=$(python3 --version)
    pyVersionMajor=$(echo ${version} | cut -f1 -d.)
    pyVersionMinor=$(echo ${version} | cut -f2 -d.)
    version=$(echo ${pyVersionMajor}.${pyVersionMinor} | sed 's/ //g')
    version=$(echo ${version} | tr '[:upper:]' '[:lower:]')
    SITE_PACKAGES_DIR=${version}
    SHORT_VERSION_NUMBER=$(echo ${pyVersionMajor} | sed 's/[^0-9]*//g')${pyVersionMinor}
}

# Builds lambda deployment package for birthday-bot function
if ! command -v pip3
then
    echo "pip3 doesn't exist, refusing to build birthday-bot"
    exit
fi

if ! command -v python3
then
    echo "python3 doesn't exist, refusing to build birthday-bot"
    exit
fi

if ! command -v virtualenv
then
    echo "virtualenv doesn't exist, installing it..."
    pip3 install virtualenv
fi

set +e
ORIGINAL_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
rm -rf build/ birthday-bot.zip
mkdir -p build/
cd build/
cp ${ORIGINAL_DIR}/birthday-bot.py .
cp ${ORIGINAL_DIR}/requirements.txt .
cp -r ${ORIGINAL_DIR}/common .
virtualenv venv
source venv/bin/activate
$VIRTUAL_ENV/bin/pip3 install -r requirements.txt
getSitePackagesDir
zip -r9 ${ORIGINAL_DIR}/birthday-bot.zip birthday-bot.py
zip -r9 ${ORIGINAL_DIR}/birthday-bot.zip quotes.json
zip -r9 ${ORIGINAL_DIR}/birthday-bot.zip common/
cd ./venv/lib/${SITE_PACKAGES_DIR}/site-packages/
zip -r9 ${ORIGINAL_DIR}/birthday-bot.zip .
deactivate