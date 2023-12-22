#!/bin/bash

if [ "${PWD##*/}" = "locale" ];
then
	function compile {
		# shellcheck disable=SC2164
		cd './'"$1"'/LC_MESSAGES/'
		msgfmt bbot.po -o bbot.mo
		cd ../../
	};
else
	exit 1;
fi


compile ru_RU
compile en_US