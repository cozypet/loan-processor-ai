# 🚀 Streamlit Cloud Deployment Guide

This guide will walk you through deploying the AI-Powered Loan Application Processor to Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub account** - [Sign up](https://github.com/signup)
2. **Streamlit Cloud account** - [Sign up](https://share.streamlit.io/signup)
3. **Your API credentials** ready:
   - Azure Mistral Document AI key
   - Azure Ministral-3B key
   - MongoDB Atlas connection string

## 🔄 Step 1: Push to GitHub

### 1.1 Create a New GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository (e.g., `loan-processor-ai`)
3. Choose **Public** or **Private** (both work with Streamlit Cloud)
4. **Don't** initialize with README (we already have files)

### 1.2 Push Your Code

```bash
cd "/path/to/IssuranceDocAI"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Loan Processor"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/loan-processor-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** The `.gitignore` file will automatically exclude:
- `.env` (your local credentials)
- `venv/` (virtual environment)
- Other sensitive files

## ☁️ Step 2: Deploy to Streamlit Cloud

### 2.1 Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **"New app"**
3. Connect your GitHub account (if not already)

### 2.2 Configure Deployment Settings

Fill in the deployment form:

- **Repository:** Select `YOUR_USERNAME/loan-processor-ai`
- **Branch:** `main`
- **Main file path:** `app.py`
- **App URL:** Choose your custom URL (e.g., `loan-processor-demo`)

Click **"Advanced settings"** before deploying!

### 2.3 Configure Secrets

In the **Advanced settings** > **Secrets** section, paste the following (replace with your actual values):

```toml
# Mistral Document AI Configuration
AZURE_MISTRAL_DOCAI_ENDPOINT = "https://francecentral.api.cognitive.microsoft.com/providers/mistral/azure/ocr"
AZURE_MISTRAL_DOCAI_KEY = "your-actual-docai-key-here"

# Ministral-3B Chat Configuration
AZURE_MINISTRAL_ENDPOINT = "https://francecentral.api.cognitive.microsoft.com/models/chat/completions?api-version=2024-05-01-preview"
AZURE_MINISTRAL_KEY = "your-actual-ministral-key-here"
AZURE_MINISTRAL_MODEL = "maas-foundry-ministral-3b"

# MongoDB Configuration
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DATABASE = "loan_processor"
MONGODB_COLLECTION = "loan_applications"
```

### 2.4 Deploy!

Click **"Deploy!"**

Streamlit Cloud will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Run your app
4. Provide a public URL

⏱️ Deployment typically takes 2-3 minutes.

## ✅ Step 3: Verify Deployment

Once deployed, your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

### Test the Application

1. Open the URL
2. Upload sample PDFs (from `sample_documents/`)
3. Click "Process Application"
4. Verify all steps complete successfully
5. Check MongoDB to confirm data was saved

## 🔧 Post-Deployment

### Update Your App

When you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will **automatically redeploy** within ~30 seconds!

### View Logs

- Click on your app in [Streamlit Cloud dashboard](https://share.streamlit.io/)
- Click **"Manage app"** > **"Logs"**
- Monitor real-time logs for debugging

### Update Secrets

1. Go to app settings in Streamlit Cloud
2. Click **"Secrets"**
3. Edit and save
4. App will automatically restart

## 🐛 Troubleshooting

### "ModuleNotFoundError"

**Problem:** Missing dependency

**Solution:**
1. Check `requirements.txt` includes all packages
2. Push updated `requirements.txt` to GitHub
3. Streamlit Cloud will auto-redeploy

### MongoDB Connection Error

**Problem:** SSL certificate or connection string issue

**Solution:**
1. Verify `MONGODB_URI` in Streamlit secrets
2. Check MongoDB Atlas allows connections from `0.0.0.0/0` (all IPs)
3. Our app already has `tlsAllowInvalidCertificates=True` for compatibility

### Secrets Not Loading

**Problem:** App can't read secrets

**Solution:**
1. Check secrets format in Streamlit Cloud (must be valid TOML)
2. Ensure no extra quotes or spaces
3. Restart app from Streamlit Cloud dashboard

### App Crashes on Startup

**Problem:** Configuration error

**Solution:**
1. Check logs in Streamlit Cloud
2. Verify all required secrets are set
3. Test locally first with `.env` file

## 📊 Monitoring

### View App Analytics

Streamlit Cloud provides:
- **Viewer count:** Number of active users
- **Resource usage:** CPU and memory
- **Logs:** Real-time application logs

### MongoDB Monitoring

Check MongoDB Atlas dashboard for:
- Connection count
- Database size
- Query performance

## 🔒 Security Best Practices

### Secrets Management

✅ **Do:**
- Use Streamlit Cloud secrets for credentials
- Keep `.env` in `.gitignore`
- Rotate API keys periodically
- Use separate MongoDB databases for dev/prod

❌ **Don't:**
- Commit `.env` to GitHub
- Share secrets in public repositories
- Use production credentials in development

### MongoDB Security

1. **Whitelist IPs:** Add `0.0.0.0/0` in MongoDB Atlas for Streamlit Cloud
2. **Strong passwords:** Use complex database passwords
3. **Read-only users:** Consider separate read/write users

## 🎯 Custom Domain (Optional)

To use your own domain:

1. Purchase domain (e.g., from Namecheap, GoDaddy)
2. In Streamlit Cloud: Settings > Custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (~24-48 hours)

## 💰 Cost Estimation

### Streamlit Cloud
- **Free tier:** 1 app, unlimited viewers
- **Pro:** $20/month for private apps + more resources

### Azure Mistral AI
- Pay-per-use pricing
- Document AI: ~$0.01 per page
- Ministral-3B: ~$0.001 per 1K tokens

### MongoDB Atlas
- **Free tier (M0):** 512 MB storage
- Sufficient for demos and small deployments

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [MongoDB Atlas Setup](https://www.mongodb.com/docs/atlas/getting-started/)
- [Mistral AI Documentation](https://docs.mistral.ai/)

## 🆘 Support

- **Streamlit Community:** [forum.streamlit.io](https://forum.streamlit.io/)
- **MongoDB Support:** [MongoDB Community](https://www.mongodb.com/community/forums/)
- **Mistral AI:** [Mistral AI Discord](https://discord.gg/mistralai)

---

**Ready to deploy!** 🚀 Follow the steps above and your AI loan processor will be live in minutes!
