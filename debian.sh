#!/usr/bin/env bash


if [ ! -d "venv" ]; then
	echo "Starting one-time setup"
	required_packages=("git" "python3-venv" "curl" "nodejs" "gcc" "python3-dev")

	is_package_installed() {
		package=$1
		if dpkg -l | grep "^ii.* $package " > /dev/null; then
			return 1
		else
			echo "$package not found, installing automatically"
			return 0
		fi
	}

	for package in "${required_packages[@]}"; do
		if is_package_installed "$package"; then
			sudo apt install $package > /dev/null
		fi
	done


	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

	clear

	echo "Enter link for backend (press enter and leave this empty if you havent setup anything separately)"
	read link

	if [ "$link" == "http"* ]; then
		sed -i "8s/.*/    api_url='$link',/" "rxconfig.py"
	fi


	reflex init

else

	source venv/bin/activate

fi
reflex run --env prod
