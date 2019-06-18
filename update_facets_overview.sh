#!/usr/bin/env bash

BASE="$(realpath "$(dirname $0)")"

# Copy facets overview modules
rm -rf "${BASE}/ipyfacets/overview/"
mkdir -p "${BASE}/ipyfacets/overview/"
cp -r "${BASE}/facets/facets_overview/python/." "${BASE}/ipyfacets/overview/"

files=$(find "${BASE}/ipyfacets/overview/" -regex "${BASE}/ipyfacets/overview/[a-z][a-z_]+.py")

modules=(
	"base_feature_statistics_generator"
	"base_generic_feature_statistics_generator"
	"feature_statistics_generator"
	"generic_feature_statistics_generator"
	"feature_statistics_pb2"
)

# Fix imports for distribution
for file in ${files}; do
	for module in "${modules[@]}"; do
		sed -i "s/from ${module}/from .${module}/g" "${file}"
		sed -i "s/import ${module}/from . import ${module}/g" "${file}"
	done
done
