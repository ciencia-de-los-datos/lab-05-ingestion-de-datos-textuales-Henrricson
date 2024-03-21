import zipfile
import os
import pandas as pd


# Función para descomprimir el archivo ZIP
def unzip_file(zip_file, destination_dir):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(destination_dir)


# Función para leer los archivos de texto y obtener los datos
def read_files_and_create_dataframe(directory, nombreColumnaA, nombreColumnaB):
    rows = []
    for root, dirs, files in os.walk(directory):
        # Ignorar la carpeta __MACOSX y todas sus subcarpetas
        # if os.path.basename(root) == "__MACOSX":
        print(f"carpetas: {os.path.basename(root)}")

        print(
            f"Reading {len(files)} files from {root} with {len(dirs)} subdirectories."
        )
        for file in files:
            # print(f"Reading {file} from {root}")
            file_path = os.path.join(root, file)
            # print(file_path)
            if file.endswith(".txt") and not file.startswith(
                "."
            ):  # Leer solo archivos de texto y omitir archivos ocultos
                try:
                    sentiment = os.path.basename(
                        root
                    )  # Obtener la etiqueta de sentimiento desde el directorio padre

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
train_directory = os.path.join(destination_directory, "train")
test_directory = os.path.join(destination_directory, "test")

# Leer los archivos de entrenamiento y prueba y crear DataFrames
train_df = read_files_and_create_dataframe(train_directory, "phrase", "sentiment")
test_df = read_files_and_create_dataframe(test_directory, "phrase", "sentiment")

# Guardar los DataFrames en archivos CSV
train_df.to_csv("train_dataset.csv", index=False)
test_df.to_csv("test_dataset.csv", index=False)
