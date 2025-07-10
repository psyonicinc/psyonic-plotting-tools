#!/bin/bash

target_file="plot-lines.desktop"
insert_line="Exec=/home/$USER/psyonic-plotting-tools/run_docker.sh"

# Replace line 5 with the expanded line
sed -i "5c $insert_line" "$target_file"

# Copy the desktop file to system applications folder
sudo cp "$target_file" /usr/share/applications/

# Make it executable (though desktop files usually only need readable permission)
sudo chmod 644 /usr/share/applications/$(basename "$target_file")

# Update the desktop database
sudo update-desktop-database