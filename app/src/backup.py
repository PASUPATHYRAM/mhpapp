import subprocess


def backup_database(database_name, output_file):
    # Ensure the command is executed as a shell command
    result = subprocess.run(f'pg_dump -Fc -f {output_file} {database_name}', shell=True)

    # Check if the backup was successful
    if result.returncode == 0:
        print("Backup successful.")
    else:
        print("Backup failed.")


# Call the function with the database name and the desired output file path
backup_database('MHP', '/app/output.dump')
