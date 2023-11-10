# sort_markdown_by_headings

Sorts a Markdown file based on headings.

## Example

### Before sorting

~~~text
# B

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## C

Nunc consequat justo eget enim finibus porta.

### A

Suspendisse potenti. Praesent sit amet.

```text
# B

# A
```

# A

## C

Pellentesque in ipsum id.

Orci porta non pulvinar neque.

Lectus vestibulum mattis ullamcorper velit.

## B

Nulla aliquet enim tortor at.

~~~

### After sorting

~~~text
# A

## B

Nulla aliquet enim tortor at.

## C

Pellentesque in ipsum id.

Orci porta non pulvinar neque.

Lectus vestibulum mattis ullamcorper velit.

# B

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## C

Nunc consequat justo eget enim finibus porta.

### A

Suspendisse potenti. Praesent sit amet.

```text
# B

# A
```

~~~

## Example using -s to sort content between headings

### Before sorting

~~~text
# A

## E

- [Zenodo](https://zenodo.org)
- [datalad/datalad](https://github.com/datalad/datalad)

## D

- [ChartsCSS/charts.css](https://github.com/ChartsCSS/charts.css)
- [arvestad/alv](https://github.com/arvestad/alv)

## C

- [Quay](https://quay.io)
- [Docker Hub](https://hub.docker.com)

## B

- [ffmprovisr](https://amiaopensource.github.io/ffmprovisr/)
- [ffmpeg](https://ffmpeg.org)

## A

- [faressoft/terminalizer](https://github.com/faressoft/terminalizer)
- [BioRender](https://biorender.com)

~~~

### After sorting

~~~text
# A

## A

- [BioRender](https://biorender.com)
- [faressoft/terminalizer](https://github.com/faressoft/terminalizer)

## B

- [ffmpeg](https://ffmpeg.org)
- [ffmprovisr](https://amiaopensource.github.io/ffmprovisr/)

## C

- [Docker Hub](https://hub.docker.com)
- [Quay](https://quay.io)

## D

- [arvestad/alv](https://github.com/arvestad/alv)
- [ChartsCSS/charts.css](https://github.com/ChartsCSS/charts.css)

## E

- [datalad/datalad](https://github.com/datalad/datalad)
- [Zenodo](https://zenodo.org)

~~~

## Usage

```text
usage: sort_markdown_by_headings.py [-h] [-o OUTPUT] [-s] input

Sorts a Markdown file based on headings.

positional arguments:
  input                 Markdown file to parse

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Markdown file to create, otherwise write to stdout
  -s, --sort            sort the content between headings

python sort_markdown_by_headings.py input
```