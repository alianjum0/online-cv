<a href="https://jekyll-themes.com">
<img src="https://img.shields.io/badge/featured%20on-JT-red.svg" height="20" alt="Jekyll Themes Shield" >
</a>

# Orbit
> This theme is designed by Xiaoying Riley at [3rd Wave Media](http://themes.3rdwavemedia.com/).
> Visit [her website](http://themes.3rdwavemedia.com/) for more themes.

I have made this into a Jekyll Theme. Checkout the live demo [here](https://online-cv.webjeda.com).

<table>
  <tr>
    <th>Desktop</th>
    <th>Mobile</th>
  </tr>
  <tr>
    <td>
        <img src="https://online-cv.webjeda.com/assets/images/desktop.png?raw=true" width="600"/>
    </td>
    <td>
        <img src="https://online-cv.webjeda.com/assets/images/mobile.png?raw=true" width="250"/>
    </td>
  </tr>
</table>

## Installation

* [Fork](https://github.com/sharu725/online-cv/fork) the repository;
* Go to settings and set master branch as Github Pages source;
* Your new site should be ready at `https://<username>.github.io/online-cv/`;
* Printable version of the site can be found at `https://<username>.github.io/online-cv/print`. Use a third party link https://pdflayer.com/, https://www.web2pdfconvert.com/ etc to get the printable PDF.

Change all the details from one place: `_data/data.yml`.

### To preview/edit locally with docker

```sh
docker-compose up
```

*docker-compose.yml* file is used to create a container that is reachable under <http://localhost:4000>.
Changes *_data/data.yml* will be visible after a while.

### Local machine

* Get the repo into your machine 

```bash
git clone https://github.com/sharu725/online-cv.git
```

* Install required ruby gems

```bash
bundle install
```

* Serve the site locally

```bash
bundle exec jekyll serve
```

* Navigate to `http://localhost:4000`


## Skins

There are 6 color schemes available:

| Blue | Turquoise | Green |
|---------|---------|---------|
| <img src="https://online-cv.webjeda.com/assets/images/blue.jpg" width="300"/> | <img src="https://online-cv.webjeda.com/assets/images/turquoise.jpg" width="300"/> | <img src="https://online-cv.webjeda.com/assets/images/green.jpg" width="300"/> |

| Berry | Orange | Ceramic |
|---------|---------|---------|
| <img src="https://online-cv.webjeda.com/assets/images/berry.jpg" width="300"/> | <img src="https://online-cv.webjeda.com/assets/images/orange.jpg" width="300"/> | <img src="https://online-cv.webjeda.com/assets/images/ceramic.jpg" width="300"/> |

## Credits

Thanks to [Nelson Estevão](https://github.com/nelsonmestevao) for all the [contributions](https://github.com/sharu725/online-cv/commits?author=nelsonmestevao).

Thanks to [t-h-e(sfrost)](https://github.com/t-h-e) for all the [contributions](https://github.com/sharu725/online-cv/commits?author=t-h-e).

Check out for more themes: [**Jekyll Themes**](http://jekyll-themes.com).

## run locally
Testing your GitHub Pages site locally with Jekyll
[link](https://docs.github.com/en/free-pro-team@latest/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll)
> bundle exec jekyll serve

## run locally in docker
Testing your GitHub Pages site locally with Jekyll in docker
> docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:$JEKYLL_VERSION jekyll serve
Go to [localhost:4000/online-cv/](localhost:4000/online-cv/)

## Verified local preview and PDF checks

The current configuration uses an empty `baseurl`: open
<http://localhost:4000/> and <http://localhost:4000/print>.

For Docker on an Apple Silicon Mac, the existing Jekyll image can run with
AMD64 emulation (the first run installs the locked gems):

```sh
rtk proxy docker run --name online-cv-local --platform linux/amd64 -d \
  -p 127.0.0.1:4000:4000 \
  --mount type=bind,src="$PWD",dst=/srv/jekyll \
  jekyll/builder:4.0 jekyll serve --watch --force_polling --host 0.0.0.0 --port 4000
```

Subsequent runs can use `rtk proxy docker start online-cv-local`. Use
`rtk proxy docker logs online-cv-local` to check startup. The container started
during the October 19, 2026 setup is named `online-cv-local-20261019`.

To check the PDF blank-page regression, export using the PDF button both before
and after scrolling down. The opening content should appear on the first page,
with no large gap above it. With Poppler installed, check the actual PDFs:

```sh
rtk proxy python3 scripts/check-pdf-top.py /path/to/top.pdf /path/to/scrolled.pdf
```

For a repeatable browser check, install/use `playwright-cli`, open a session,
and pass `scripts/export-pdf-regression.js` to its `run-code` command:

```sh
rtk proxy mkdir -p /tmp/online-cv-pdf-check
rtk proxy playwright-cli -s=cv-pdf open http://127.0.0.1:4000/
rtk proxy sh -c 'playwright-cli -s=cv-pdf run-code "$(cat scripts/export-pdf-regression.js)"'
rtk proxy sh -c 'python3 scripts/check-pdf-top.py /tmp/online-cv-pdf-check/*.pdf'
```

The scenario covers desktop exports at the top, middle, and bottom, plus mobile
export after scrolling. The pixel check catches blank opening pages; visually
inspect the remaining pages for layout and pagination issues as well.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sharu725/online-cv&type=Date)](https://star-history.com/#sharu725/online-cv&Date)
