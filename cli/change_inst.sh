#!/bin/bash

FICH="$1"

cat $FICH.asm | sed -e "s/cbr/bclr/g" | sed -e "s/sbr/bset/g" | sed -e "s/tbr/bchg/g" | sed -e "s/bcrs/btsts/g" > "$FICH"_2U.asm
