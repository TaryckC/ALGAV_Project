#!/bin/bash

#!/bin/bash

# Vérification du nombre d'arguments
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <action> <x> <filename> [optional_param]"
    exit 1
fi

# Récupération des arguments
ACTION=$1
X=$2
FILENAME=$3

# Cas avec 4 arguments
if [ "$#" -eq 4 ]; then
    OPTIONAL_PARAM=$4
    echo "Quatre arguments détectés."
    echo "Action: $ACTION"
    echo "X: $X"
    echo "Filename: $FILENAME"
    echo "Optional Parameter: $OPTIONAL_PARAM"
    python3 main.py "$ACTION" "$X" "$FILENAME" "$OPTIONAL_PARAM"
else
    # Cas avec 3 arguments
    echo "Trois arguments détectés."
    echo "Action: $ACTION"
    echo "X: $X"
    echo "Filename: $FILENAME"
    python3 main.py "$ACTION" "$X" "$FILENAME"
fi
