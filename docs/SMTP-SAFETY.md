# SMTP reporting safety

Keep `seo_auditor/config/smtp.json` out of version control. Use a dedicated, revocable SMTP credential and restrict report recipients to authorized addresses. SEO reports can contain private URLs or query parameters; inspect reports before emailing them.

Before enabling email, run the CLI without `--email` against a site you control and verify the generated reports. Then test delivery with a dedicated mailbox. If a credential is accidentally committed, revoke it immediately; deleting the file alone does not remove it from Git history.
