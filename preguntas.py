import zipfile
import os
import pandas as pd


# Función para descomprimir el archivo ZIP
def unzip_file(zip_file: str, destination_dir: str) -> None:
    """
    Unzip a file to a destination directory
    :param zip_file: The path to the ZIP file
    :param destination_dir: The destination directory

    """
    if not os.path.exists(zip_file):
        raise FileNotFoundError(f"File {zip_file} not found")
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(destination_dir)


def read_files_and_create_dataframe(
    directory: str, nombreColumnaA: str, nombreColumnaB: str
) -> None:
    """
    Read text files from a directory and create a DataFrame with the contents
    :param directory: The directory containing the text files
    :param nombreColumnaA: The name of the column for the text content
    :param nombreColumnaB: The name of the column for the sentiment label

    """

    rows = []
    for root, dirs, files in os.walk(directory):

        for file in files:

            file_path = os.path.join(root, file)

            if file.endswith(".txt") and not file.startswith("."):
                try:
                    sentiment = os.path.basename(root)

                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        rows.append([text, sentiment])
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            else:
                print(f"Ignoring non-text file: {file_path}")

    return pd.DataFrame(rows, columns=[nombreColumnaA, nombreColumnaB])


# Descomprimir el archivo "data.zip" en la carpeta raíz
zip_file_path = "data.zip"
destination_directory = "./data/"
unzip_file(zip_file_path, destination_directory)

# Directorios de entrenamiento y prueba
train_directory = os.path.join(destination_directory, "train/")

test_directory = os.path.join(destination_directory, "test/")


# Leer los archivos de entrenamiento y prueba y crear DataFrames
train_df = read_files_and_create_dataframe(train_directory, "phrase", "sentiment")
test_df = read_files_and_create_dataframe(test_directory, "phrase", "sentiment")

# Guardar los DataFrames en archivos CSV
train_df.to_csv("train_dataset.csv", index=False)
test_df.to_csv("test_dataset.csv", index=False)
