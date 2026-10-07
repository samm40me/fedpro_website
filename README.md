# FEDPRO Energy Resources Limited Website

Corporate website for **FEDPRO Energy Resources Limited**.

## Structure
- `index.html` – single-page corporate website
- `styles.css` – responsive FEDPRO navy/gold styling
- `script.js` – navigation, reveal animation, contact-email handler
- `assets/fedpro-logo.png` – supplied company logo

## Branch model
- `feature` – feature work
- `develop` – integration/development
- `test` – testing / QA
- `main` – production-ready branch

## Before production launch
1. Replace `CONTACT_EMAIL` in `script.js` with the official FEDPRO email address.
2. Add the exact registered office address, telephone and social links if desired.
3. Review corporate-object wording with company counsel before presenting it as legal text.
4. Configure a custom domain and HTTPS through your chosen host.

## Local preview
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`.
