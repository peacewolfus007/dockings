#!/bin/bash

for file in *.gjf; do
	    base_name=$(basename "$file" .gjf)
	        g09 < "$file" > "${base_name}_out.log"
		    echo "Processed $file, output saved to ${base_name}_out.log"
	    done

