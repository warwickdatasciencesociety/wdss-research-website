# WDSS Research Website

This repository hosts the legacy version of WDSS's research blog. This is still in use whilst we develop the new system.

## Overview

### Architecture

The blog architecture is shown in the diagram below.

```
                  nbconvert              hexo
Jupyter Notebook -----------> Markdown --------> HTML
```

The rawest form of a blog post is a Jupyter notebook (stored in `content`). These are then converted to markdown files using the Python script in `build`, which mainly consists of calls to `nbconvert`, saving the results in `source`. [Hexo](https://hexo.io) can then read these markdown files to generate the website.

## Contributing to the Blog

### Prerequisities

- An installation of Conda (preferably through [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- An installation of [Git](https://git-scm.com/downloads)
- Basic knowledge of [Jupyter Notebook](https://www.youtube.com/watch?v=HW29067qVWk) (or Lab if you're feeling fancy)
- Basic knowledge of [Markdown](https://www.markdownguide.org/basic-syntax/)

### Navigation

#### Linux

- You can open a terminal at specific location by right-clicking in any empty space in the file explorer
- Alternately, you can use `cd <path>` (short for change directory) to move to a specific path

#### MacOS

- As with Linux but you open a terminal in a folder by right-clicking on the folder itself

#### Windows (Miniconda and Git)

- You can open a Git terminal by right clicking in any empty space in the file explorer and selecting Git Bash (not Git GUI)
- You can navigate using `cd` as with Linux but note that Windows uses backslashes for paths rather than regular slashes

### Setup (one-off)

- Fork WDSS's repo using the button in the top-right of GitHub
- Open a terminal (Linux/MacOS) or Git Bash (Windows) in a location where you would like to store the research blog files
- Clone this repository by running `git clone https://github.com/<your-username>/wdss-research-website.git` (or use SSH if you wish)
- If using Windows, switch to the Miniconda prompt at this point
- Create a Conda environment with the requirements for this repository with `conda env create -f environment.yml`
- Activate the environment with `conda activate wdss-research-blog-env`
- Install NodeJS dependencies with `npm install .`
- Globally install the Hexo command line interface with `npm install -g hexo-cli`

### Writing a Post (every time)

- Open a terminal (Linux/MacOS) or Miniconda prompt (Windows) at the repository root
- Launch Jupyter with `jupyter notebook`
- If you haven't already, create a notebook for your post in `content` by copying an existing post
- Fill in the metadata, write your post, and run the cells to create output
- Stop Jupyter using `ctrl-c`
- Run the build script with `python build/build_pages.py` (`\` for Windows)
- Launch Hexo with `hexo server` and visit `localhost:4000` in your browser to see the results

#### Tag Plugins

You can create pretty banners using 

```
{% note <type> %}
<content>
{% endnote %}
```

placed in a **raw** cell. The valid types are `success`, `info`, `warning`, `error` (green, blue, yellow, red, respectively).

#### Other Languages

To use other languages than Python, see:

- [R](https://github.com/IRkernel/IRkernel)
- [Julia](https://github.com/JuliaLang/IJulia.jl)

### Publishing

- When you are happy with your post, commit your changes to your fork using `git add .`, `git commit -m <message>`, `git push`
- On visiting your repo on GitHub, you will find a button to create a pull request. Do so, and assign the current Research Lead and Editor as reviewers.

## Accessing Post Sources

It is currently rather difficult to access post sources in a reproducible way. The notebooks that are used to create the blog can be found in `content`.

There are a few caveats:
- The state of the notebook in `content` is likely but not guaranteed to match the blog.
- The environment used to create the notebook is not stored so you will have to install all packages required to run the notebook.
- Blog posts may have data dependencies that are not included in the repo (particularly large files). Either contact the author or look for links in the blog post to download these.
