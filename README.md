# Dastak 90807 website

Static website for www.dastak90807.com, hosted on Cloudflare Pages.

The repository was reconstructed from the owner's Hostinger archive and the current public Cloudflare Pages deployment on 21 November 2026. The archive included older update packages and a damaged ZIP index. This repository contains the current published site files and does not include those historical packages.

To run locally, serve this directory with any static HTTP server. The current Cloudflare Pages project uses Direct Upload. Cloudflare does not convert a Direct Upload project to Git integration. To use native Git integration, create a new Pages project connected to this repository, select `main` as the production branch, leave the build command empty, and set the build output directory to `.` (the repository root). After checking its preview URL, move the custom domain to the new project. The existing project can instead be deployed from GitHub Actions using the Cloudflare Pages API.
