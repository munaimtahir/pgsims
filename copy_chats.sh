#!/bin/bash
# Script to copy previous conversation transcripts to the workspace

SOURCE_DIR="/home/munaim/.gemini/antigravity-ide/brain"
TARGET_DIR="/home/munaim/srv/apps/pgsims/previous_chats"

echo "Creating target directory: $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi

echo "Copying transcripts..."
count=0
# Loop through all folders in brain directory
for conv_dir in "$SOURCE_DIR"/*; do
    if [ -d "$conv_dir" ]; then
        conv_id=$(basename "$conv_dir")
        transcript_file="$conv_dir/.system_generated/logs/transcript.jsonl"
        if [ -f "$transcript_file" ]; then
            cp "$transcript_file" "$TARGET_DIR/transcript_${conv_id}.jsonl"
            echo "Copied: $conv_id"
            count=$((count+1))
        fi
    fi
done

echo "Successfully copied $count past conversation(s) to the workspace!"
echo "You can now ask me to read files under: /home/munaim/srv/apps/pgsims/previous_chats/"
