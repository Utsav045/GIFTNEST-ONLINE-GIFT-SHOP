# Deploying to Render

This project is configured for Render with `render.yaml`, `Procfile`, and `runtime.txt`.

If you see build errors about `xhtml2pdf` or wheel building failures, follow these steps:

1. Ensure `runtime.txt` is pinned to a compatible Python version (recommended: `python-3.11.7`).
2. Ensure `requirements.txt` pins `xhtml2pdf==0.2.15` (this repo includes that pin).
3. In the Render dashboard, go to your service -> Manual Deploy -> "Clear build cache" then deploy the branch.
4. Watch build logs. If a Pillow build fails, consider using a compiled wheel (pin Pillow to a version with prebuilt wheels) or install system libs on the build image.

Common fixes:
- Build fails with KeyError '__version__' while building xhtml2pdf: pin `xhtml2pdf==0.2.15` and ensure Python is 3.11.
- Render is using Python 3.13 despite `runtime.txt`: make sure `runtime.txt` is at project root and commit/push it; then clear the build cache in Render and re-deploy.

If you'd like, I can trigger a manual redeploy and monitor the logs if you provide Render access or run the deploy and paste the log output here.
