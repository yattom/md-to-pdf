# md-to-pdf

A tool to automatically convert Markdown files to PDF using Sphinx.

## Features

- Automatically converts Markdown files to PDF
- Works as a standalone application
- Processes files in local directories and places PDFs in the same directory
- Monitors directories for changes to Markdown files
- Automatically triggers conversion when files are edited or updated
- Uses a 1-minute delay that extends if additional changes occur during the delay period

## Installation

### Prerequisites

- Python 3.8 or higher
- Sphinx
- rinohtype (for PDF generation without LaTeX)

```bash
# Install dependencies
pip install sphinx myst-parser rinohtype
```

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/yattom/md-to-pdf.git
cd md-to-pdf

# Install the package
pip install -e .
```

## Usage

### Converting a Single File

To convert a single Markdown file to PDF:

```bash
md-to-pdf convert path/to/file.md
```

You can specify an output path:

```bash
md-to-pdf convert path/to/file.md --output path/to/output.pdf
```

### Watching a Directory

To watch a directory for changes to Markdown files:

```bash
md-to-pdf watch path/to/directory
```

Options:

- `--recursive` or `-r`: Watch subdirectories recursively
- `--delay` or `-d`: Set the delay in seconds before conversion (default: 60)

```bash
md-to-pdf watch path/to/directory --recursive --delay 30
```

## How It Works

md-to-pdf uses Sphinx with the MyST parser to convert Markdown to PDF. When watching a directory, it monitors for changes to Markdown files and triggers conversion after a specified delay period. If additional changes are detected during the delay period, the timer is reset.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yattom/md-to-pdf.git
cd md-to-pdf

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

---

# md-to-pdf (日本語)

Sphinxを使用してMarkdownファイルを自動的にPDFファイルに変換するツールです。

## 特徴

- Markdownファイルを自動的にPDFに変換
- スタンドアロンアプリケーションとして動作
- ローカルディレクトリ内のファイルを処理し、同じディレクトリにPDFを配置
- ディレクトリを監視してMarkdownファイルの変更を検出
- ファイルが編集または更新されると自動的に変換を実行
- 1分間の遅延を設け、遅延時間中に変更があれば延長

## インストール

### 前提条件

- Python 3.8以上
- Sphinx
- rinohtype (LaTeXなしでPDF生成)

```bash
# 依存関係のインストール
pip install sphinx myst-parser rinohtype
```

### ソースからのインストール

```bash
# リポジトリのクローン
git clone https://github.com/yattom/md-to-pdf.git
cd md-to-pdf

# パッケージのインストール
pip install -e .
```

## 使用方法

### 単一ファイルの変換

単一のMarkdownファイルをPDFに変換するには：

```bash
md-to-pdf convert path/to/file.md
```

出力パスを指定することもできます：

```bash
md-to-pdf convert path/to/file.md --output path/to/output.pdf
```

### ディレクトリの監視

Markdownファイルの変更を監視するには：

```bash
md-to-pdf watch path/to/directory
```

オプション：

- `--recursive` または `-r`：サブディレクトリを再帰的に監視
- `--delay` または `-d`：変換前の遅延時間（秒）を設定（デフォルト：60）

```bash
md-to-pdf watch path/to/directory --recursive --delay 30
```

## 動作の仕組み

md-to-pdfはSphinxとMyST parserを使用してMarkdownをPDFに変換します。ディレクトリを監視する場合、Markdownファイルの変更を監視し、指定された遅延時間後に変換をトリガーします。遅延時間中に追加の変更が検出された場合、タイマーはリセットされます。

## 開発

### 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yattom/md-to-pdf.git
cd md-to-pdf

# 開発用依存関係のインストール
pip install -e ".[dev]"
```

### テストの実行

```bash
pytest
```
