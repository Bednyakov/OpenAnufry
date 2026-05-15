#!/bin/bash
URI="$1"
DATABASE="$2"
COLLECTION="$3"
QUERY="$4"

if [ -z "$URI" ] || [ -z "$DATABASE" ] || [ -z "$COLLECTION" ] || [ -z "$QUERY" ]; then
    echo "Usage: $0 <uri> <database> <collection> '<query_json>'"
    exit 1
fi

mongosh "${URI}/${DATABASE}" --eval "
  const result = db.${COLLECTION}.find(${QUERY}).limit(50).toArray();
  printjson(result);
"
