# Publish this repository with GitHub Pages

The website is already generated. GitHub Pages serves `index.html` and the existing assets, model files, reports, and downloads; no Python or RTL compilation is needed on the hosting server. `.nojekyll` is included, and `.gitignore` excludes local `.qa/` browser tools and screenshots.

The commands below use `lia-lim` as an example repository name under `llgelarall`. Replace it throughout if you choose another name.

## 1. Create an empty repository

Open [New repository](https://github.com/new), choose owner `llgelarall`, and enter `lia-lim`. Choose **Public** and leave the README, `.gitignore`, and license initialization options unchecked. Create the repository.

Suggested description: “LIA/LIM approximate adders and multipliers: C, Python and Verilog models, exhaustive error metrics, synthesis comparisons and downloads.”

GitHub's [local-code import instructions](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) explain this empty-repository workflow.

## 2. Push this folder

Open PowerShell and run:

```powershell
Set-Location 'D:\ICVLSI\LimLia\lia_lim_website_starter\lia_lim_site'
git init -b main
git add .
git commit -m "Publish LIA/LIM library website"
git remote add origin https://github.com/llgelarall/lia-lim.git
git push -u origin main
```

Complete the GitHub sign-in if prompted. These initialization commands are for the first upload of this currently uninitialized folder.

## 3. Enable the webpage

In the new repository, open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**, choose **main** and **/(root)**, and click **Save**. Check the repository's **Actions** tab for deployment progress, then use **Visit site** in Pages settings. See GitHub's [publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The standard project URL for this example is `https://llgelarall.github.io/lia-lim/`. Use the actual URL shown in Pages settings: if your account's user site has a custom domain, project sites can inherit it, for example `https://gisink.com/lia-lim/`. See [custom domains across repositories](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages#using-a-custom-domain-across-multiple-repositories). The example repository and site URLs are not configured or published by this document.

## 4. Set the actual public URLs for search engines

Open `data/catalog.json` and update its existing `site` object:

- `site.url`: the exact published URL from Pages settings, ending in `/`.
- `site.repository_url`: `https://github.com/llgelarall/lia-lim`, using your chosen repository name.

Then run:

```powershell
python tools/catalog.py build
git add .
git commit -m "Configure public website URLs"
git push
```

The build generates the canonical URL, Open Graph URL, and sitemap from your real URL. Subsequent pushes to `main` update the website automatically.

For later edits, use `git add .`, `git commit -m "Describe the update"`, and `git push`. Rebuild locally first when editing catalog data or generated tables.
