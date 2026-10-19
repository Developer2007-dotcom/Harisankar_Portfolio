# Deploy the Django portfolio on Vercel

This project is set up for Vercel's Django runtime. Vercel detects the root `manage.py`, runs `collectstatic` during the build, and serves static files through its CDN. The contact form sends enquiries through Resend and does not save them to a database. Signed-cookie sessions cover the current site features without requiring a database.

## 1. Put the project in GitHub

1. Extract `harisankar_django_portfolio_vercel.zip`.
2. Create a GitHub repository and upload the extracted project contents so `manage.py` is at the repository root. Do not commit `.env` or API keys; `.gitignore` excludes `.env`.
3. In Vercel, choose **Add New → Project**, import the repository, and keep the project root at the folder containing `manage.py`.
4. Vercel should detect Django automatically. Keep the detected framework/build settings; this project does not need a Render Blueprint or custom build command.
5. Add the environment variables in section 2, then deploy.

If Vercel system variables are unavailable, enable **Project Settings → Environment Variables → Automatically expose System Environment Variables**. The app uses Vercel's deployment hostname automatically. For a custom domain, add its hostnames and HTTPS origins to the variables below.

## 2. Add Vercel environment variables

In **Project → Settings → Environment Variables**, add these for **Production** (and **Preview** if preview builds should send email):

| Name | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | A long, unique random secret. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` and paste the output into Vercel. |
| `DJANGO_DEBUG` | `false` |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost,your-project.vercel.app,yourdomain.com,www.yourdomain.com` — replace sample domains with actual hostnames. Vercel deployment hosts are also allowed automatically. |
| `CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app,https://yourdomain.com,https://www.yourdomain.com` — replace with the HTTPS origins you use. |
| `RESEND_API_KEY` | Your private Resend API key (`re_...`). |
| `RESEND_FROM_EMAIL` | A sender on your verified domain, e.g. `Portfolio enquiries <portfolio@mail.yourdomain.com>`. |
| `CONTACT_TO_EMAIL` | The inbox where enquiries should arrive. It defaults to the email address in the CV. |

Never add the real Resend key to source code, GitHub, or a committed `.env`. Vercel applies changed environment variables to new deployments, so redeploy after changing them.

## 3. Set up Resend email delivery

1. In Resend, add a domain you own. A mail subdomain such as `mail.yourdomain.com` can be used as the sender domain.
2. At your DNS provider, add the exact verification and sending records shown by Resend, including SPF/DKIM. Wait until Resend marks the domain verified.
3. Create a Resend API key and add it as `RESEND_API_KEY` in Vercel.
4. Set `RESEND_FROM_EMAIL` to an address on that verified domain and `CONTACT_TO_EMAIL` to your inbox.
5. Redeploy, submit the contact form using an email address you can access, and confirm delivery. The visitor's address is configured as reply-to.
6. If delivery fails, check Vercel function logs and Resend email logs. Confirm the sender domain, recipient, and environment selections.

The sample `onboarding@resend.dev` sender is for limited testing; production should use a sender on your verified domain.

## 4. Add your custom domain

1. In Vercel, open **Project → Settings → Domains** and add your domain.
2. Copy the DNS records Vercel shows into your registrar's DNS settings. Wait for Vercel to verify the domain and enable HTTPS.
3. Update `DJANGO_ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` with the exact custom hostnames and HTTPS origins. Save and redeploy.
4. Canonical and sitemap URLs use the active request host. Check them on your chosen production domain after DNS is ready.

## 5. Finish search-engine setup

Pages include individual titles and descriptions, canonical URLs, Open Graph metadata, Person structured data for Trivandrum, Kerala, and live `/robots.txt` and `/sitemap.xml` endpoints.

1. Open `https://YOUR-DOMAIN/robots.txt` and `https://YOUR-DOMAIN/sitemap.xml` on the final public domain.
2. Add the domain as a property in Google Search Console and verify ownership using its DNS TXT record.
3. In Search Console, submit `https://YOUR-DOMAIN/sitemap.xml` under **Sitemaps**.
4. Use URL Inspection for Home, Work, Skills, About, and Contact. Request indexing after the public pages look correct.
5. Edit each page's title and description in `portfolio/templates/portfolio/`. Update structured data and social links in `base.html` when those details change.

Search engines control indexing and rankings; setup cannot guarantee a particular position.

## 6. Before launch

- Replace the Facebook profile URL placeholder in `portfolio/templates/portfolio/base.html`.
- Confirm the production sender and destination inbox.
- Confirm `DJANGO_DEBUG=false` and allowed hosts/origins match the Vercel and custom domains.
- Check the contact form, social links, `/robots.txt`, and `/sitemap.xml` on the deployed site.
- Push updates to the connected Git branch; Vercel will create a deployment.

## Run locally on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`, then run:

```powershell
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. `runserver` is for local development only.

## Official references

- [Vercel: Deploy a Django app](https://vercel.com/docs/frameworks/full-stack/django)
- [Vercel: Environment variables](https://vercel.com/docs/environment-variables)
- [Django: Deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)
- [Resend: Verified domains](https://resend.com/docs/dashboard/domains/introduction)
- [Resend: Django email guide](https://resend.com/django)
- [Google Search Console: Verify site ownership](https://support.google.com/webmasters/answer/9008080)
- [Google Search Central: Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
