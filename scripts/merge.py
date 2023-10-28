import os

def merge_m3u(files, output_file):
    """
    Merges multiple m3u files into a single file.

    :param files: list of m3u filenames to merge
    :param output_file: the output filename for the merged content
    """
    with open(output_file, 'w') as out_file:
        for m3u_file in files:
            if os.path.exists(m3u_file):
                with open(m3u_file, 'r') as in_file:
                    # Read and write the content of each file to the output file
                    out_file.write(in_file.read())
                    out_file.write("\n")  # Add a newline after each file to ensure separation
            else:
                print(f"Warning: {m3u_file} does not exist and will be skipped.")
        print(f"Merge complete. Output saved to {output_file}.")

if __name__ == '__main__':
    # Example usage
    files_to_merge = ['playlist1.m3u', 'playlist2.m3u', 'playlist3.m3u']
    output_filename = 'merged_playlist.m3u'
    merge_m3u(main, main)
