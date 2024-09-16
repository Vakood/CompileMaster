# CompileMaster

## Установка

1. ```git clone https://github.com/Vakood/CompileMaster.git```
2. ```pip install build```
3. ```python -m build```
4. ```pip install .```

## Команды

1. ```compl -h```  <-- Показывает меню помощи
2. ```compl -b```  <-- Создает архив с названием, указанным в конфигурационном файле
3. ```compl -e```  <-- Команда для разархивирования. Требуется указать ключ для расшифровки архива
4. ```compl -f```  <-- Указывает файл архива, который нужно разархивировать
5. ```compl -d```  <-- Указывает папку, в которую будет разархивирован архив

## Преимущества

### Упаковка файлов и папок

С помощью команды `compl -b` вы можете упаковать файлы и папки в собственный зашифрованный архив, что предоставляет несколько преимуществ:

- **Защита данных**: Упаковка с использованием шифрования гарантирует, что ваши данные защищены от несанкционированного доступа. Архивы создаются в формате `.compl`, который зашифрован с помощью уникального ключа.
- **Удобное управление конфигурацией**: Конфигурационный файл TOML позволяет легко указать, какие файлы и папки должны быть включены в архив. Это упрощает процесс создания архива и делает его более гибким.
- **Автоматическое создание ключа**: При упаковке автоматически создается ключ для шифрования, который сохраняется в отдельном файле. Это упрощает управление безопасностью ваших данных.

### Распаковка файлов и папок

Команда `compl -e` позволяет распаковать зашифрованный архив. Преимущества распаковки с использованием ключа включают:

- **Безопасность**: Распаковка осуществляется только с использованием правильного ключа, что обеспечивает безопасность ваших данных. Это предотвращает несанкционированный доступ к содержимому архива.
- **Гибкость в выборе места для распаковки**: Вы можете указать, в какую папку следует распаковать архив, что позволяет легко интегрировать распакованные файлы в вашу файловую структуру.
- **Поддержка различных форматов**: Архивы могут содержать как файлы, так и папки, обеспечивая удобный способ для резервного копирования и передачи данных.

## Пример конфигурационного файла для создания архива

.toml

```toml
[archive]
name = "test"

[[files]]
path = "app.py"

[[files]]
path = "test.py"

[[folders]]
path = "some_folder"
